# Improved (clear) prompts

These prompts state the finance rules explicitly. They are designed to elicit
**correct** code by removing the ambiguity that produces the baseline mistakes.
The grader, cases, and tolerance are identical to the baseline — only the prompt
changes — so any score difference is attributable to prompt quality.

Save each model response to `attempts/improved_NN/attempt.py` and score with:

```
python evaluate_attempt.py attempts/improved_01/attempt.py
```

Record the run in `metadata/runs.csv` and summarize in `results/improved_results.md`.

The required function signature for every attempt is:

```python
invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period)
```

---

## Shared specification (prepend to every improved prompt)

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

---

## improved_01 — full spec, terse

> Use the shared specification above. Implement `invoice_amount(...)` and nothing else.

## improved_02 — full spec + worked example

> Use the shared specification above. As a check: with `face_value=100_000`,
> `annual_coupon_rate=0.05`, `quote="99-16+"`, `days_since_coupon=90`,
> `days_in_coupon_period=181`, the result must be `100758.72`.

## improved_03 — full spec, asks for a quote parser helper

> Use the shared specification above. Write a small helper that converts the 32nds
> quote string (handling the trailing `+`) into a decimal price, then use it inside
> `invoice_amount(...)`.

## improved_04 — full spec, names the pitfalls

> Use the shared specification above. Be careful to: (a) not parse the quote as a
> decimal, (b) not drop the `+`, (c) return the dirty/invoice value not the clean
> value, (d) use the **semiannual** (half-year) coupon for accrued interest, and
> (e) round to the cent.

## improved_05 — full spec, restates clean vs dirty

> Use the shared specification above. Remember the invoice/dirty amount is the
> clean (quoted) value **plus** accrued interest — never the clean value alone.
