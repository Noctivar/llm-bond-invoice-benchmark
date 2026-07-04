# Case 01: Treasury Bond Invoice Calculation

**Result: an underspecified prompt scored 11/16; a convention-aware prompt scored 16/16 on the same 16-case evaluator — only the prompt changed (`baseline_01` → `improved_01`).**

## Research Question

Can an LLM correctly implement a Treasury bond invoice calculation from quoted
Treasury prices and accrued interest inputs?

## Why This Case Matters

Treasury bond prices are not ordinary decimal numbers. They use market-specific
conventions that a general-purpose coding agent may not infer from a vague
prompt:

* Prices are quoted in **32nds of a point**, written as `handle-ticks`
  (`99-16` means `99 + 16/32`, **not** `99.16`).
* A trailing **`+`** represents **half of a 32nd** (`99-16+` means `99 + 16.5/32`).
* A **third digit after the dash** can represent **eighths of a 32nd**
  (`99-162` means `99 + (16 + 2/8) / 32`).
* The **invoice amount** the buyer pays is the **clean price plus accrued
  interest**, where accrued interest uses the **semiannual** coupon.

These conventions are obvious to a fixed-income practitioner but easy for a
general coding model to omit. That is exactly what this case measures.

## Before/After Summary

| Run         |      Prompt Type | Score | Main Result                                                                |
| ----------- | ---------------: | ----: | -------------------------------------------------------------------------- |
| baseline_01 |   underspecified | 11/16 | passed common quote formats but failed extended eighths-of-a-32nd notation |
| improved_01 | convention-aware | 16/16 | passed all evaluation cases                                                |

Both runs were graded by the same evaluator (`evaluate_attempt.py`) against the
same 16 deterministic cases (`cases.json`) with a one-cent tolerance. Only the
prompt changed, so the score difference is attributable to prompt quality.

## Key Finding

Naive LLM prompts can produce plausible finance code that fails subtle market
conventions. The baseline solution was syntactically clean and handled every
ordinary quote format, but silently mishandled extended eighths-of-a-32nd
notation. Adding explicit domain conventions in the prompt raised the score from
11/16 to 16/16.

## Reproduction

The benchmark infrastructure lives at the repository root and is runnable as-is.
From the repo root:

```bash
# grade the featured baseline run (expect 11/16)
python3 evaluate_attempt.py attempts/baseline_01/solution.py

# grade the featured improved run (expect 16/16)
python3 evaluate_attempt.py attempts/improved_01/solution.py

# run the oracle/reference test suite (expect 29 passed)
pytest
```

## Files

* [baseline.md](baseline.md) — the baseline run: prompt records, produced code,
  evaluation result, and failure analysis.
* [improved.md](improved.md) — the improved run: the convention-aware prompt,
  produced code, and what changed.
* [metadata.md](metadata.md) — what run metadata was and was not captured.
* [prompt_variants.md](prompt_variants.md) — **appendix**: the remaining
  canonical runs (baseline_02–05, improved_02–05) for this same task, with a
  summary table and per-run detail in [`runs/`](runs/). This headline write-up
  stays focused on baseline_01 → improved_01; the appendix covers the variants.
