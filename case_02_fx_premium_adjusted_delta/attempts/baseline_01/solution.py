"""Premium-adjusted (foreign-currency-premium) 25-delta call strike.

Garman-Kohlhagen, premium-adjusted spot delta for a call:

    delta_pa(K) = exp(-r_f * T) * (K / S) * N(d2)

    d1 = (ln(S/K) + (r_d - r_f + 0.5*vol^2)*T) / (vol*sqrt(T))
    d2 = d1 - vol*sqrt(T)

Unlike the plain spot delta, delta_pa is NOT monotonic in K: it is 0 at K -> 0,
rises to a single interior maximum, then decays back to 0 as K -> infinity.
So a target delta below that maximum has TWO positive strike solutions.
"""

import math

SQRT2 = math.sqrt(2.0)


def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / SQRT2))


def premium_adjusted_call_delta(strike, spot, domestic_rate, foreign_rate,
                                maturity, volatility):
    """Premium-adjusted spot delta of a call (premium paid in foreign ccy)."""
    if strike <= 0.0:
        return 0.0
    vol_sqrt_t = volatility * math.sqrt(maturity)
    d1 = (math.log(spot / strike)
          + (domestic_rate - foreign_rate + 0.5 * volatility ** 2) * maturity) / vol_sqrt_t
    d2 = d1 - vol_sqrt_t
    return math.exp(-foreign_rate * maturity) * (strike / spot) * norm_cdf(d2)


def _bisect(f, lo, hi, tol=1e-14, max_iter=300):
    """Bisection on a bracket where f(lo) and f(hi) have opposite signs."""
    f_lo = f(lo)
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        f_mid = f(mid)
        if f_mid == 0.0 or (hi - lo) < tol:
            return mid
        if (f_lo < 0.0) != (f_mid < 0.0):
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    return 0.5 * (lo + hi)


def find_premium_adjusted_call_strikes(spot, domestic_rate, foreign_rate,
                                       maturity, volatility, target_delta):
    """Return every positive strike whose premium-adjusted call delta == target.

    Returns a dict with the forward, all solutions, their deltas, the
    market-standard OTM 25-delta strike, and the delta-maximising strike.
    """
    forward = spot * math.exp((domestic_rate - foreign_rate) * maturity)

    def delta(k):
        return premium_adjusted_call_delta(k, spot, domestic_rate, foreign_rate,
                                           maturity, volatility)

    # Locate the interior maximum of delta_pa(K) by golden-section/ternary search.
    lo, hi = 1e-12, spot * 100.0
    for _ in range(500):
        m1 = lo + (hi - lo) / 3.0
        m2 = hi - (hi - lo) / 3.0
        if delta(m1) < delta(m2):
            lo = m1
        else:
            hi = m2
    k_max = 0.5 * (lo + hi)
    delta_max = delta(k_max)

    if target_delta > delta_max:
        raise ValueError(
            "target delta %.6f exceeds the maximum attainable premium-adjusted "
            "delta %.6f (at K=%.6f); no strike solves it" % (target_delta, delta_max, k_max))

    f = lambda k: delta(k) - target_delta

    # Lower branch: delta rises from 0 at K->0+ up to delta_max at k_max.
    lower = _bisect(f, 1e-12, k_max)

    # Upper branch: delta falls from delta_max back to 0 as K -> infinity.
    upper_bound = k_max * 2.0
    while delta(upper_bound) > target_delta:
        upper_bound *= 2.0
    upper = _bisect(f, k_max, upper_bound)

    solutions = sorted({round(lower, 12), round(upper, 12)})

    # Market standard: the OTM call strike, i.e. the one on the decreasing
    # branch (above the delta-maximising strike, and above the forward).
    selected = upper

    return {
        "forward": forward,
        "solutions": solutions,
        "deltas": [delta(k) for k in solutions],
        "delta_max_strike": k_max,
        "delta_max": delta_max,
        "selected_strike": selected,
        "selected_delta": delta(selected),
    }


def main():
    spot = 1.10
    domestic_rate = 0.04
    foreign_rate = 0.02
    maturity = 0.50
    volatility = 0.12
    target_delta = 0.25

    res = find_premium_adjusted_call_strikes(spot, domestic_rate, foreign_rate,
                                             maturity, volatility, target_delta)

    print("Garman-Kohlhagen, premium-adjusted spot delta call")
    print("  spot = %.4f, r_d = %.4f, r_f = %.4f, T = %.4f, vol = %.4f, target = %.4f"
          % (spot, domestic_rate, foreign_rate, maturity, volatility, target_delta))
    print()
    print("FX forward                     : %.10f" % res["forward"])
    print("Delta-maximising strike        : %.10f  (max delta = %.10f)"
          % (res["delta_max_strike"], res["delta_max"]))
    print()
    print("Positive mathematical solutions:")
    for k, d in zip(res["solutions"], res["deltas"]):
        branch = "rising branch (below delta peak)" if k < res["delta_max_strike"] \
            else "falling branch (above delta peak)"
        print("  K = %.10f   delta_pa = %.10f   %s" % (k, d, branch))
    print()
    print("Market-standard OTM 25-delta call strike: %.10f (delta_pa = %.10f)"
          % (res["selected_strike"], res["selected_delta"]))
    print()
    print("Why the other solution is not quoted:")
    print("""  The premium-adjusted call delta exp(-r_f*T)*(K/S)*N(d2) is not monotonic in K.
  It is 0 as K -> 0, rises to a peak at K = %.6f, and decays back to 0 as K -> inf,
  so a 0.25 target is hit twice. The small root K = %.6f sits far below the forward
  (F = %.6f): it is a deep in-the-money call whose delta is small only because the
  premium paid in foreign currency is huge and almost entirely offsets the raw spot
  exposure. Deep-ITM options are not what the market quotes, the inverse delta->strike
  map there is ambiguous/unstable (delta is increasing in K, opposite to the usual
  convention), and the risk-reversal/butterfly quoting convention requires the
  out-of-the-money strike. The market therefore always takes the root on the
  decreasing branch above the peak, K = %.6f > F, the OTM call.""" % (
        res["delta_max_strike"], res["solutions"][0], res["forward"], res["selected_strike"]))


if __name__ == "__main__":
    main()
