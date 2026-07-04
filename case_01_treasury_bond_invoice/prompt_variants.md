# Prompt Variants for Case 01

## Purpose

These are additional baseline and improved **prompt variants for the same
Treasury bond invoice task** documented in this case study. They are not separate
finance cases — the problem, oracle, evaluator, and 16-case evaluation set are
identical to the headline run. Only the wording and specificity of the prompt
change. The variants test a single question: **does prompt specificity change
correctness on the same evaluation set?**

The headline run (`baseline_01` → `improved_01`) is written up in
[`baseline.md`](baseline.md) and [`improved.md`](improved.md). This file is the
appendix covering the remaining canonical runs. Per-run detail lives in
[`runs/`](runs/).

## Summary Table

Scores are taken directly from the `results/*_eval.txt` outputs and reproduced by
re-running `evaluate_attempt.py`; observations reflect only what those eval
outputs show.

| Run         | Prompt Type | Score | Main Observation                                                     |
| ----------- | ----------- | ----: | ------------------------------------------------------------------- |
| baseline_01 | baseline    | 11/16 | failed extended eighths-of-a-32nd notation (wrong numeric values)   |
| baseline_02 | baseline    | 11/16 | failed extended eighths-of-a-32nd notation (wrong numeric values)   |
| baseline_03 | baseline    | 11/16 | failed extended eighths-of-a-32nd notation (wrong numeric values)   |
| baseline_04 | baseline    | 11/16 | raised `ValueError` on the extended eighths-of-a-32nd cases         |
| baseline_05 | baseline    |  0/16 | raised `ValueError` on every case (`float(quote)` parse failure)    |
| improved_01 | improved    | 16/16 | passed all cases                                                    |
| improved_02 | improved    | 16/16 | passed all cases                                                    |
| improved_03 | improved    | 16/16 | passed all cases                                                    |
| improved_04 | improved    | 16/16 | passed all cases                                                    |
| improved_05 | improved    | 16/16 | passed all cases                                                    |

Per-run write-ups:
[baseline_02](runs/baseline_02.md),
[baseline_03](runs/baseline_03.md),
[baseline_04](runs/baseline_04.md),
[baseline_05](runs/baseline_05.md),
[improved_02](runs/improved_02.md),
[improved_03](runs/improved_03.md),
[improved_04](runs/improved_04.md),
[improved_05](runs/improved_05.md).

## Pattern

The evidenced pattern across the canonical runs:

* **baseline_01 through baseline_04** produced plausible, mostly-correct
  implementations that handled ordinary quote formats, the clean-vs-dirty split,
  and the semiannual coupon, but did **not** handle the **extended
  eighths-of-a-32nd notation** (`99-161`, `99-162`, `99-163`, `98-317`,
  `101-035`). baseline_01–03 returned wrong numeric values for those cases;
  baseline_04 raised `ValueError` on them because its quote regex rejected a
  three-digit ticks field. All four scored 11/16.
* **baseline_05** is the most severe baseline failure in the evidence: its
  generated parser called `float(quote)`, which raises `ValueError` for every
  Treasury-format quote, so it scored 0/16. No case reached the invoice
  calculation.
* **improved_01 through improved_05** each scored 16/16. The shared specification
  they all use states the missing conventions explicitly — most decisively the
  rule that a third digit after the dash denotes eighths of a 32nd (and that `+`
  equals half a 32nd) — which is precisely the convention the baselines lacked.

This supports the case-study thesis: on an identical evaluation set, correctness
tracked whether the prompt specified the Treasury quote conventions, not the
model's raw coding ability.

## Metadata Note

Exact model IDs, request IDs, response IDs, exact timestamps, sampling settings,
and raw model transcripts were **not captured** for the initial prototype. The
run ledger (`metadata/runs.csv`) records only the tool name ("Claude Code"), a
date (`2026-06-30`), the attempt path, and the score. See
[`metadata.md`](metadata.md) for the full disclosure.
