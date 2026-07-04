# Baseline Run

## Run Selected

`baseline_01`

* Attempt code: `attempts/baseline_01/solution.py`
* Evaluation output: `results/baseline_01_eval.txt`
* Ledger row: `metadata/runs.csv` (`baseline_01`)

## Submitted Prompt

> Write a Python function called `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)` that calculates the amount paid for a Treasury bond purchase.
>
> The quote may look like `99-16` or `99-16+`.
>
> Keep the implementation simple and put everything in one file called `solution.py`.

The submitted prompt is the version recorded in `results/baseline_results.md`. It
matches the generated artifact naming convention because the prompt asks for one
file called `solution.py`, and the saved model output is
`attempts/baseline_01/solution.py`. The shorter version in
`prompts/baseline_prompts.md` is preserved below as an abbreviated repository
record, not as the submitted prompt.

### Abbreviated Prompt Record

> Write a Python function `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)` that returns the invoice amount for a Treasury bond trade. `quote` looks like `"99-16"`.

## Model Output Summary

The produced `solution.py` (plain English):

* Defines a `_parse_quote` helper that splits the quote on `-` into a handle and
  a ticks field, strips a trailing `+` (adding `1/64`), converts the ticks with
  `int(ticks_str)`, and computes `handle + ticks/32`.
* In `invoice_amount`, converts the parsed price to a clean value
  (`face_value * price / 100`), computes accrued interest using the **correct
  semiannual** coupon (`face_value * annual_coupon_rate / 2 * days_since_coupon
  / days_in_coupon_period`), and returns `clean_value + accrued_interest`.

Notably, the baseline got the clean-vs-dirty split and the semiannual coupon
**right**. The single defect is in quote parsing.

## Evaluation Result

**Score: 11/16**

The 11 passing cases cover ordinary quote formats (plain 32nds like `99-16`,
`+` half-ticks like `99-16+`, low ticks like `101-03`, par `100-00`, boundary
`98-31+`, and various face values). The 5 failing cases are all the extended
eighths-of-a-32nd forms. Concrete failures from `results/baseline_01_eval.txt`:

| Case            | Quote     |   Expected |     Actual | Result |
| --------------- | --------- | ---------: | ---------: | ------ |
| eighths_99_162  | `99-162`  | 100,750.91 | 105,305.59 | FAIL   |
| eighths_99_161  | `99-161`  | 100,747.00 | 105,274.34 | FAIL   |
| eighths_99_163  | `99-163`  | 100,754.81 | 105,336.84 | FAIL   |
| eighths_98_317  | `98-317`  | 100,121.09 | 109,031.25 | FAIL   |
| eighths_101_035 | `101-035` | 253,020.97 | 255,472.15 | FAIL   |

The model handled ordinary quote formats but failed extended
eighths-of-a-32nd notation.

## Failure Analysis

* The baseline implementation was **syntactically plausible** and ran without
  errors on every case.
* It **handled common Treasury quote formats** correctly (11/16).
* It **failed subtle extended notation** such as `99-162` and `98-317`. When the
  ticks field has three characters, `int("162")` is read as **162 thirty-seconds**
  instead of `16` thirty-seconds plus `2/8` of a thirty-second, inflating the
  price and the invoice amount.
* Correct interpretation example:
  `99-162 = 99 + (16 + 2/8) / 32`.
* The failure is **finance-specific**: the missing knowledge is not Python
  syntax but the Treasury market quote convention for eighths of a 32nd. The
  model was never told the third digit exists, so it parsed the whole ticks
  field as a single integer.

Note on scope: a separate run, `baseline_05`, produced a **degenerate parse
failure** (0/16) because its prompt gave no quote-format guidance at all and the
generated code called `float(quote)`, raising `ValueError` on every Treasury
quote. That run is not the headline here; the representative baseline failure is
the extended-notation parsing gap shown above.

## What This Shows

A general coding prompt can produce code that appears correct — and is correct
for the common cases — while missing domain-specific financial conventions that
only surface on the harder quote formats.
