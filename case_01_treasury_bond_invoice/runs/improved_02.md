# improved_02

Prompt variant for Case 01. See [`../prompt_variants.md`](../prompt_variants.md)
for context.

* Attempt code: `attempts/improved_02/solution.py`
* Evaluation output: `results/improved_02_eval.txt`
* Ledger row: `metadata/runs.csv` (`improved_02`)

## Prompt

The improved prompts have a single record (`prompts/improved_prompts.md`); there
is no conflicting second version. Each improved run prepends the shared
specification — reproduced verbatim in [`../improved.md`](../improved.md) — to a
short run-specific instruction. The run-specific instruction for this run:

> Use the shared specification above. As a check: with `face_value=100_000`,
> `annual_coupon_rate=0.05`, `quote="99-16+"`, `days_since_coupon=90`,
> `days_in_coupon_period=181`, the result must be `100758.72`.

## Model Output Summary

* `parse_quote` reads the first two characters of the ticks field as 32nds, and
  handles the extended forms explicitly: a trailing `+` sets `eighths = 4`, and
  otherwise a third character sets `eighths = int(frac_str[2])`. The price is
  `points + (thirty_seconds + eighths / 8) / 32`.
* `invoice_amount` returns the clean value plus semiannual accrued interest,
  `round(..., 2)`.

## Evaluation Result

**Score: 16/16**

All 16 cases passed, including every extended eighths-of-a-32nd case (`99-161`,
`99-162`, `99-163`, `98-317`, `101-035`) that the baselines failed.

## Failure or Success Analysis

The pass is attributable to the shared specification stating the missing
convention outright: a third digit after the dash denotes eighths of a 32nd, and
`+` equals half a 32nd (four eighths). That is exactly the rule baseline_01–04
lacked, and the solution encodes it directly. The worked numeric example in this
variant's instruction (`99-16+` → `100758.72`) provides an additional correctness
check, but the extended-notation cases pass because of the eighths rule in the
shared spec, not the single `+` example.

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
