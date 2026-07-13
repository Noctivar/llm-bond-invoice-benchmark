"""Premium-adjusted spot delta strikes for a Garman-Kohlhagen FX call."""

from math import erf, exp, log, sqrt


def _norm_cdf(x):
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))


def find_premium_adjusted_call_strikes(
    spot,
    domestic_rate,
    foreign_rate,
    maturity,
    volatility,
    target_delta,
):
    forward = spot * exp((domestic_rate - foreign_rate) * maturity)
    vol_sqrt_t = volatility * sqrt(maturity)
    df_domestic = exp(-domestic_rate * maturity)

    def delta(strike):
        d1 = (log(forward / strike) + 0.5 * volatility**2 * maturity) / vol_sqrt_t
        d2 = d1 - vol_sqrt_t
        return df_domestic * (strike / spot) * _norm_cdf(d2)

    # The premium-adjusted call delta rises from 0 at K -> 0, peaks, then decays
    # back to 0, so locate the peak first and bisect on each side of it.
    lo, hi = 1e-8 * forward, 1e8 * forward
    for _ in range(500):
        m1 = lo + (hi - lo) / 3.0
        m2 = hi - (hi - lo) / 3.0
        if delta(m1) < delta(m2):
            lo = m1
        else:
            hi = m2
    strike_at_maximum = 0.5 * (lo + hi)
    maximum_delta = delta(strike_at_maximum)

    def bisect(low, high):
        for _ in range(400):
            mid = 0.5 * (low + high)
            if (delta(low) - target_delta) * (delta(mid) - target_delta) <= 0.0:
                high = mid
            else:
                low = mid
        return 0.5 * (low + high)

    all_strikes = []
    if maximum_delta >= target_delta:
        all_strikes.append(bisect(1e-8 * forward, strike_at_maximum))
        all_strikes.append(bisect(strike_at_maximum, 1e8 * forward))
        all_strikes.sort()

    otm_roots = [k for k in all_strikes if k > forward]
    selected_market_strike = max(otm_roots) if otm_roots else None

    explanation = (
        "Premium-adjusted spot delta is exp(-rd*T) * (K/S) * N(d2), which is zero "
        "at both K -> 0 and K -> infinity, so it is hump-shaped with a maximum of "
        "{:.6f} at K = {:.6f}. A target delta below that maximum therefore has two "
        "positive roots, one on each side of the peak. The quoted 25-delta call is "
        "the out-of-the-money root above the forward ({:.6f}), i.e. K = {}.".format(
            maximum_delta,
            strike_at_maximum,
            forward,
            "{:.6f}".format(selected_market_strike) if selected_market_strike else "none",
        )
    )

    return {
        "forward": forward,
        "all_strikes": all_strikes,
        "deltas_at_strikes": [delta(k) for k in all_strikes],
        "selected_market_strike": selected_market_strike,
        "maximum_delta": maximum_delta,
        "strike_at_maximum": strike_at_maximum,
        "explanation": explanation,
    }


if __name__ == "__main__":
    result = find_premium_adjusted_call_strikes(
        spot=1.10,
        domestic_rate=0.04,
        foreign_rate=0.02,
        maturity=0.50,
        volatility=0.12,
        target_delta=0.25,
    )
    for key, value in result.items():
        print("{}: {}".format(key, value))
