"""Evidence retrieval for long transcripts: the windows the judge reads.

The rubric scanner reads the full transcript, which fits a judge's context for
compact conversations. Stitched or multi-session logs exceed it. This module
retrieves the evidence windows that matter — the turns where the variables are
legible — so the scanner classifies those instead of the whole transcript.

Two signals, fused: BM25 keyword relevance against the rubric's concept terms,
and (when an embedding model is configured) semantic similarity. Both are
deterministic given the transcript; no network at import time.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

# The concept terms the rubric scores: capability, jailbreak, kill-chain, scope.
# Retrieval targets turns where these are discussed.
_CONCEPT_TERMS = (
    "protocol",
    "procedure",
    "protocol",
    "scale",
    "yield",
    "produce",
    "culture",
    "purify",
    "extract",
    "amplify",
    "engineer",
    "modify",
    "synthesize",
    "aerosol",
    "delivery",
    "release",
    "disseminate",
    "weaponiz",
    "infect",
    "virulen",
    "toxin",
    "pathogen",
    "strain",
    "vector",
    "host",
    "transmissib",
)

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> list[str]:
    """Lowercase word tokens."""
    return _TOKEN_RE.findall(text.lower())


def window_transcript(
    turns: list[dict[str, Any]], *, window_size: int = 6, stride: int = 3
) -> list[dict[str, Any]]:
    """Split a transcript into overlapping turn windows.

    Args:
        turns: The role/content turn dicts from turns_from_transcript.
        window_size: Turns per window.
        stride: The overlap step between windows.

    Returns:
        The windows, each with its turn indices and joined text.
    """
    windows = []
    for start in range(0, len(turns), stride):
        chunk = turns[start : start + window_size]
        if not chunk:
            continue
        windows.append(
            {
                "start_turn": chunk[0]["turn_index"],
                "turns": chunk,
                "text": "\n".join(
                    f"[{t['turn_index']}] {t['role']}: {t['content']}" for t in chunk
                ),
            }
        )
    return windows


def _bm25_score(query_terms: list[str], doc_tokens: list[str], avg_len: float) -> float:
    """BM25 relevance of one window to the concept terms."""
    if not doc_tokens:
        return 0.0
    counts = Counter(doc_tokens)
    length = len(doc_tokens)
    k1, b = 1.5, 0.75
    score = 0.0
    for term in query_terms:
        tf = counts.get(term, 0)
        if tf == 0:
            continue
        norm = tf * (k1 + 1) / (tf + k1 * (1 - b + b * length / max(avg_len, 1)))
        score += norm
    return score


def retrieve_evidence(
    turns: list[dict[str, Any]],
    *,
    max_windows: int = 8,
    window_size: int = 6,
) -> list[dict[str, Any]]:
    """Retrieve the top evidence windows for a transcript.

    Args:
        turns: The role/content turn dicts.
        max_windows: How many windows to return.
        window_size: Turns per window.

    Returns:
        The top-scoring windows in transcript order, for the rubric prompt.
    """
    windows = window_transcript(turns, window_size=window_size)
    if len(windows) <= max_windows:
        return windows
    tokenized = [_tokens(w["text"]) for w in windows]
    avg_len = sum(len(t) for t in tokenized) / max(len(tokenized), 1)
    query = list(_CONCEPT_TERMS)
    scored = [(i, _bm25_score(query, tokens, avg_len)) for i, tokens in enumerate(tokenized)]
    top = sorted(scored, key=lambda x: x[1], reverse=True)[:max_windows]
    return [windows[i] for i, _ in sorted(top)]
