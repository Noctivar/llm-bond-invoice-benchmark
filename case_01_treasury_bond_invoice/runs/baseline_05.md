# baseline_05

Prompt variant for Case 01. See [`../prompt_variants.md`](../prompt_variants.md)
for context. This is the most severe baseline failure in the canonical set.

* Attempt code: `attempts/baseline_05/solution.py`
* Evaluation output: `results/baseline_05_eval.txt`
* Ledger row: `metadata/runs.csv` (`baseline_05`)

## Submitted Prompt

> Write a simple Python function:
>
> `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)`
>
> It should calculate the total amount paid for a bond trade using the quoted price, coupon rate, and accrued days.
>
> The quote is provided as a string.
>
> Save the implementation in one file called `solution.py`.

The submitted prompt is the version recorded in `results/baseline_results.md`. It
matches the generated artifact naming convention because the prompt asks for one
file called `solution.py`, and the saved model output is
`attempts/baseline_05/solution.py`. The shorter version in
`prompts/baseline_prompts.md` is preserved below as an abbreviated repository
record, not as the submitted prompt.

### Abbreviated Prompt Record

> Given a coupon rate and a quoted price like `99-16+`, value the bond and return the cash amount from `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)`.

## Model Output Summary

* `invoice_amount` treats the quote as an ordinary decimal string: it computes
  `clean_price = (float(quote) / 100.0) * face_value`. Its docstring states it
  expects a quote like `"99.5"` (99.5% of par), i.e. it does not implement the
  Treasury 32nds format at all.
* It then adds accrued interest computed from the **annual** coupon
  (`period_coupon = face_value * annual_coupon_rate`, with no division by two).
  This differs from the semiannual convention, but that line is never reached
  during evaluation because `float(quote)` raises first (see below).

## Evaluation Result

**Score: 0/16**

Every case fails with a `ValueError`. Representative rows from
`results/baseline_05_eval.txt`:

| Case            | Quote    |   Expected |            Actual | Result |
| --------------- | -------- | ---------: | ----------------- | ------ |
| basic_99_16     | `99-16`  | 100,743.09 | ERROR: ValueError | FAIL   |
| plus_tick_99_16p| `99-16+` | 100,758.72 | ERROR: ValueError | FAIL   |
| decimal_trap_101_03 | `101-03` | 101,745.92 | ERROR: ValueError | FAIL |

All 16 cases produce `ERROR: ValueError`.

## Failure or Success Analysis

The single evidenced failure is that `float("99-16")` (and every other
Treasury-format quote in `cases.json`) raises `ValueError`, so no case reaches
the invoice calculation and the run scores 0/16. The prompt gave no
quote-format guidance, and the generated code assumed a plain decimal quote
string. The annual-vs-semiannual coupon discrepancy noted above is visible in the
source but is **not** an evidenced evaluation failure, because parsing fails
before that code runs — it is reported here only as a description of the saved
solution, not as an observed eval result.

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
| Score | 0/16 |

The `metadata/runs.csv` note for this run reads: "Vague quote-string prompt
failed all Treasury quote-format cases." A separate, undocumented run in which a
baseline-style prompt unexpectedly produced a fully correct parser is preserved
outside the case study in [`../../archive_v1/NOTES.md`](../../archive_v1/NOTES.md).
