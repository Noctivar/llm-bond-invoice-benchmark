# LLM Bond Invoice Benchmark

This project evaluates whether an AI coding agent can correctly implement a small but domain-specific fixed-income calculation. It computes the invoice amount for a Treasury bond from a quoted clean price and accrued interest inputs.

The assignment goal is to compare vague baseline prompts against improved prompts. The baseline prompts produce plausible but incorrect finance code. The improved prompts explicitly specify the missing fixed-income conventions and produce correct results.

This repository is a small **LLM finance benchmark research artifact**. For the
clean, self-contained write-up of the headline result (baseline_01 → improved_01,
11/16 → 16/16), see **[`case_01_treasury_bond_invoice/`](case_01_treasury_bond_invoice/README.md)**.
That case study also includes an
[appendix of prompt variants](case_01_treasury_bond_invoice/prompt_variants.md)
documenting the remaining canonical runs (baseline_02–05, improved_02–05) for the
same Treasury bond invoice task. The `archive_v1/` folder preserves an excluded
orphan run for transparency; see [`archive_v1/NOTES.md`](archive_v1/NOTES.md).

## Problem

Given:

* face value
* annual coupon rate
* Treasury clean price quote
* days since last coupon
* days in coupon period

compute the buyer's invoice amount.

The key finance conventions are:

```text
Treasury quote -> clean price per 100 face value

clean_value = face_value * clean_price / 100

accrued_interest = face_value * annual_coupon_rate / 2
                   * days_since_coupon / days_in_coupon_period

invoice_amount = clean_value + accrued_interest
```

The quote parsing is the main trap. Treasury quotes are not decimal prices.

Examples:

```text
99-16   = 99 + 16/32
99-16+  = 99 + 16.5/32
99-162  = 99 + (16 + 2/8)/32
98-317  = 98 + (31 + 7/8)/32
101-035 = 101 + (3 + 5/8)/32
```

## Why LLMs fail

The 16 cases in `cases.json` are *designed* to catch a range of realistic
fixed-income mistakes (naive decimal parsing of `99-16`, dropping the `+`,
missing eighths-of-a-32nd notation, returning the clean value instead of the
dirty/invoice amount, using the annual instead of the semiannual coupon, or
rounding too early).

In the runs actually recorded here, the **observed** baseline failures were
narrower than that full list:

* baseline_01–baseline_04 correctly handled ordinary quote formats, the
  clean-vs-dirty split, and the semiannual coupon, but **failed the extended
  eighths-of-a-32nd notation** (e.g. `99-162`, `98-317`, `101-035`), scoring
  11/16.
* baseline_05 had a **degenerate parse failure** (`float(quote)` raising
  `ValueError` on every Treasury quote), scoring 0/16.

The other mistakes in the list above are pitfalls the cases guard against, not
failures these particular attempts exhibited.

## Results

| Run        | Prompt Type | Score | Main Result                                   |
| ---------- | ----------: | ----: | --------------------------------------------- |
| Baseline 1 |       Vague | 11/16 | Failed extended eighths-of-a-32nd quote cases |
| Baseline 2 |       Vague | 11/16 | Failed extended eighths-of-a-32nd quote cases |
| Baseline 3 |       Vague | 11/16 | Failed extended eighths-of-a-32nd quote cases |
| Baseline 4 |       Vague | 11/16 | Raised errors on extended eighths quote cases |
| Baseline 5 |       Vague |  0/16 | Failed all Treasury quote-format cases        |
| Improved 1 |      Guided | 16/16 | Passed                                        |
| Improved 2 |      Guided | 16/16 | Passed                                        |
| Improved 3 |      Guided | 16/16 | Passed                                        |
| Improved 4 |      Guided | 16/16 | Passed                                        |
| Improved 5 |      Guided | 16/16 | Passed                                        |

## Project structure

```text
.
├── oracle.py
├── cases.json
├── evaluate_attempt.py
├── case_01_treasury_bond_invoice/   # clean case-study write-up
│   ├── README.md
│   ├── baseline.md
│   ├── improved.md
│   └── metadata.md
├── attempts/
│   ├── baseline_01/
│   ├── baseline_02/
│   ├── baseline_03/
│   ├── baseline_04/
│   ├── baseline_05/
│   ├── improved_01/
│   ├── improved_02/
│   ├── improved_03/
│   ├── improved_04/
│   └── improved_05/
├── prompts/
│   ├── baseline_prompts.md
│   └── improved_prompts.md
├── results/
│   ├── baseline_results.md
│   ├── improved_results.md
│   └── *_eval.txt
├── metadata/
│   └── runs.csv
├── archive_v1/                       # excluded orphan run, kept for transparency
│   ├── NOTES.md
│   └── baseline_05_unexpected_pass/
└── tests/
    └── test_oracle.py
```

## Running the benchmark

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run oracle tests:

```bash
pytest
```

Evaluate one attempt:

```bash
python3 evaluate_attempt.py attempts/baseline_01/solution.py
```

Evaluate all attempts:

```bash
for f in attempts/baseline_01/solution.py attempts/baseline_02/solution.py attempts/baseline_03/solution.py attempts/baseline_04/solution.py attempts/baseline_05/solution.py attempts/improved_01/solution.py attempts/improved_02/solution.py attempts/improved_03/solution.py attempts/improved_04/solution.py attempts/improved_05/solution.py
do
  echo "===== $f ====="
  python3 evaluate_attempt.py "$f" | tail -n 3
done
```

## Takeaway

The baseline prompts were not malicious or deliberately wrong. They were merely underspecified. The failures came from missing fixed-income conventions that are obvious to a domain expert but easy for a general coding agent to omit.

The improved prompts fixed the failures by explicitly specifying Treasury quote notation, clean-vs-dirty price, semiannual coupon accrual, and final cent rounding.
