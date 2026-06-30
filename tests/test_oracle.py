"""Unit tests for the oracle. Each test names the natural mistake it guards against.

Run with::  pytest -q   (from the repo root)
"""

import json
import os
import sys

import pytest

# Make the repo root importable when pytest is run from anywhere.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import oracle  # noqa: E402


# --------------------------------------------------------------------------- #
# Quote parsing
# --------------------------------------------------------------------------- #
def test_parse_basic_32nds():
    # Guards against: parsing "99-16" as the decimal 99.16
    assert oracle.parse_quote("99-16") == pytest.approx(99 + 16 / 32)


def test_parse_trailing_plus_is_half_tick():
    # Guards against: ignoring the trailing '+'
    assert oracle.parse_quote("99-16+") == pytest.approx(99 + 16.5 / 32)
    assert oracle.parse_quote("99-16+") != oracle.parse_quote("99-16")


def test_parse_low_ticks_not_decimal():
    # Guards against: "101-03" -> 101.03
    assert oracle.parse_quote("101-03") == pytest.approx(101 + 3 / 32)
    assert oracle.parse_quote("100-01") == pytest.approx(100 + 1 / 32)


def test_parse_eighths_subtick():
    # The third digit encodes eighths of a 32nd; '+' equals a 4 there.
    assert oracle.parse_quote("99-162") == pytest.approx(99 + (16 + 2 / 8) / 32)
    assert oracle.parse_quote("99-164") == pytest.approx(oracle.parse_quote("99-16+"))


def test_parse_rejects_garbage():
    with pytest.raises(ValueError):
        oracle.parse_quote("9916")
    with pytest.raises(ValueError):
        oracle.parse_quote("99-99")  # 99 >= 32 ticks


# --------------------------------------------------------------------------- #
# Components of the invoice amount
# --------------------------------------------------------------------------- #
def test_clean_value_is_per_100_face():
    # Guards against: clean_value formula without the /100
    assert oracle.clean_value(100_000, "99-16") == pytest.approx(99_500.0)


def test_accrued_uses_semiannual_coupon():
    # Guards against: using the annual coupon instead of half of it.
    # Full-period accrual must equal exactly one semiannual coupon, not the annual one.
    acc = oracle.accrued_interest(100_000, 0.05, 181, 181)
    assert acc == pytest.approx(100_000 * 0.05 / 2)
    assert acc != pytest.approx(100_000 * 0.05)


def test_accrued_scales_linearly_with_days():
    acc_half = oracle.accrued_interest(100_000, 0.05, 90, 180)
    acc_full = oracle.accrued_interest(100_000, 0.05, 180, 180)
    assert acc_half == pytest.approx(acc_full / 2)


def test_zero_days_means_no_accrued():
    assert oracle.accrued_interest(100_000, 0.05, 0, 181) == 0.0


# --------------------------------------------------------------------------- #
# Invoice amount (dirty value)
# --------------------------------------------------------------------------- #
def test_invoice_is_clean_plus_accrued():
    # Guards against: returning the clean value instead of the dirty/invoice value.
    face, cpn, q, d, dp = 100_000, 0.05, "99-16", 90, 181
    clean = oracle.clean_value(face, q)
    acc = oracle.accrued_interest(face, cpn, d, dp)
    inv = oracle.invoice_amount(face, cpn, q, d, dp)
    assert inv == pytest.approx(round(clean + acc, 2))
    assert inv > clean  # dirty strictly exceeds clean when accrued > 0


def test_invoice_rounded_to_cents():
    # Guards against: returning many-decimal or truncated values.
    inv = oracle.invoice_amount(100_000, 0.05, "99-16+", 90, 181)
    assert inv == round(inv, 2)
    assert inv == pytest.approx(100_758.72)


# --------------------------------------------------------------------------- #
# Cross-check: every case in cases.json must reproduce from the oracle.
# --------------------------------------------------------------------------- #
def _load_cases():
    with open(os.path.join(ROOT, "cases.json")) as f:
        return json.load(f)


@pytest.mark.parametrize("case", _load_cases(), ids=lambda c: c["id"])
def test_cases_match_oracle(case):
    got = oracle.invoice_amount(
        case["face_value"],
        case["annual_coupon_rate"],
        case["quote"],
        case["days_since_coupon"],
        case["days_in_coupon_period"],
    )
    assert got == pytest.approx(case["expected_invoice_amount"], abs=0.01)


def test_at_least_ten_cases():
    assert len(_load_cases()) >= 10
