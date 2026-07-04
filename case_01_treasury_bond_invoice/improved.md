# Improved Run

## Run Selected

`improved_01`

* Attempt code: `attempts/improved_01/solution.py`
* Evaluation output: `results/improved_01_eval.txt`
* Ledger row: `metadata/runs.csv` (`improved_01`)

## User Prompt

The improved prompt is a shared, convention-aware specification (prepended to
every improved run) plus a short run-specific instruction. Both are reproduced
verbatim from `prompts/improved_prompts.md`.

### Shared specification (prepended to every improved prompt)

> Write a Python function:
>
> ```python
> def invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period):
>     ...
> ```
>
> Follow these finance rules exactly:
>
> 1. **Quotes are in 32nds of a point**, given as a string `"handle-ticks"`:
>    - `"99-16"`  means `99 + 16/32`
>    - `"99-16+"` means `99 + 16.5/32` (a trailing `+` adds **half** a 32nd)
>    - `"101-03"` means `101 + 3/32`
>    Do **not** read the quote as a decimal number; `"101-03"` is **not** `101.03`.
> 2. The quote is a **clean price per 100 of face value**.
> 3. `clean_value = face_value * clean_price_decimal / 100`
> 4. Treasury coupons pay **semiannually**, so
>    `accrued_interest = face_value * annual_coupon_rate / 2 * days_since_coupon / days_in_coupon_period`.
>    `annual_coupon_rate` is a decimal (`0.05` == 5%).
> 5. The **invoice amount (dirty value)** = `clean_value + accrued_interest`.
> 6. Round the final result to the nearest cent (2 decimals).
>
> Return the invoice amount as a number. Do not price the bond from yield; use the
> quoted clean price directly.

### improved_01 — full spec, terse

> Use the shared specification above. Implement `invoice_amount(...)` and nothing else.

## Model Output Summary

The produced `solution.py` (plain English):

* Uses `Decimal` throughout to avoid binary floating-point drift.
* Defines a `_parse_quote` helper that splits on `-`, reads the first two
  characters of the ticks field as 32nds, and then handles the extended forms:
  a trailing `+` adds `0.5` of a 32nd, and a trailing digit adds that digit's
  **eighths of a 32nd** (`Decimal(extra) / 8`). This is the exact convention the
  baseline missed.
* Computes `clean_value = face_value * clean_price / 100` and
  `accrued_interest = face_value * annual_coupon_rate / 2 * days_since_coupon /
  days_in_coupon_period`.
* Returns `clean_value + accrued_interest` **rounded to the cent** with
  `quantize(Decimal("0.01"), ROUND_HALF_UP)`.

## Evaluation Result

**Score: 16/16**

The improved solution passed all 16 evaluation cases, including every extended
eighths-of-a-32nd case (`99-161`, `99-162`, `99-163`, `98-317`, `101-035`) that
the baseline failed.

## Improvements Over Baseline

The improved prompt clarified the conventions the baseline prompt left implicit:

* Treasury quotes are in **32nds** of a point, not decimals.
* A trailing **`+`** represents **half of a 32nd**.
* The **third digit after the dash** represents **eighths of a 32nd** — the
  specific rule the baseline prompt never stated.
* The invoice amount uses **clean value plus accrued interest**, with the
  **semiannual** coupon.
* The final output is **rounded to the nearest cent**, which aligns cleanly with
  the evaluator's one-cent tolerance.

## Key Difference

The improved prompt did not merely ask for generic code. It specified the
missing finance conventions in natural language — especially the eighths-of-a-32nd
rule — allowing the LLM to produce a correct implementation. The grader, cases,
and tolerance were identical to the baseline, so the jump from 11/16 to 16/16 is
attributable entirely to the added domain specification.
