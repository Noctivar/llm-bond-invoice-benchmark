# baseline_04

Prompt variant for Case 01. See [`../prompt_variants.md`](../prompt_variants.md)
for context.

* Attempt code: `attempts/baseline_04/solution.py`
* Evaluation output: `results/baseline_04_eval.txt`
* Ledger row: `metadata/runs.csv` (`baseline_04`)

## Prompt

The repository contains **two slightly different prompt records** for this run.
Both are reproduced verbatim; neither is silently preferred. The results-file
wording is the more likely match to the actual run because it references the
saved output filename `solution.py`.

### Recorded in `prompts/baseline_prompts.md`

> Write `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)`. It should use the price and add the interest. The quote is something like `99-16`.

### Recorded in `results/baseline_results.md`

> Build a one-file Python helper for converting Treasury bond quotes into dollar prices.
>
> Write a function:
> `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)`
>
> The quote can look like `99-16`, `99-16+`, or `101-03`.
>
> Return the bond's dollar price for the trade.
>
> Save everything in `solution.py`.

## Model Output Summary

* A `parse_quote` helper validates the quote against the regular expression
  `^\s*(\d+)-(\d{1,2})(\+?)\s*$` — i.e. a handle, **one or two** tick digits, and
  an optional `+`. Anything else raises `ValueError`. A matched quote yields
  `points + thirty_seconds / 32`, plus `1/64` when the `+` is present.
* `invoice_amount` additionally range-checks the day inputs (raising `ValueError`
  if `days_in_coupon_period <= 0` or `days_since_coupon` is outside
  `0..days_in_coupon_period`), then computes the clean value plus accrued interest
  using the **correct semiannual** coupon.

## Evaluation Result

**Score: 11/16**

The 11 ordinary quote-format cases pass. The 5 failing cases are the extended
eighths-of-a-32nd forms, which fail here as raised errors rather than wrong
numbers, from `results/baseline_04_eval.txt`:

| Case            | Quote     |   Expected |            Actual | Result |
| --------------- | --------- | ---------: | ----------------- | ------ |
| eighths_99_162  | `99-162`  | 100,750.91 | ERROR: ValueError | FAIL   |
| eighths_99_161  | `99-161`  | 100,747.00 | ERROR: ValueError | FAIL   |
| eighths_99_163  | `99-163`  | 100,754.81 | ERROR: ValueError | FAIL   |
| eighths_98_317  | `98-317`  | 100,121.09 | ERROR: ValueError | FAIL   |
| eighths_101_035 | `101-035` | 253,020.97 | ERROR: ValueError | FAIL   |

## Failure or Success Analysis

The single evidenced failure is that the quote regex allows only a one- or
two-digit ticks field, so the three-character forms (`99-162`, `98-317`,
`101-035`, etc.) do not match and `parse_quote` raises `ValueError`. This is the
same missing convention as baseline_01–03 — a third digit denoting eighths of a
32nd — surfacing as an error instead of a wrong value because this
implementation validates its input. The evaluator counts a raised exception as a
failed case (see `evaluate_attempt.py`). Ordinary formats, the clean-vs-dirty
split, and the semiannual coupon are handled correctly; no other failure mode
appears in the eval output.

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

The `metadata/runs.csv` note for this run reads: "Raised ValueError on extended
eighths-of-a-32nd Treasury quote cases."
