# Baseline results

Scores for the vague-prompt attempts. Fill this in after running each attempt
through the evaluator. (Attempt solutions are **not** included in this repo yet —
generate them from `prompts/baseline_prompts.md`.)

To produce a row:

```
python evaluate_attempt.py attempts/baseline_01/attempt.py
```

## Summary

| run_id      | prompt | model | tests_passed | tests_total | score | notes |
|-------------|--------|-------|--------------|-------------|-------|-------|
| baseline_01 | 1      |       | _TBD_        | 12          |       |       |
| baseline_02 | 2      |       | _TBD_        | 12          |       |       |
| baseline_03 | 3      |       | _TBD_        | 12          |       |       |
| baseline_04 | 4      |       | _TBD_        | 12          |       |       |
| baseline_05 | 5      |       | _TBD_        | 12          |       |       |

## Observed failure modes

Note which of the targeted mistakes each attempt exhibited:

- [ ] Parsed `99-16` as the decimal `99.16`
- [ ] Ignored the trailing `+`
- [ ] Returned the clean value instead of the dirty/invoice value
- [ ] Forgot accrued interest entirely
- [ ] Used the annual coupon instead of the semiannual coupon
- [ ] Rounded incorrectly (or not to the cent)
- [ ] Confused the quoted clean price with yield-based bond pricing

## Per-attempt notes

### baseline_01
_paste evaluator output / observations here_

### baseline_02

### baseline_03

### baseline_04

### baseline_05

## Baseline 1

Prompt:
Write a Python function called invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period) that calculates the amount paid for a Treasury bond purchase.

The quote may look like 99-16 or 99-16+.

Keep the implementation simple and put everything in one file called solution.py.

Result:
Failed 1 of 12 deterministic evaluator cases.

Score:
11/12 passed.

Failure:
- Failed eighths_99_162.
- Expected 100,750.91 but returned 105,305.59.
- The vague prompt did not specify fractional 32nd quote suffixes beyond "+", so the model mishandled the quote format.

Conclusion:
Baseline prompt produced plausible but incorrect finance code.

## Baseline 2

Prompt:
Write a Python function invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period) that returns the total amount a buyer pays for a Treasury bond.

The quoted price can be written in bond format, for example 99-16+, 101-03, or 98-31+.

Save the implementation in one file called solution.py.

Result:
Failed 1 of 12 deterministic evaluator cases.

Score:
11/12 passed.

Failure:
- Failed eighths_99_162.
- Expected 100,750.91 but returned 105,305.59.
- The model handled common 32nds and plus-tick notation but failed extended fractional 32nd notation.

Conclusion:
Baseline prompt produced plausible but incomplete finance code.

## Baseline 3

Prompt:
Create a Python fixed-income quote converter.

Write a function invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period).

It should take a Treasury bond quote such as 99-16+, 101-03, or 100-00 and return the total dollar amount paid by the buyer.

Keep it simple and save everything in solution.py.

Result:
Failed 1 of 12 deterministic evaluator cases.

Score:
11/12 passed.

Failure:
- Failed eighths_99_162.
- Expected 100,750.91 but returned 105,305.59.
- The model handled common quote forms but failed the extended fractional 32nd notation.

Conclusion:
Baseline prompt produced plausible but incomplete finance code.

## Baseline 4

Prompt:
Build a one-file Python helper for converting Treasury bond quotes into dollar prices.

Write a function:
invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)

The quote can look like 99-16, 99-16+, or 101-03.

Return the bond's dollar price for the trade.

Save everything in solution.py.

Result:
Failed 5 of 16 deterministic evaluator cases.

Score:
11/16 passed.

Failure:
- Failed all extended eighths-of-a-32nd quote cases.
- Produced ValueError on 99-162, 99-161, 99-163, 98-317, and 101-035.
- The vague prompt specified common quote examples but did not explain fractional 32nd suffix notation.

Conclusion:
Baseline prompt produced plausible but incomplete finance code.

## Baseline 5A — Unexpected Pass

Prompt:
Implement a simple Treasury bond pricing calculator in Python.

Inputs:
- face_value
- annual_coupon_rate
- quote
- days_since_coupon
- days_in_coupon_period

The main function should be:
invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)

It should parse quotes like 99-16+ and return the final price. Put the implementation in solution.py.

Result:
Passed all 16 deterministic evaluator cases.

Score:
16/16 passed.

Decision:
Excluded from the failed-baseline set because the screening assignment asks for baseline prompts that produce incorrect results. This run was kept as an unexpected-pass observation.

## Baseline 5B

Prompt:
Write a simple Python function:

invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)

It should calculate the total amount paid for a bond trade using the quoted price, coupon rate, and accrued days.

The quote is provided as a string.

Save the implementation in one file called solution.py.

Result:
Failed all 16 deterministic evaluator cases.

Score:
0/16 passed.

Failure:
- Raised ValueError for every Treasury quote case.
- The vague prompt did not specify that quoted price strings use Treasury 32nds notation such as 99-16, 99-16+, or 99-162.
- The model produced code that could not handle the domain-specific quote format.

Conclusion:
The baseline prompt was too underspecified for Treasury quote conventions and produced unusable finance code.
