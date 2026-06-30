# Treasury Bond Invoice Benchmark

A small, deterministic benchmark that demonstrates how **prompt quality affects
the correctness of LLM-generated finance code**. The task: compute the *invoice
amount* (a.k.a. dirty value) of a U.S. Treasury bond trade from a 32nds price
quote, a coupon rate, and an accrued-interest day count.

Vague prompts tend to produce code with predictable, realistic mistakes (parsing
`99-16` as `99.16`, dropping the `+`, returning the clean value, forgetting
accrued interest, using the annual coupon, mis-rounding, or pricing from yield).
Improved prompts that state the finance rules explicitly produce code that passes.
The grader, test cases, and tolerance are held constant — **only the prompt
changes** — so the score gap is attributable to prompt quality.

## The finance problem

Given:

- `face_value` — par value of the position (e.g. `100_000`)
- `annual_coupon_rate` — decimal annual coupon (`0.05` == 5%)
- `quote` — a Treasury 32nds price string (`"99-16"`, `"99-16+"`, `"101-03"`)
- `days_since_coupon` — days elapsed in the current coupon period
- `days_in_coupon_period` — total days in the current coupon period

Compute the invoice amount with these rules:

1. **Quotes are in 32nds of a point.**
   - `99-16`  = `99 + 16/32`
   - `99-16+` = `99 + 16.5/32`  (a trailing `+` adds half a 32nd)
   - `101-03` = `101 + 3/32`
2. The quote is a **clean price per 100 of face value**.
3. `clean_value = face_value * clean_price_decimal / 100`
4. `accrued_interest = face_value * annual_coupon_rate / 2 * days_since_coupon / days_in_coupon_period`
   (the `/ 2` is because Treasury coupons pay **semiannually**)
5. `invoice_amount = clean_value + accrued_interest`, rounded to the nearest cent.

## Repository layout

```
oracle.py                     Reference correct implementation + quote parser
cases.json                    12 deterministic test cases (expected values from the oracle)
evaluate_attempt.py           Scores any attempt file against cases.json
tests/test_oracle.py          Pytest unit tests for the oracle (24 tests)
prompts/baseline_prompts.md   Vague prompts (expected to fail)
prompts/improved_prompts.md   Clear, rule-stating prompts (expected to pass)
results/baseline_results.md   Scoreboard template for baseline runs
results/improved_results.md   Scoreboard template for improved runs
metadata/runs.csv             One row per evaluated attempt (provenance + score)
attempts/<run_id>/            Where attempt.py files go (not generated yet)
requirements.txt              pytest (everything else is stdlib)
```

## The contract an attempt must satisfy

Each attempt is a Python file that defines exactly:

```python
def invoice_amount(face_value, annual_coupon_rate, quote,
                   days_since_coupon, days_in_coupon_period):
    ...
```

It must return the invoice amount as a number.

## Usage

Install the (single) test dependency:

```bash
pip install -r requirements.txt
```

Run the oracle's own tests:

```bash
pytest -q
```

Score an attempt against the cases:

```bash
python evaluate_attempt.py attempts/baseline_01/attempt.py
```

The evaluator prints each case (inputs, expected, actual, PASS/FAIL) and an
overall score. A case passes when the answer is within **one cent** of the
oracle. Exit code is `0` only when all cases pass.

You can sanity-check the harness by scoring the oracle itself (it satisfies the
contract and scores 12/12):

```bash
python evaluate_attempt.py oracle.py
```

## What each case targets

`cases.json` is built so that the common natural mistakes each fail at least one
case:

| Mistake                                              | Caught by (examples)                       |
|------------------------------------------------------|--------------------------------------------|
| Parsing `99-16` as `99.16`                           | `basic_99_16`, `decimal_trap_101_03`       |
| Ignoring the trailing `+`                            | `plus_tick_99_16p`, `near_boundary_98_31p` |
| Returning clean value instead of dirty/invoice value | every case with `days_since_coupon > 0`    |
| Forgetting accrued interest                          | `par_100_00`, `full_period_accrued`        |
| Using annual coupon instead of semiannual            | `high_coupon_10`, `full_period_accrued`    |
| Incorrect rounding                                   | `small_face_1k`, `big_face_1mm`            |
| Confusing quoted clean price with yield-based pricing| `basic_99_16` and all (quote is used directly) |

The `zero_accrued` case (where `days_since_coupon == 0`) is the one case where
clean == dirty; it guards against an attempt that *only* ever works when accrued
is zero.

## Workflow for the screening exercise

1. Send each prompt in `prompts/baseline_prompts.md` to the model; save the
   returned code to `attempts/baseline_NN/attempt.py`.
2. Do the same for `prompts/improved_prompts.md` into `attempts/improved_NN/`.
3. Score every attempt with `evaluate_attempt.py`.
4. Record one row per run in `metadata/runs.csv` and summarize the scoreboards in
   `results/baseline_results.md` and `results/improved_results.md`.

> Note: this repo intentionally ships **no attempt solutions** — neither correct
> nor deliberately wrong. The oracle is the ground truth; the evaluator is fair
> and simply catches realistic mistakes. Generate the attempts from the prompts.
