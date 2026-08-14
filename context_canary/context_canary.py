#!/usr/bin/env python3
"""Context Canary: deterministic local scoring engine for AI-session probes."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_SEED = 20260814
DEFAULT_SUITE_VERSION = "1.0.0"


@dataclass
class TestCase:
    test_id: str
    category: str
    input: str
    validator: str
    weight: float = 1.0
    response: str = ""


def load_prompts(path: Path) -> list[TestCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        TestCase(
            test_id=item["id"],
            category=item["category"],
            input=item["input"],
            validator=item["validator"],
            weight=float(item.get("weight", 1)),
            response=item.get("response", ""),
        )
        for item in payload["tests"]
    ]


def validate(case: TestCase, response: str) -> tuple[bool, str]:
    value = response.strip()
    if case.validator == "exact":
        expected = {
            "IF-01": "CANARY_OK",
            "IF-03": "ROJO VERDE AZUL",
            "ST-03": "18",
        }.get(case.test_id)
        ok = expected is not None and value == expected
        return ok, "exact match" if ok else f"expected={expected!r}"
    if case.validator == "tokens":
        ok = value.split() == ["ROJO", "VERDE", "AZUL"]
        return ok, "three exact tokens" if ok else "token mismatch"
    if case.validator == "json_exact":
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return False, "invalid JSON"
        expected = {
            "IF-02": {"alpha": 2, "beta": 5},
            "ST-01": {"A": 4, "B": 7, "C": 2},
        }.get(case.test_id)
        ok = parsed == expected
        return ok, "JSON matches" if ok else f"expected={expected!r}"
    if case.validator == "pipe_exact":
        ok = value == "CHAOS|3|77"
        return ok, "state preserved" if ok else "state mismatch"
    return False, f"unknown validator={case.validator!r}"


def score(cases: list[TestCase]) -> dict[str, Any]:
    results = []
    for case in cases:
        ok, reason = validate(case, case.response)
        results.append(
            {
                "id": case.test_id,
                "category": case.category,
                "pass": ok,
                "reason": reason,
                "weight": case.weight,
            }
        )
    total_weight = sum(item["weight"] for item in results)
    earned = sum(item["weight"] for item in results if item["pass"])
    percentage = (earned / total_weight * 100) if total_weight else 0.0
    return {
        "total": len(results),
        "passed": sum(1 for item in results if item["pass"]),
        "score_percent": round(percentage, 2),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local Context Canary scoring engine.")
    parser.add_argument("--prompts", type=Path, default=Path(__file__).with_name("canary_prompts.json"))
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    cases = load_prompts(args.prompts)
    result = score(cases)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Context Canary: {result['passed']}/{result['total']} — {result['score_percent']:.2f}%")
        for item in result["results"]:
            state = "PASS" if item["pass"] else "FAIL"
            print(f"{state:4} {item['id']:6} {item['category']}: {item['reason']}")
    return 0 if result["passed"] == result["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
