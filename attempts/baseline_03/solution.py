"""Fixed-income quote converter for US Treasury bonds.

Treasury bonds are quoted in points and 32nds of a point, written as
``handle-ticks``.  For example ``99-16`` means 99 and 16/32 = 99.5 percent
of face value.  A trailing ``+`` adds half a 32nd (i.e. 1/64).

The price a buyer actually pays (the "invoice" or "dirty" price) is the
quoted clean price plus accrued interest since the last coupon payment.
US Treasuries pay coupons semi-annually.
"""


def parse_quote(quote):
    """Convert a Treasury quote string into a decimal price per 100 face.

    Examples:
        "99-16+"  -> 99.515625   (99 + 16.5/32)
        "101-03"  -> 101.09375   (101 + 3/32)
        "100-00"  -> 100.0
    """
    quote = quote.strip()

    handle_str, _, ticks_str = quote.partition("-")
    if not ticks_str:
        raise ValueError("Quote must be in 'handle-ticks' form, e.g. 99-16+")

    handle = int(handle_str)

    # An optional trailing '+' means an extra half tick (1/64 of a point).
    extra_half_tick = ticks_str.endswith("+")
    if extra_half_tick:
        ticks_str = ticks_str[:-1]

    ticks = int(ticks_str)
    if extra_half_tick:
        ticks += 0.5

    return handle + ticks / 32.0


def invoice_amount(face_value, annual_coupon_rate, quote,
                   days_since_coupon, days_in_coupon_period):
    """Return the total dollar amount the buyer pays for a Treasury bond.

    Args:
        face_value: par (face) amount of the bond, e.g. 1000 or 1_000_000.
        annual_coupon_rate: annual coupon as a decimal, e.g. 0.05 for 5%.
        quote: Treasury price quote string, e.g. "99-16+".
        days_since_coupon: days elapsed since the last coupon payment.
        days_in_coupon_period: total days in the current coupon period.

    The invoice (dirty) price is the clean price plus accrued interest.
    Treasuries pay semi-annually, so each coupon period carries half the
    annual coupon.
    """
    decimal_price = parse_quote(quote)
    clean_price = face_value * decimal_price / 100.0

    coupon_per_period = face_value * annual_coupon_rate / 2.0
    accrued_interest = coupon_per_period * days_since_coupon / days_in_coupon_period

    return clean_price + accrued_interest


if __name__ == "__main__":
    # 99-16+ on $100,000 face, 5% coupon, 60 of 181 days into the period.
    amount = invoice_amount(
        face_value=100_000,
        annual_coupon_rate=0.05,
        quote="99-16+",
        days_since_coupon=60,
        days_in_coupon_period=181,
    )
    print(f"Invoice amount: ${amount:,.2f}")
