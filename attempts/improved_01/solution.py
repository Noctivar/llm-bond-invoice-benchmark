from decimal import Decimal, ROUND_HALF_UP


def _parse_quote(quote):
    """Parse a Treasury price quote (quoted in 32nds) into a Decimal price
    per 100 face value."""
    quote = str(quote).strip()
    whole_str, frac_str = quote.split("-")
    whole = Decimal(whole_str)

    # The fractional field after the dash is expressed in 32nds.
    # First two characters: the number of 32nds.
    thirty_seconds = Decimal(frac_str[0:2])

    extra = frac_str[2:]
    if extra == "+":
        # '+' denotes half of a 32nd.
        thirty_seconds += Decimal("0.5")
    elif extra:
        # A trailing digit denotes eighths of a 32nd.
        thirty_seconds += Decimal(extra) / Decimal(8)

    return whole + thirty_seconds / Decimal(32)


def invoice_amount(face_value, annual_coupon_rate, quote,
                   days_since_coupon, days_in_coupon_period):
    face_value = Decimal(str(face_value))
    annual_coupon_rate = Decimal(str(annual_coupon_rate))
    days_since_coupon = Decimal(str(days_since_coupon))
    days_in_coupon_period = Decimal(str(days_in_coupon_period))

    clean_price = _parse_quote(quote)

    clean_value = face_value * clean_price / Decimal(100)
    accrued_interest = (face_value * annual_coupon_rate / Decimal(2)
                        * days_since_coupon / days_in_coupon_period)

    invoice = clean_value + accrued_interest
    return float(invoice.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


if __name__ == "__main__":
    # 99-16 = 99.50 clean price
    print(invoice_amount(100000, 0.05, "99-16", 30, 182))
    print(invoice_amount(100000, 0.05, "99-16+", 30, 182))
    print(invoice_amount(100000, 0.05, "98-317", 30, 182))
    print(invoice_amount(100000, 0.05, "101-035", 30, 182))
