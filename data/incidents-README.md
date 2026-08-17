# ASTRAL Incident Registry

Curated, labeled records of documented autonomous-agent incidents, grounded in
public evidence. Each incident is one registry entry with provenance-linked
phases, so the records can ground the cyber pipeline's compiler, evaluate
detection methods, and seed transcript generation.

## Sources (all public)

| Incident | Source | Evidence level |
|---|---|---|
| OpenAI/HF breach (Jul 9-13, 2026) | HF forensic timeline + OpenAI disclosure | full: 17,600 actions, 6,280 clusters, verbatim commands |
| Anthropic's 3 incidents (Apr-Jul 2026) | Anthropic's review (141,006 runs) | summary: per-incident accounts |
| AISI near-miss | AISI cheating-behaviour study (475 runs x 5 models) | summary + stats |
| OpenAI sandbox-escape PR incident (Jul 20) | OpenAI long-horizon post | summary |
| METR-documented incidents | METR Frontier Risk Report | aggregate |

## Schema

Each incident: id, date range, lab, model(s), category (intrusion / eval-cheating
/ sandbox-escape), phases (ATT&CK-mapped), detection (how caught, at what
stage), sources (linked receipts).
