# ASTRAL

![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

ASTRAL is an open framework for evaluating biosecurity risk in AI
conversations. It generates multi-turn transcripts of malicious and benign
actors under controlled conditions, and it scans transcripts to produce
evidence-cited risk assessments.

**The problem?** AI is becoming increasingly capable across dual-use domains
like cyber and bio/CBRNe, with open models offering frontier capabilities with
limited safeguards. Measuring what these systems hand to different actors, and
where safeguards hold or fail, requires conversation data with known
conditions and labels.

**Generate.** The data pipeline produces multi-turn transcripts of malicious
and benign actors at scale, with support for bio-tools and automated red
teaming. Grounded in [SecureBio's BioTIER](https://securebio.org/biotier/)
taxonomy and expert-curated misuse variables, it compiles actor cards, runs
conversations on the [Petri Bloom](https://meridianlabs-ai.github.io/petri_bloom/)
harness, labels metadata and turns with compliance (permit/refuse) and
behavior to compute trajectories over many turns, and grades with judges.
Evaluation conditions for each conversation are set at generation time with
different combinations of ground truth variables, so model behavior can be
traced back to known conditions.

**Scan.** The scanner (embedding filter + LLM + DSPy), built on
[Inspect AI](https://inspect.aisi.org.uk/) and
[Inspect Scout](https://meridianlabs-ai.github.io/inspect_scout/), reads
transcripts and scores against a rubric, with support for prompt optimization
so its assessments improve as it is tuned on more transcripts. It reports an
evidence-cited risk assessment: what the user appears to be pursuing, what
capabilities and commitment they show, and how urgently the session needs
review.

## The benign dataset

[`data/dataset/`](data/dataset/) contains 591 verified benign transcripts in
Inspect `.eval` format (472 train, 119 test), drawn from the ASTRAL 1,000-log
set. The logs cover Related Biology research conversations and the benign
twins of higher-risk routes, filtered to zero jailbreak, zero scope, and
firewall pass. Use it for over-refusal measurement, scanner calibration, and
as a template for the transcript schema.

## Access tiers

ASTRAL follows BioTIER's tiered-access model.

| Tier | Contents | Access |
|---|---|---|
| Related Biology | full roleplay grounding | public, this repo |
| Benign twins | benign control arms of every route | public, this repo |
| CA/BD framework | route ids, families, allowed variable spaces | public, this repo |
| CA/BD malicious roleplay | detailed objectives and framing | vetted researchers |

The public package generates benign and Related Biology transcripts end to
end. Compiling a malicious CA/BD card without the vetted overlay raises
`GroundingAccessError`. Vetted researchers receive the overlay and set
`ASTRAL_GROUNDING_OVERLAY` to its path.

## Install

```bash
git clone https://github.com/jasontang-ai/astral-bio
cd astral-bio
uv venv
source .venv/bin/activate
uv pip install -e '.[dev]'
```

Add the Petri Bloom harness for conversation generation:

```bash
uv pip install -e '.[bloom]'
```

## Quick start

Compile a benign actor card:

```python
from astral import VariableAssignment, make_actor_card

card = make_actor_card(
    side="benign",
    route_id="rb.biochemistry",
    variables=VariableAssignment(
        scientific_capability=3, jailbreak=0, kill_chain=0, intended_scope=0
    ),
    seed=7,
)
```

Run a batch of conversations through the Bloom harness:

```python
from astral.bridge.batch import run_bloom_batch

report = run_bloom_batch("manifest.yaml", out_dir="_runs/batch")
```

Scan eval samples against ground truth:

```python
from inspect_ai.log import read_eval_log

from astral.scanner.run import scan_sample

log = read_eval_log("data/dataset/benign-test.eval")
result = scan_sample(next(iter(log.samples)), model="openrouter/google/gemini-3.5-flash")
```

## Layout

```text
src/astral/
  cards/       actor-card compile, draw, select, grounding
  runtime/     deterministic control and model arm
  bridge/      Petri Bloom adapter: batch, campaign, normalize, pack, trajectories
  qa/          judges, acceptance, realization gates
  scanner/     Inspect Scout stack: rubric, optimize, evidence retrieval
  assets/      pinned ground truth
data/dataset/  the benign public dataset (.eval)
docs/          design registry, architecture, evidence
```

## Verify

```bash
pytest
mypy src
python skills/astral/scripts/check_submission.py --full
```

CI enforces ruff, mypy, pytest, coverage, complexity metrics, and the design
registry in [`docs/design.md`](docs/design.md).

## Contributing and citation

Development standards live in [`CONTRIBUTING.md`](CONTRIBUTING.md) and the
agent contract in [`AGENTS.md`](AGENTS.md). If you use ASTRAL in research,
cite [`CITATION.cff`](CITATION.cff).

## License

MIT. See [`LICENSE`](LICENSE).
