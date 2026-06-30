"""Convert Treasury bond quotes into dollar invoice prices.

Treasury bonds are quoted in points and 32nds of a point, per 100 of face
value, e.g. "99-16" means 99 + 16/32.  An optional trailing "+" adds a further
1/64 of a point, e.g. "99-16+" means 99 + 16/32 + 1/64.

The *invoice price* (a.k.a. dirty price) paid by the buyer is the quoted clean
price plus accrued interest:

    invoice = clean_price + accrued_interest

where both are scaled to the bond's face value.
"""

import re

# Treasury quote: <points>-<thirty-seconds><optional +>
_QUOTE_RE = re.compile(r"^\s*(\d+)-(\d{1,2})(\+?)\s*$")


def parse_quote(quote):
    """Return the clean price per 100 face value for a Treasury quote string.

    Accepts forms like ``99-16``, ``99-16+`` and ``101-03``.
    """
    match = _QUOTE_RE.match(quote)
    if not match:
        raise ValueError("Invalid Treasury quote: {!r}".format(quote))

    points = int(match.group(1))
    thirty_seconds = int(match.group(2))
    has_plus = match.group(3) == "+"

    if thirty_seconds >= 32:
        raise ValueError(
            "32nds part must be in 0..31, got {} in {!r}".format(thirty_seconds, quote)
        )

    price = points + thirty_seconds / 32.0
    if has_plus:
        price += 1.0 / 64.0
    return price


def invoice_amount(
    face_value,
    annual_coupon_rate,
    quote,
    days_since_coupon,
    days_in_coupon_period,
):
    """Dollar invoice price (dirty price) for a Treasury bond trade.

    Parameters
    ----------
    face_value : float
        Face (par) value of the bond, e.g. 100000.
    annual_coupon_rate : float
        Annual coupon rate as a decimal (e.g. 0.06 for 6%).  Treasuries pay
        semiannually, so each coupon is half of this.
    quote : str
        Treasury quote such as "99-16", "99-16+" or "101-03".
    days_since_coupon : int
        Days elapsed since the last coupon payment.
    days_in_coupon_period : int
        Total days in the current coupon period.

    Returns
    -------
    float
        The dollar amount paid by the buyer (clean price + accrued interest).
    """
    if days_in_coupon_period <= 0:
        raise ValueError("days_in_coupon_period must be positive")
    if not (0 <= days_since_coupon <= days_in_coupon_period):
        raise ValueError(
            "days_since_coupon must be in 0..days_in_coupon_period"
        )

    clean_per_100 = parse_quote(quote)
    clean_price = clean_per_100 / 100.0 * face_value

    semiannual_coupon = annual_coupon_rate / 2.0 * face_value
    accrued_interest = semiannual_coupon * days_since_coupon / days_in_coupon_period

    return clean_price + accrued_interest


if __name__ == "__main__":
    # Example: $100,000 face, 6% coupon, quoted 99-16+, 60 of 182 days elapsed.
    price = invoice_amount(
        face_value=100000,
        annual_coupon_rate=0.06,
        quote="99-16+",
        days_since_coupon=60,
        days_in_coupon_period=182,
    )
    print("Invoice amount: {:,.2f}".format(price))
