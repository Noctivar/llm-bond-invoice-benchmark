# baseline_03

Prompt variant for Case 01. See [`../prompt_variants.md`](../prompt_variants.md)
for context.

* Attempt code: `attempts/baseline_03/solution.py`
* Evaluation output: `results/baseline_03_eval.txt`
* Ledger row: `metadata/runs.csv` (`baseline_03`)

## Prompt

The repository contains **two slightly different prompt records** for this run.
Both are reproduced verbatim; neither is silently preferred. The results-file
wording is the more likely match to the actual run because it references the
saved output filename `solution.py`.

### Recorded in `prompts/baseline_prompts.md`

> Parse the bond quote string (e.g. `"101-03"`) and return the total amount for `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)`. The quote is the price.

### Recorded in `results/baseline_results.md`

> Create a Python fixed-income quote converter.
>
> Write a function `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)`.
>
> It should take a Treasury bond quote such as `99-16+`, `101-03`, or `100-00` and return the total dollar amount paid by the buyer.
>
> Keep it simple and save everything in `solution.py`.

## Model Output Summary

* A `parse_quote` helper partitions the quote on `-`, strips a trailing `+`
  (adding half a tick), and converts the remaining ticks with `int(ticks_str)`,
  returning `handle + ticks / 32`.
* `invoice_amount` computes the clean value (`face_value * price / 100`), accrued
  interest with the **correct semiannual** coupon
  (`face_value * annual_coupon_rate / 2 * days_since_coupon /
  days_in_coupon_period`), and returns their sum. No explicit rounding; values
  stay within the one-cent tolerance.

## Evaluation Result

**Score: 11/16**

The 11 ordinary quote-format cases pass. The 5 failing cases are the extended
eighths-of-a-32nd forms, from `results/baseline_03_eval.txt`:

| Case            | Quote     |   Expected |     Actual | Result |
| --------------- | --------- | ---------: | ---------: | ------ |
| eighths_99_162  | `99-162`  | 100,750.91 | 105,305.59 | FAIL   |
| eighths_99_161  | `99-161`  | 100,747.00 | 105,274.34 | FAIL   |
| eighths_99_163  | `99-163`  | 100,754.81 | 105,336.84 | FAIL   |
| eighths_98_317  | `98-317`  | 100,121.09 | 109,031.25 | FAIL   |
| eighths_101_035 | `101-035` | 253,020.97 | 255,472.15 | FAIL   |

## Failure or Success Analysis

The single evidenced failure is the extended-notation parse: `int("162")` is
treated as **162 thirty-seconds** instead of `16 + 2/8` thirty-seconds, so the
five three-character-ticks cases return inflated amounts. Correct interpretation:
`99-162 = 99 + (16 + 2/8) / 32`. The prompt did not mention the eighths-of-a-32nd
convention. The eval output shows no other failure mode; ordinary formats, the
clean-vs-dirty split, and the semiannual coupon are correct.

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
