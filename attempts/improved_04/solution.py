def invoice_amount(face_value, annual_coupon_rate, quote,
                   days_since_coupon, days_in_coupon_period):
    """Parse a Treasury clean price quote and return the dirty/invoice amount."""
    whole_str, _, frac_str = quote.partition("-")
    whole = int(whole_str)

    if frac_str.endswith("+"):
        # plus sign means an extra half of a 32nd
        thirty_seconds = int(frac_str[:-1]) + 0.5
    elif len(frac_str) == 3:
        # first two digits are 32nds, third digit is eighths of a 32nd
        thirty_seconds = int(frac_str[:2]) + int(frac_str[2]) / 8
    else:
        thirty_seconds = int(frac_str)

    parsed_clean_price = whole + thirty_seconds / 32

    clean_value = face_value * parsed_clean_price / 100
    accrued_interest = (face_value * annual_coupon_rate / 2
                        * days_since_coupon / days_in_coupon_period)
    invoice = clean_value + accrued_interest

    return round(invoice, 2)
