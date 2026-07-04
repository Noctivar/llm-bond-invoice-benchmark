# baseline_02

Prompt variant for Case 01. See [`../prompt_variants.md`](../prompt_variants.md)
for context.

* Attempt code: `attempts/baseline_02/solution.py`
* Evaluation output: `results/baseline_02_eval.txt`
* Ledger row: `metadata/runs.csv` (`baseline_02`)

## Submitted Prompt

> Write a Python function `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)` that returns the total amount a buyer pays for a Treasury bond.
>
> The quoted price can be written in bond format, for example `99-16+`, `101-03`, or `98-31+`.
>
> Save the implementation in one file called `solution.py`.

The submitted prompt is the version recorded in `results/baseline_results.md`. It
matches the generated artifact naming convention because the prompt asks for one
file called `solution.py`, and the saved model output is
`attempts/baseline_02/solution.py`. The shorter version in
`prompts/baseline_prompts.md` is preserved below as an abbreviated repository
record, not as the submitted prompt.

### Abbreviated Prompt Record

> I have a bond quote like `99-16+` and a face value. Write `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)` that gives me what the buyer pays. Keep it simple.

## Model Output Summary

* A `parse_quote` helper splits the quote on `-`, strips a trailing `+` (adding
  `1/64` of a point), and converts the remaining ticks field with
  `int(ticks_str)`, returning `handle + ticks / 32`.
* `invoice_amount` computes the clean value (`price / 100 * face_value`), accrued
  interest with the **correct semiannual** coupon
  (`annual_coupon_rate / 2 * face_value * days_since_coupon /
  days_in_coupon_period`), and returns their sum. The result is not explicitly
  rounded, but the values fall within the evaluator's one-cent tolerance.

## Evaluation Result

**Score: 11/16**

The 11 ordinary quote-format cases pass. The 5 failing cases are the extended
eighths-of-a-32nd forms, from `results/baseline_02_eval.txt`:

| Case            | Quote     |   Expected |     Actual | Result |
| --------------- | --------- | ---------: | ---------: | ------ |
| eighths_99_162  | `99-162`  | 100,750.91 | 105,305.59 | FAIL   |
| eighths_99_161  | `99-161`  | 100,747.00 | 105,274.34 | FAIL   |
| eighths_99_163  | `99-163`  | 100,754.81 | 105,336.84 | FAIL   |
| eighths_98_317  | `98-317`  | 100,121.09 | 109,031.25 | FAIL   |
| eighths_101_035 | `101-035` | 253,020.97 | 255,472.15 | FAIL   |

## Failure or Success Analysis

The single evidenced failure is quote parsing of the extended notation. When the
ticks field has three characters, `int("162")` is read as **162 thirty-seconds**
instead of `16` thirty-seconds plus `2/8` of a thirty-second, inflating the price
and the invoice amount. Correct interpretation: `99-162 = 99 + (16 + 2/8) / 32`.
The prompt never stated that a third digit encodes eighths of a 32nd. No other
failure mode appears in the eval output — the clean-vs-dirty split and the
semiannual coupon are handled correctly.

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
| Score | 11/16 |
