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
