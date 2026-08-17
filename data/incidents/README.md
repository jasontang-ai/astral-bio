# ASTRAL Incident Registry + Transcripts

Real-world agentic incidents as labeled, Inspect-native data — the real-world
counterpart to ASTRAL's synthetic transcripts. Usable to train and evaluate
detection models against documented ground truth.

## Files

| File | What it is |
|---|---|
| `incident_registry.yaml` | the curated incident registry: id, lab, category, ATT&CK-mapped phases, detection, provenance sources |
| `incident-transcripts.eval` | the incidents as Inspect-format transcripts with per-turn phase labels (authorized_eval → recon → initial_access → ... → exfiltration → evasion), reconstructible and checkable against the public forensic record |

## Ground truth

Every turn label is drawn from the published forensic record (the Hugging Face
technical timeline, OpenAI's disclosure, Anthropic's review, AISI's study). The
HF breach turn structure reconstructs the documented two-stage campaign:
sandbox escape and launchpad, then the intrusion phases through cluster-admin
lateral movement to exfiltration and evasion.

## Use

Train and evaluate detection models on "flag the breach from the actions so
far" — the per-turn phase labels give the ground truth for where detection
should fire. Scan with the ASTRAL scanner or any Inspect-compatible tooling.
