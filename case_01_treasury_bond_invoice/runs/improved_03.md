# improved_03

Prompt variant for Case 01. See [`../prompt_variants.md`](../prompt_variants.md)
for context.

* Attempt code: `attempts/improved_03/solution.py`
* Evaluation output: `results/improved_03_eval.txt`
* Ledger row: `metadata/runs.csv` (`improved_03`)

## Prompt

The improved prompts have a single record (`prompts/improved_prompts.md`); there
is no conflicting second version. Each improved run prepends the shared
specification — reproduced verbatim in [`../improved.md`](../improved.md) — to a
short run-specific instruction. The run-specific instruction for this run:

> Use the shared specification above. Write a small helper that converts the 32nds
> quote string (handling the trailing `+`) into a decimal price, then use it inside
> `invoice_amount(...)`.

## Model Output Summary

* A `parse_quote` helper reads the first two ticks characters as 32nds, then
  inspects any tail: `"+"` maps to `eighths = 4`, otherwise the tail digit maps to
  `eighths = int(tail)`. The price is `whole + (thirty_seconds + eighths / 8) / 32`.
* `invoice_amount` returns the clean value plus semiannual accrued interest,
  `round(..., 2)`.

## Evaluation Result

**Score: 16/16**

All 16 cases passed, including the extended eighths-of-a-32nd cases the baselines
failed.

## Failure or Success Analysis

The pass is attributable to the shared specification's explicit eighths-of-a-32nd
rule, which this solution's helper implements. This variant additionally asked
for a dedicated quote-parsing helper; that is an organizational instruction and
the solution does isolate parsing in `parse_quote`, but correctness on the
extended cases comes from the convention being specified, not from the helper
structure itself.

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
