# Case 02: Premium-Adjusted FX Call Delta

## Failure being tested

This case tests whether an LLM correctly distinguishes the premium-adjusted
**spot** delta from nearby FX delta conventions.

The submitted baseline correctly recognized that a premium-adjusted call delta
is non-monotonic in strike and therefore can have two positive strike roots.
However, it used the wrong discount factor in the delta formula:

```text
wrong:   exp(-r_f T) * (K / S) * N(d2)
correct: exp(-r_d T) * (K / S) * N(d2)
```

The correct formula is equivalently:

```text
exp(-r_f T) * (K / F) * N(d2)
```

where:

```text
F = S * exp((r_d - r_f)T)
```

The baseline mixed the spot normalization `K/S` with the foreign discount
factor that belongs with the forward normalization `K/F`.

## Parameters

| Parameter | Value |
|---|---:|
| Spot | 1.10 |
| Domestic rate | 4% |
| Foreign rate | 2% |
| Maturity | 0.50 years |
| Volatility | 12% |
| Target premium-adjusted spot call delta | 25% |

## Ground truth

| Quantity | Correct value |
|---|---:|
| Forward | 1.111055183793 |
| Lower strike root | 0.280555368507 |
| OTM call strike root | 1.175892721469 |
| Selected market-standard strike | 1.175892721469 |
| Maximum premium-adjusted spot call delta | 0.816361020486 |
| Strike at maximum delta | 0.951784200684 |

## Baseline result

The observed baseline reported approximately:

```text
lower root: 0.2777638
upper root: 1.1767128
```

Those values solve the incorrect formula with `exp(-r_f T) * K/S`.

## Files

```text
baseline_prompt.txt
improved_prompt.txt
oracle.py
evaluate_attempt.py
ground_truth.json
rubric.json
notes.md
SOURCES.md
attempts/
results/
```

## Run order

1. Copy the already-generated baseline `solution.py` into:
   `attempts/baseline_01/solution.py`
2. Run:
   `python3 evaluate_attempt.py attempts/baseline_01/solution.py`
3. Preserve the output in:
   `results/baseline_01_eval.txt`
4. Run `improved_prompt.txt` in a fresh Claude Code folder.
5. Copy the improved output into:
   `attempts/improved_01/solution.py`
6. Evaluate it with the same evaluator.
