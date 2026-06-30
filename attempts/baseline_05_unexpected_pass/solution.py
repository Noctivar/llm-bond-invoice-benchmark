"""Simple U.S. Treasury bond pricing calculator.

Treasury notes/bonds are quoted in points and 32nds of a point, where one
point equals 1% of par (face value).  A quote like ``99-16+`` is read as:

    99      -> whole points (99% of par)
    16      -> 32nds of a point (16/32)
    +       -> an extra half 32nd (1/64)

So ``99-16+`` == 99 + 16/32 + 1/64 == 99.515625 (percent of par).

The *invoice amount* (a.k.a. dirty price) actually paid by a buyer is the
clean price implied by the quote plus the accrued interest owed to the
seller for the portion of the current coupon period that has elapsed.
"""

from __future__ import annotations


def parse_quote(quote) -> float:
    """Parse a Treasury price quote into a percentage of par.

    Accepts strings such as ``"99-16"``, ``"99-16+"``, ``"101-085"`` or a
    plain number (already a percent of par).

    The fractional part after the dash is expressed in 32nds:
      * two digits        -> XX/32
      * trailing ``+``     -> add 1/64 (half a 32nd)
      * three digits ``XXY`` -> XX/32 + Y/8 of a 32nd (eighths of a 32nd)
    """
    if isinstance(quote, (int, float)):
        return float(quote)

    text = str(quote).strip()
    if "-" not in text:
        # Plain decimal quote, e.g. "99.515625"
        return float(text)

    whole_str, frac_str = text.split("-", 1)
    whole = float(whole_str)

    plus = frac_str.endswith("+")
    if plus:
        frac_str = frac_str[:-1]

    thirty_seconds = 0.0
    if frac_str:
        if len(frac_str) <= 2:
            thirty_seconds = float(frac_str)
        else:
            # First two digits are 32nds, remaining digit is eighths of a 32nd.
            thirty_seconds = float(frac_str[:2])
            thirty_seconds += float(frac_str[2:]) / 8.0

    if plus:
        thirty_seconds += 0.5

    return whole + thirty_seconds / 32.0


def invoice_amount(
    face_value: float,
    annual_coupon_rate: float,
    quote,
    days_since_coupon: float,
    days_in_coupon_period: float,
) -> float:
    """Return the invoice (dirty) price of a Treasury bond.

    Parameters
    ----------
    face_value:
        Par value of the bond (e.g. 100000).
    annual_coupon_rate:
        Annual coupon rate as a decimal (e.g. 0.05 for 5%).  Treasuries pay
        semi-annually, so each coupon is half this rate times face value.
    quote:
        Price quote, e.g. ``"99-16+"`` or a numeric percent of par.
    days_since_coupon:
        Days elapsed since the last coupon payment.
    days_in_coupon_period:
        Total days in the current coupon period.

    Returns
    -------
    float
        Clean price + accrued interest.
    """
    price_pct = parse_quote(quote)
    clean_price = price_pct / 100.0 * face_value

    semiannual_coupon = annual_coupon_rate / 2.0 * face_value
    accrued_interest = semiannual_coupon * (
        days_since_coupon / days_in_coupon_period
    )

    return clean_price + accrued_interest


if __name__ == "__main__":
    # Example: $100,000 face, 6% coupon, quoted 99-16+, 60 of 182 days elapsed.
    amount = invoice_amount(100_000, 0.06, "99-16+", 60, 182)
    print(f"Quote 99-16+ parses to {parse_quote('99-16+')}% of par")
    print(f"Invoice amount: {amount:,.2f}")
