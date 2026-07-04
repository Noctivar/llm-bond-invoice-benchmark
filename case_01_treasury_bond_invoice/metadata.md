# Metadata

| Run         | Model        | Tool        | Date/Time                           | Prompt Type | Score | Notes                                   |
| ----------- | ------------ | ----------- | ----------------------------------- | ----------- | ----: | --------------------------------------- |
| baseline_01 | not captured | Claude Code | 2026-06-30, exact time not captured | baseline    | 11/16 | failed extended Treasury quote notation |
| improved_01 | not captured | Claude Code | 2026-06-30, exact time not captured | improved    | 16/16 | passed all evaluation cases             |

The `Model` column is recorded as "not captured" because the run ledger
(`metadata/runs.csv`) only records the tool name "Claude Code", not a specific
model identifier or version.

## Captured Evidence

* Saved generated code in `attempts/` (`attempts/baseline_01/solution.py`,
  `attempts/improved_01/solution.py`).
* Evaluation cases in `cases.json` (16 deterministic cases).
* Evaluator in `evaluate_attempt.py` (one-cent pass tolerance).
* Oracle / reference implementation in `oracle.py`.
* Per-run evaluation outputs in `results/` (`results/baseline_01_eval.txt`,
  `results/improved_01_eval.txt`).
* Run ledger in `metadata/runs.csv`.
* `pytest` result reproduced during the audit: **29 passed**.
* Attempt scores reproduced during the audit by re-running the evaluator
  (baseline_01 = 11/16, improved_01 = 16/16).

## Missing Metadata

Request IDs, response IDs, exact model version, temperature/settings, exact
timestamps, and raw model transcripts were not captured in the initial
prototype. Future cases should log model name, timestamp, prompt version,
request ID, response ID, temperature/settings if available, raw model output,
and evaluation score.

## Prompt Record Limitation

The audit found that this repository contains **two slightly different baseline
prompt records** for `baseline_01` — one in `prompts/baseline_prompts.md` and a
differently worded one in `results/baseline_results.md`. The case study
**preserves both prompt records** (see `baseline.md`) rather than silently
choosing one. The results-file wording is the more likely match to the actual
run because it references the saved output filename `solution.py`, but this was
not fully reconciled and is disclosed as a limitation rather than resolved by
invention.
