def invoice_amount(face_value, annual_coupon_rate, quote,
                   days_since_coupon, days_in_coupon_period):
    """Calculate the total (dirty) amount paid for a bond trade.

    The invoice amount is the clean price implied by the quote plus the
    accrued interest owed to the seller since the last coupon.

    Args:
        face_value: Par/face value of the bond (e.g. 1000).
        annual_coupon_rate: Annual coupon rate as a decimal (e.g. 0.05 for 5%).
        quote: Quoted clean price as a string, expressed as a percent of par
            (e.g. "99.5" means 99.5% of face value).
        days_since_coupon: Days elapsed since the last coupon payment.
        days_in_coupon_period: Total days in the current coupon period.

    Returns:
        The total amount paid (clean price + accrued interest).
    """
    clean_price = (float(quote) / 100.0) * face_value

    period_coupon = face_value * annual_coupon_rate
    accrued_interest = period_coupon * (days_since_coupon / days_in_coupon_period)

    return clean_price + accrued_interest


if __name__ == "__main__":
    # Example: $1,000 bond, 5% annual coupon, quoted at 99.5,
    # 90 of 182 days into the coupon period.
    print(invoice_amount(1000, 0.05, "99.5", 90, 182))
