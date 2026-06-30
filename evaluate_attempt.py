"""Evaluate a candidate Treasury-invoice solution against the deterministic cases.

Usage
-----
    python evaluate_attempt.py path/to/attempt.py
    python evaluate_attempt.py path/to/attempt.py --cases cases.json --tol 0.01

The attempt file must define::

    invoice_amount(face_value, annual_coupon_rate, quote,
                   days_since_coupon, days_in_coupon_period)

The evaluator prints every test case (inputs, expected, actual, PASS/FAIL) and
an overall score. A case passes when the attempt's answer is within ``--tol``
(default one cent) of the oracle's expected invoice amount. Exit code is 0 when
every case passes, 1 otherwise, so the script is CI-friendly.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys


def load_attempt(path: str):
    """Import an attempt module from a file path and return its module object."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Attempt file not found: {path}")
    spec = importlib.util.spec_from_file_location("attempt_under_test", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module spec from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "invoice_amount"):
        raise AttributeError(
            f"{path} does not define invoice_amount(face_value, annual_coupon_rate, "
            "quote, days_since_coupon, days_in_coupon_period)"
        )
    return module


def load_cases(path: str):
    with open(path) as f:
        return json.load(f)


def run(attempt_path: str, cases_path: str, tol: float) -> int:
    module = load_attempt(attempt_path)
    cases = load_cases(cases_path)

    # A small epsilon so floating-point noise never sinks a within-tolerance value.
    eps = 1e-9

    print(f"Evaluating: {attempt_path}")
    print(f"Cases:      {cases_path}  ({len(cases)} cases)")
    print(f"Tolerance:  {tol:.2f} (one cent)\n")
    print(f"{'#':>2}  {'case':24s} {'quote':8s} {'expected':>13s} {'actual':>15s}  result")
    print("-" * 78)

    passed = 0
    for i, c in enumerate(cases, 1):
        expected = c["expected_invoice_amount"]
        try:
            actual = module.invoice_amount(
                c["face_value"],
                c["annual_coupon_rate"],
                c["quote"],
                c["days_since_coupon"],
                c["days_in_coupon_period"],
            )
            actual_num = float(actual)
            ok = abs(actual_num - expected) <= tol + eps
            actual_str = f"{actual_num:,.2f}"
        except Exception as exc:  # noqa: BLE001 - report any failure as a failed case
            ok = False
            actual_str = f"ERROR: {type(exc).__name__}"

        if ok:
            passed += 1
        result = "PASS" if ok else "FAIL"
        print(
            f"{i:>2}  {c['id']:24s} {str(c['quote']):8s} "
            f"{expected:>13,.2f} {actual_str:>15s}  {result}"
        )

    total = len(cases)
    pct = (passed / total * 100.0) if total else 0.0
    print("-" * 78)
    print(f"\nSCORE: {passed}/{total} passed ({pct:.1f}%)")
    return 0 if passed == total else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("attempt", help="Path to the attempt .py file under test")
    parser.add_argument("--cases", default="cases.json", help="Path to cases.json")
    parser.add_argument(
        "--tol", type=float, default=0.01, help="Pass tolerance in dollars (default 0.01)"
    )
    args = parser.parse_args(argv)
    return run(args.attempt, args.cases, args.tol)


if __name__ == "__main__":
    sys.exit(main())
