"""Treasury bond invoice (dirty) price calculation."""


def parse_quote(quote):
    """Convert a Treasury bond price quote into a decimal price per 100 of face.

    Treasury bonds are quoted in points and 32nds of a point, written as
    ``points-ticks`` (e.g. ``"101-03"`` -> 101 + 3/32).  A trailing ``+`` means
    an extra half of a 32nd, i.e. a 64th (e.g. ``"99-16+"`` -> 99 + 16/32 + 1/64).
    """
    quote = quote.strip()
    points_str, ticks_str = quote.split("-")
    points = int(points_str)

    plus = ticks_str.endswith("+")
    if plus:
        ticks_str = ticks_str[:-1]

    ticks = int(ticks_str)
    price = points + ticks / 32.0
    if plus:
        price += 1.0 / 64.0

    return price


def invoice_amount(face_value, annual_coupon_rate, quote,
                   days_since_coupon, days_in_coupon_period):
    """Return the total amount a buyer pays for a Treasury bond.

    The invoice (dirty) price is the quoted clean price plus accrued interest.

    Parameters
    ----------
    face_value : float
        Par/face value of the bond.
    annual_coupon_rate : float
        Annual coupon rate as a decimal (e.g. 0.05 for 5%).
    quote : str
        Quoted clean price in bond format, e.g. ``"99-16+"``, ``"101-03"``.
    days_since_coupon : int
        Days elapsed since the last coupon payment.
    days_in_coupon_period : int
        Total days in the current coupon period.
    """
    price_per_100 = parse_quote(quote)
    clean_price = price_per_100 / 100.0 * face_value

    # Treasury bonds pay semiannual coupons.
    coupon_payment = annual_coupon_rate / 2.0 * face_value
    accrued_interest = coupon_payment * (days_since_coupon / days_in_coupon_period)

    return clean_price + accrued_interest


if __name__ == "__main__":
    # 100,000 face, 5% coupon, quoted 99-16+, halfway through a 182-day period.
    amt = invoice_amount(100_000, 0.05, "99-16+", 91, 182)
    print(f"Invoice amount: {amt:,.2f}")
