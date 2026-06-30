def _parse_quote(quote):
    """Parse a 32nds Treasury price quote into a clean price (float)."""
    quote = quote.strip()
    whole_str, frac_str = quote.split("-")
    whole = int(whole_str)

    plus = frac_str.endswith("+")
    if plus:
        frac_str = frac_str[:-1]

    thirty_seconds = int(frac_str[:2])

    eighths = 0
    if len(frac_str) > 2:
        eighths = int(frac_str[2])
    if plus:
        eighths = 4  # half of 1/32 == 4/8 of 1/32

    fraction = (thirty_seconds + eighths / 8) / 32
    return whole + fraction


def invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon,
                   days_in_coupon_period):
    clean_price = _parse_quote(quote)
    clean_value = face_value * clean_price / 100
    accrued_interest = (face_value * annual_coupon_rate / 2
                        * days_since_coupon / days_in_coupon_period)
    return round(clean_value + accrued_interest, 2)
