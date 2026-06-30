def parse_quote(quote):
    """Convert a Treasury price quote string to its decimal value.

    The fractional part after the dash is in 32nds, optionally followed by a
    finer increment: a '+' means a half 32nd (4/8), and a trailing digit gives
    the number of eighths of a 32nd.
    """
    quote = str(quote).strip()
    whole_str, frac_str = quote.split("-")
    whole = int(whole_str)

    thirty_seconds = int(frac_str[:2])

    eighths = 0
    if len(frac_str) > 2:
        tail = frac_str[2:]
        if tail == "+":
            eighths = 4
        else:
            eighths = int(tail)

    return whole + (thirty_seconds + eighths / 8) / 32


def invoice_amount(face_value, annual_coupon_rate, quote,
                   days_since_coupon, days_in_coupon_period):
    clean_quote_decimal = parse_quote(quote)

    clean_value = face_value * clean_quote_decimal / 100
    accrued_interest = (face_value * annual_coupon_rate / 2
                        * days_since_coupon / days_in_coupon_period)
    invoice = clean_value + accrued_interest

    return round(invoice, 2)
