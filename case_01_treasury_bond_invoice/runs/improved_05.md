# improved_05

Prompt variant for Case 01. See [`../prompt_variants.md`](../prompt_variants.md)
for context.

* Attempt code: `attempts/improved_05/solution.py`
* Evaluation output: `results/improved_05_eval.txt`
* Ledger row: `metadata/runs.csv` (`improved_05`)

## Prompt

The improved prompts have a single record (`prompts/improved_prompts.md`); there
is no conflicting second version. Each improved run prepends the shared
specification — reproduced verbatim in [`../improved.md`](../improved.md) — to a
short run-specific instruction. The run-specific instruction for this run:

> Use the shared specification above. Remember the invoice/dirty amount is the
> clean (quoted) value **plus** accrued interest — never the clean value alone.

## Model Output Summary

* A `_parse_quote` helper reads the first two ticks characters as 32nds; a third
  character sets `eighths = int(frac_str[2])`, and a trailing `+` overrides
  `eighths = 4`. The price is `whole + (thirty_seconds + eighths / 8) / 32`.
* `invoice_amount` returns the clean value plus semiannual accrued interest,
  `round(..., 2)`.

## Evaluation Result

**Score: 16/16**

All 16 cases passed, including the extended eighths-of-a-32nd cases the baselines
failed.

## Failure or Success Analysis

The pass is attributable to the shared specification's explicit eighths-of-a-32nd
rule, which the helper implements. This variant's added instruction restates that
the invoice amount is clean value **plus** accrued interest. Notably, the
baselines already returned clean-plus-accrued correctly, so that restatement did
not address an observed baseline failure; the extended-notation cases pass here
because of the eighths convention supplied by the shared spec. This is called out
to avoid attributing the improvement to a clarification that the evidence does not
support.

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
