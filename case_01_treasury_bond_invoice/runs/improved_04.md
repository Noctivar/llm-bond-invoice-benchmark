# improved_04

Prompt variant for Case 01. See [`../prompt_variants.md`](../prompt_variants.md)
for context.

* Attempt code: `attempts/improved_04/solution.py`
* Evaluation output: `results/improved_04_eval.txt`
* Ledger row: `metadata/runs.csv` (`improved_04`)

## Prompt

The improved prompts have a single record (`prompts/improved_prompts.md`); there
is no conflicting second version. Each improved run prepends the shared
specification — reproduced verbatim in [`../improved.md`](../improved.md) — to a
short run-specific instruction. The run-specific instruction for this run:

> Use the shared specification above. Be careful to: (a) not parse the quote as a
> decimal, (b) not drop the `+`, (c) return the dirty/invoice value not the clean
> value, (d) use the **semiannual** (half-year) coupon for accrued interest, and
> (e) round to the cent.

## Model Output Summary

* `invoice_amount` parses the quote inline: a trailing `+` gives
  `int(frac_str[:-1]) + 0.5` thirty-seconds; a three-character ticks field gives
  `int(frac_str[:2]) + int(frac_str[2]) / 8` thirty-seconds; otherwise
  `int(frac_str)`. The clean price is `whole + thirty_seconds / 32`.
* It returns the clean value plus semiannual accrued interest, `round(..., 2)`.

## Evaluation Result

**Score: 16/16**

All 16 cases passed, including the extended eighths-of-a-32nd cases the baselines
failed.

## Failure or Success Analysis

The pass is attributable to the shared specification's eighths-of-a-32nd rule,
which the inline parser implements (the three-character branch). This variant
also enumerated the specific pitfalls (no decimal parse, keep the `+`, return
dirty not clean, use the semiannual coupon, round to the cent); those match the
conventions the baselines had to infer. The decisive addition relative to the
baselines is the explicit eighths handling — the other listed pitfalls
(clean-vs-dirty, semiannual coupon) were already handled correctly by
baseline_01–04.

## Metadata

| Field | Value |
| --- | --- |
| Model | not captured |
| Tool | Claude Code (from `metadata/runs.csv`) |
| Date | 2026-06-30 (exact time not captured) |
| Request ID | not captured |
| Response ID | not captured |
| Temperature / settings | not captured |
| Raw transcript | not captured |
| Score | 16/16 |
