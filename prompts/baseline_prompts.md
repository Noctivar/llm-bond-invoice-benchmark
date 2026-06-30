# Baseline (vague) prompts

These are the **intentionally under-specified** prompts. They describe the task
in the loose, informal way a non-expert might phrase it. They omit the finance
rules (32nds parsing, the `+` half-tick, clean-vs-dirty, semiannual coupon,
rounding to the cent). They are expected to elicit the realistic mistakes that
`cases.json` is designed to catch.

Each prompt should be sent to the model on its own. Save the model's returned
code to the matching `attempts/baseline_NN/attempt.py` file, then score it with:

```
python evaluate_attempt.py attempts/baseline_01/attempt.py
```

Record the run in `metadata/runs.csv` and summarize in `results/baseline_results.md`.

The required function signature for every attempt is:

```python
invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)
```

---

## baseline_01 — bare request

> Write a Python function `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)` that returns the invoice amount for a Treasury bond trade. `quote` looks like `"99-16"`.

## baseline_02 — "just compute the price"

> I have a bond quote like `99-16+` and a face value. Write `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)` that gives me what the buyer pays. Keep it simple.

## baseline_03 — emphasizes the quote, nothing else

> Parse the bond quote string (e.g. `"101-03"`) and return the total amount for
> `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)`. The quote is the price.

## baseline_04 — mentions interest vaguely

> Write `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)`. It should use the price and add the interest. The quote is something like `99-16`.

## baseline_05 — "value the bond"

> Given a coupon rate and a quoted price like `99-16+`, value the bond and return
> the cash amount from `invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)`.
