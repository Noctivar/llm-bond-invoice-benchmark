def invoice_amount(
    face_value,
    annual_coupon_rate,
    quote,
    days_since_coupon,
    days_in_coupon_period,
):
    """Calculate the invoice (dirty) price paid for a Treasury bond purchase.

    The invoice amount is the clean price (from the quote) plus accrued
    interest.

    Treasury bonds are quoted in points and 32nds of a point, e.g. "99-16"
    means 99 + 16/32 = 99.5 percent of par. A trailing "+" adds a further
    1/64 of a point, so "99-16+" means 99 + 16/32 + 1/64.

    Parameters
    ----------
    face_value : float
        Par/face value of the bond.
    annual_coupon_rate : float
        Annual coupon rate as a decimal (e.g. 0.05 for 5%). Coupons are
        assumed to be paid semiannually.
    quote : str
        Price quote in 32nds, e.g. "99-16" or "99-16+".
    days_since_coupon : int
        Days elapsed since the last coupon payment.
    days_in_coupon_period : int
        Total days in the current coupon period.

    Returns
    -------
    float
        The total amount paid (clean price + accrued interest).
    """
    price_pct = _parse_quote(quote)

    clean_price = face_value * price_pct / 100.0

    semiannual_coupon = face_value * annual_coupon_rate / 2.0
    accrued_interest = semiannual_coupon * days_since_coupon / days_in_coupon_period

    return clean_price + accrued_interest


def _parse_quote(quote):
    """Convert a 32nds quote string like "99-16" or "99-16+" to a percent."""
    quote = quote.strip()

    plus = quote.endswith("+")
    if plus:
        quote = quote[:-1]

    handle_str, _, ticks_str = quote.partition("-")
    handle = int(handle_str)
    ticks = int(ticks_str)

    price = handle + ticks / 32.0
    if plus:
        price += 1.0 / 64.0

    return price


if __name__ == "__main__":
    # 99-16+ = 99 + 16/32 + 1/64 = 99.515625 percent of par
    print(invoice_amount(100_000, 0.06, "99-16+", 30, 182))
