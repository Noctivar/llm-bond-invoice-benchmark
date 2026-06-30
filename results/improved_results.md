# Improved Results

These runs used guided prompts that explicitly stated the missing finance conventions.

| Run | Score | Result |
|---|---:|---|
| Improved 1 | 16/16 | Passed |
| Improved 2 | 16/16 | Passed |
| Improved 3 | 16/16 | Passed |
| Improved 4 | 16/16 | Passed |
| Improved 5 | 16/16 | Passed |

The improved prompts explicitly specified:

- Treasury quote parsing in 32nds
- plus-tick notation
- eighths-of-a-32nd notation
- clean price versus dirty/invoice amount
- semiannual coupon accrual
- final cent rounding without intermediate rounding

## Conclusion

Guided prompts corrected the failure modes observed in the baseline attempts. All improved attempts passed the full deterministic evaluator.
