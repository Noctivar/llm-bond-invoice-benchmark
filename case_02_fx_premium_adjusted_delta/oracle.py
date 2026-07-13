"""Oracle for premium-adjusted FX spot-call delta."""

from __future__ import annotations

import math
from statistics import NormalDist
from typing import Dict, List

_NORMAL = NormalDist()


def premium_adjusted_spot_call_delta(
    strike: float,
    spot: float,
    domestic_rate: float,
    foreign_rate: float,
    maturity: float,
    volatility: float,
) -> float:
    if strike <= 0.0:
        raise ValueError("strike must be positive")
    if spot <= 0.0 or maturity <= 0.0 or volatility <= 0.0:
        raise ValueError("spot, maturity, and volatility must be positive")

    forward = spot * math.exp(
        (domestic_rate - foreign_rate) * maturity
    )
    root_t = math.sqrt(maturity)
    d1 = (
        math.log(forward / strike)
        + 0.5 * volatility * volatility * maturity
    ) / (volatility * root_t)
    d2 = d1 - volatility * root_t

    return (
        math.exp(-domestic_rate * maturity)
        * (strike / spot)
        * _NORMAL.cdf(d2)
    )


def _bisect_root(
    function,
    lower: float,
    upper: float,
    target: float,
    iterations: int = 200,
) -> float:
    f_lower = function(lower) - target
    f_upper = function(upper) - target

    if f_lower == 0.0:
        return lower
    if f_upper == 0.0:
        return upper
    if f_lower * f_upper > 0.0:
        raise ValueError("root is not bracketed")

    for _ in range(iterations):
        midpoint = 0.5 * (lower + upper)
        f_midpoint = function(midpoint) - target

        if abs(f_midpoint) < 1.0e-15:
            return midpoint

        if f_lower * f_midpoint <= 0.0:
            upper = midpoint
            f_upper = f_midpoint
        else:
            lower = midpoint
            f_lower = f_midpoint

    return 0.5 * (lower + upper)


def solve_case(
    spot: float = 1.10,
    domestic_rate: float = 0.04,
    foreign_rate: float = 0.02,
    maturity: float = 0.50,
    volatility: float = 0.12,
    target_delta: float = 0.25,
) -> Dict[str, object]:
    forward = spot * math.exp(
        (domestic_rate - foreign_rate) * maturity
    )

    def delta(strike: float) -> float:
        return premium_adjusted_spot_call_delta(
            strike=strike,
            spot=spot,
            domestic_rate=domestic_rate,
            foreign_rate=foreign_rate,
            maturity=maturity,
            volatility=volatility,
        )

    # Ternary search for the unique maximum of the call delta.
    lower = 1.0e-12
    upper = forward * 5.0
    for _ in range(250):
        left = lower + (upper - lower) / 3.0
        right = upper - (upper - lower) / 3.0
        if delta(left) < delta(right):
            lower = left
        else:
            upper = right

    strike_at_maximum = 0.5 * (lower + upper)
    maximum_delta = delta(strike_at_maximum)

    if not 0.0 < target_delta < maximum_delta:
        raise ValueError("target delta must lie below the maximum")

    low_root = _bisect_root(
        delta,
        1.0e-12,
        strike_at_maximum,
        target_delta,
    )
    high_root = _bisect_root(
        delta,
        strike_at_maximum,
        forward * 10.0,
        target_delta,
    )

    return {
        "forward": forward,
        "all_strikes": [low_root, high_root],
        "deltas_at_strikes": [delta(low_root), delta(high_root)],
        "selected_market_strike": high_root,
        "maximum_delta": maximum_delta,
        "strike_at_maximum": strike_at_maximum,
        "explanation": (
            "The lower root is a deeply in-the-money call. "
            "The market-standard quoted 25-delta call is the "
            "out-of-the-money root above the forward."
        ),
    }


if __name__ == "__main__":
    result = solve_case()
    for key, value in result.items():
        print(f"{key}: {value}")
