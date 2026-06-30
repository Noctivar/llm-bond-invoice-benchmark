def parse_quote(quote):
    quote = str(quote).strip()
    points_str, frac_str = quote.split("-")
    points = int(points_str)

    plus = frac_str.endswith("+")
    if plus:
        frac_str = frac_str[:-1]

    thirty_seconds = int(frac_str[:2])
    eighths = 0
    if plus:
        eighths = 4
    elif len(frac_str) > 2:
        eighths = int(frac_str[2])

    thirty_seconds_total = thirty_seconds + eighths / 8.0
    return points + thirty_seconds_total / 32.0


def invoice_amount(face_value, annual_coupon_rate, quote, days_since_coupon, days_in_coupon_period):
    parsed_quote = parse_quote(quote)
    clean_value = face_value * parsed_quote / 100.0
    accrued_interest = face_value * annual_coupon_rate / 2.0 * days_since_coupon / days_in_coupon_period
    return round(clean_value + accrued_interest, 2)
