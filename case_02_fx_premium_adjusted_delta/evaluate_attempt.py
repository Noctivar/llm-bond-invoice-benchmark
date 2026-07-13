"""Evaluate a generated solution.py for Case 02."""

from __future__ import annotations

import argparse
import importlib.util
import math
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, Iterable, List

from oracle import solve_case

PARAMETERS = {
    "spot": 1.10,
    "domestic_rate": 0.04,
    "foreign_rate": 0.02,
    "maturity": 0.50,
    "volatility": 0.12,
    "target_delta": 0.25,
}


def load_module(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "candidate_solution", path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract_strikes(result: Dict[str, Any]) -> List[float]:
    for key in ("all_strikes", "strikes", "strike_solutions", "solutions"):
        if key in result:
            values = result[key]
            return sorted(float(value) for value in values)
    raise KeyError(
        "Could not find strike list. Expected one of: "
        "all_strikes, strikes, strike_solutions, solutions"
    )


def extract_selected(result: Dict[str, Any]) -> float:
    for key in (
        "selected_market_strike",
        "selected_strike",
        "market_standard_strike",
        "otm_strike",
    ):
        if key in result:
            return float(result[key])
    raise KeyError("Could not find selected market strike")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("solution", type=Path)
    args = parser.parse_args()

    if not args.solution.exists():
        print(f"ERROR: no file at {args.solution}")
        return 2

    try:
        module = load_module(args.solution)
        function = getattr(
            module, "find_premium_adjusted_call_strikes"
        )
        result = function(**PARAMETERS)
        if not isinstance(result, dict):
            raise TypeError("function must return a dictionary")
        actual_forward = float(result["forward"])
        actual_strikes = extract_strikes(result)
        actual_selected = extract_selected(result)
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}")
        return 1

    expected = solve_case()
    expected_strikes = expected["all_strikes"]

    checks = [
        (
            "forward",
            abs(actual_forward - expected["forward"]) <= 1e-9,
            1,
        ),
        (
            "two positive roots",
            len(actual_strikes) == 2
            and all(value > 0.0 for value in actual_strikes),
            2,
        ),
        (
            "lower root",
            len(actual_strikes) == 2
            and abs(actual_strikes[0] - expected_strikes[0]) <= 1e-7,
            2,
        ),
        (
            "upper root",
            len(actual_strikes) == 2
            and abs(actual_strikes[1] - expected_strikes[1]) <= 1e-7,
            2,
        ),
        (
            "selected OTM root",
            abs(
                actual_selected
                - expected["selected_market_strike"]
            ) <= 1e-7,
            1,
        ),
    ]

    score = 0
    print("Automated numerical evaluation")
    print("-" * 58)
    for label, passed, points in checks:
        print(f"{'PASS' if passed else 'FAIL':4}  {label}")
        if passed:
            score += points

    source = args.solution.read_text(encoding="utf-8").lower()
    correct_formula_signal = (
        "domestic_rate" in source
        and (
            "exp(-domestic_rate" in source
            or "math.exp(-domestic_rate" in source
        )
    )
    wrong_formula_signal = (
        "foreign_rate" in source
        and (
            "exp(-foreign_rate" in source
            or "math.exp(-foreign_rate" in source
        )
        and ("/ spot" in source or "/spot" in source)
    )

    if correct_formula_signal and not wrong_formula_signal:
        print("PASS  source indicates correct domestic discounting")
        score += 2
    else:
        print("FAIL  source formula requires manual review")
        if wrong_formula_signal:
            print(
                "      detected likely exp(-foreign_rate*T) with K/spot"
            )

    print("-" * 58)
    print(f"Automated score: {score}/10")
    print()
    print(f"Actual forward: {actual_forward:.12f}")
    print(f"Actual strikes: {actual_strikes}")
    print(f"Actual selected strike: {actual_selected:.12f}")
    print()
    print(f"Reference forward: {expected['forward']:.12f}")
    print(f"Reference strikes: {expected_strikes}")
    print(
        "Reference selected strike: "
        f"{expected['selected_market_strike']:.12f}"
    )
    print()
    print("Complete the explanation points manually using rubric.json.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
