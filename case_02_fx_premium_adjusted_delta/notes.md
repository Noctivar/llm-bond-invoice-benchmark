## Baseline

- Automated score: 3/10
- Manual rubric score: 6/10
- Classification: Partial success / core valuation failure
- Failure label: `wrong_discount_factor_in_premium_adjusted_spot_delta`
- Formula used: `exp(-r_f T) * (K/S) * N(d2)`
- Lower root: 0.277763795948
- Upper root: 1.176712833834
- Selected root: 1.176712833834

The baseline correctly recognized that premium-adjusted call delta is
non-monotonic and found two roots. However, it mixed the foreign-rate discount
factor with the spot normalization K/S. The correct premium-adjusted spot-delta
formula uses `exp(-r_d T) * (K/S) * N(d2)`, or equivalently
`exp(-r_f T) * (K/F) * N(d2)`. This produced incorrect strike roots.

## Improved

- Automated score: 10/10
- Manual rubric score: 10/10
- Classification: Full success
- Lower root: 0.280555368507
- Upper root: 1.175892721469
- Selected root: 1.175892721469

The improved prompt corrected the discount-factor and normalization mismatch,
found both correct roots, and selected the market-standard OTM call strike.