# Baseline Results

These runs used vague or under-specified prompts. The model was not asked to fail. The failures came from missing fixed-income conventions in the prompt.

| Run | Score | Main Failure |
|---|---:|---|
| Baseline 1 | 11/16 | Failed extended eighths-of-a-32nd Treasury quote cases |
| Baseline 2 | 11/16 | Failed extended eighths-of-a-32nd Treasury quote cases |
| Baseline 3 | 11/16 | Failed extended eighths-of-a-32nd Treasury quote cases |
| Baseline 4 | 11/16 | Raised errors on extended eighths quote cases |
| Baseline 5 | 0/16 | Failed all Treasury quote-format cases |

## Baseline 1

Prompt:
Write a Python function called `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)` that calculates the amount paid for a Treasury bond purchase.

The quote may look like `99-16` or `99-16+`.

Keep the implementation simple and put everything in one file called `solution.py`.

Result:
11/16 passed.

Failure:
The solution handled common quote forms but failed extended eighths-of-a-32nd notation such as `99-162`, `99-161`, `99-163`, `98-317`, and `101-035`.

## Baseline 2

Prompt:
Write a Python function `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)` that returns the total amount a buyer pays for a Treasury bond.

The quoted price can be written in bond format, for example `99-16+`, `101-03`, or `98-31+`.

Save the implementation in one file called `solution.py`.

Result:
11/16 passed.

Failure:
The solution handled common 32nds and plus-tick notation but failed extended fractional 32nd notation.

## Baseline 3

Prompt:
Create a Python fixed-income quote converter.

Write a function `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)`.

It should take a Treasury bond quote such as `99-16+`, `101-03`, or `100-00` and return the total dollar amount paid by the buyer.

Keep it simple and save everything in `solution.py`.

Result:
11/16 passed.

Failure:
The solution handled common quote forms but failed extended eighths-of-a-32nd notation.

## Baseline 4

Prompt:
Build a one-file Python helper for converting Treasury bond quotes into dollar prices.

Write a function:
`invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)`

The quote can look like `99-16`, `99-16+`, or `101-03`.

Return the bond's dollar price for the trade.

Save everything in `solution.py`.

Result:
11/16 passed.

Failure:
The solution raised errors on extended eighths-of-a-32nd quote cases.

## Baseline 5

Prompt:
Write a simple Python function:

`invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)`

It should calculate the total amount paid for a bond trade using the quoted price, coupon rate, and accrued days.

The quote is provided as a string.

Save the implementation in one file called `solution.py`.

Result:
0/16 passed.

Failure:
The prompt did not specify Treasury 32nds notation, so the generated solution could not handle the quote strings at all.

## Conclusion

The vague prompts produced plausible but incorrect finance code. The most common failure was missing the extended eighths-of-a-32nd Treasury quote convention.
