"""Reference ("oracle") implementation of the Treasury bond invoice problem.

This module encodes the *correct* finance rules. It is used both to generate
the expected values in ``cases.json`` and as the ground truth that
``evaluate_attempt.py`` compares candidate solutions against.

Finance rules
-------------
1. Treasury-style quotes are in 32nds of a point.
   - ``"99-16"``  = 99 + 16/32
   - ``"99-16+"`` = 99 + 16.5/32      (the trailing ``+`` adds half a 32nd)
   - ``"101-03"`` = 101 + 3/32
   (A trailing single digit denotes eighths of a 32nd, e.g. ``"99-162"`` =
   99 + 16.25/32, and ``+`` is exactly equivalent to a ``4`` in that slot.)

2. The quote is a *clean* price expressed per 100 of face value.

3. clean_value = face_value * clean_price_decimal / 100

4. accrued_interest =
       face_value * annual_coupon_rate / 2
       * days_since_coupon / days_in_coupon_period
   (``/ 2`` because Treasury coupons pay semiannually.)

5. invoice_amount (a.k.a. dirty value) = clean_value + accrued_interest
"""

from __future__ import annotations


def parse_quote(quote) -> float:
    """Convert a Treasury-style 32nds quote into a decimal price per 100.

    Accepts strings such as ``"99-16"``, ``"99-16+"``, ``"101-03"`` and the
    less common eighths form ``"99-162"``. For convenience a numeric input is
    treated as an already-decimal price and returned unchanged.

    Raises ``ValueError`` on input that does not look like a Treasury quote.
    """
    # Allow callers to pass an already-decimal price through untouched.
    if isinstance(quote, (int, float)):
        return float(quote)

    if not isinstance(quote, str):
        raise ValueError(f"Unsupported quote type: {type(quote)!r}")

    text = quote.strip()
    if "-" not in text:
        raise ValueError(f"Quote {quote!r} is not in Treasury 'handle-ticks' form")

    handle_str, ticks_str = text.split("-", 1)
    handle = int(handle_str)

    # A trailing '+' means an extra half tick == 4 eighths of a 32nd.
    eighths = 0
    if ticks_str.endswith("+"):
        eighths = 4
        ticks_str = ticks_str[:-1]

    # An optional third character encodes eighths of a 32nd (0-7).
    if len(ticks_str) == 3:
        eighths = int(ticks_str[2])
        ticks_str = ticks_str[:2]

    if not ticks_str.isdigit() or len(ticks_str) > 2:
        raise ValueError(f"Quote {quote!r} has an unparseable 32nds field")

    ticks = int(ticks_str)
    if ticks >= 32 or eighths >= 8:
        raise ValueError(f"Quote {quote!r} has an out-of-range 32nds field")

    return handle + (ticks + eighths / 8.0) / 32.0


def clean_value(face_value: float, quote) -> float:
    """Clean (quoted) value of the position, before accrued interest."""
    return face_value * parse_quote(quote) / 100.0


def accrued_interest(
    face_value: float,
    annual_coupon_rate: float,
    days_since_coupon: float,
    days_in_coupon_period: float,
) -> float:
    """Accrued interest using semiannual coupons and actual day counts.

    ``annual_coupon_rate`` is a decimal (0.05 == 5%).
    """
    semiannual_coupon = face_value * annual_coupon_rate / 2.0
    return semiannual_coupon * days_since_coupon / days_in_coupon_period


def invoice_amount(
    face_value: float,
    annual_coupon_rate: float,
    quote,
    days_since_coupon: float,
    days_in_coupon_period: float,
) -> float:
    """Invoice (dirty) amount = clean value + accrued interest, rounded to cents."""
    dirty = clean_value(face_value, quote) + accrued_interest(
        face_value, annual_coupon_rate, days_since_coupon, days_in_coupon_period
    )
    return round(dirty, 2)


if __name__ == "__main__":
    # Quick manual sanity check.
    print("99-16  ->", parse_quote("99-16"))
    print("99-16+ ->", parse_quote("99-16+"))
    print("101-03 ->", parse_quote("101-03"))
    print(
        "invoice ->",
        invoice_amount(100_000, 0.05, "99-16+", 90, 181),
    )
