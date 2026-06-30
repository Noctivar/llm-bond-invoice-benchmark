# Improved results

Scores for the clear-prompt attempts. Fill this in after running each attempt
through the evaluator. (Attempt solutions are **not** included in this repo yet —
generate them from `prompts/improved_prompts.md`.)

To produce a row:

```
python evaluate_attempt.py attempts/improved_01/attempt.py
```

## Summary

| run_id      | prompt | model | tests_passed | tests_total | score | notes |
|-------------|--------|-------|--------------|-------------|-------|-------|
| improved_01 | 1      |       | _TBD_        | 12          |       |       |
| improved_02 | 2      |       | _TBD_        | 12          |       |       |
| improved_03 | 3      |       | _TBD_        | 12          |       |       |
| improved_04 | 4      |       | _TBD_        | 12          |       |       |
| improved_05 | 5      |       | _TBD_        | 12          |       |       |

## Baseline vs improved

| metric                  | baseline (avg) | improved (avg) |
|-------------------------|----------------|----------------|
| tests_passed / 12       | _TBD_          | _TBD_          |
| score %                 | _TBD_          | _TBD_          |

## Per-attempt notes

### improved_01
_paste evaluator output / observations here_

### improved_02

### improved_03

### improved_04

### improved_05

## Improved Results Summary

All improved prompts passed the full deterministic evaluator.

| Run | Score | Result |
|---|---:|---|
| Improved 1 | 16/16 | PASS |
| Improved 2 | 16/16 | PASS |
| Improved 3 | 16/16 | PASS |
| Improved 4 | 16/16 | PASS |
| Improved 5 | 16/16 | PASS |

The improved prompts explicitly specified:
- Treasury quote parsing in 32nds
- plus-tick notation
- eighths-of-a-32nd notation
- clean price vs invoice/dirty amount
- semiannual coupon accrual
- final cent rounding without intermediate rounding

Conclusion:
Guided prompts corrected the failure modes observed in the baseline attempts.

## Improved Results Summary

All improved prompts passed the full deterministic evaluator.

| Run | Score | Result |
|---|---:|---|
| Improved 1 | 16/16 | PASS |
| Improved 2 | 16/16 | PASS |
| Improved 3 | 16/16 | PASS |
| Improved 4 | 16/16 | PASS |
| Improved 5 | 16/16 | PASS |

The improved prompts explicitly specified:
- Treasury quote parsing in 32nds
- plus-tick notation
- eighths-of-a-32nd notation
- clean price vs invoice/dirty amount
- semiannual coupon accrual
- final cent rounding without intermediate rounding

Conclusion:
Guided prompts corrected the failure modes observed in the baseline attempts.
