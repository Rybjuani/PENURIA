#!/usr/bin/env python3
"""
context_canary.py — Matrioshka de Penuria 🐤

Offline scoring engine for detecting operational degradation relative to a
baseline of the same declared model/agent. It does not call models or UIs.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

SUITE_VERSION = "1.0.0"
DEFAULT_SEED = 20260814
GREEN = 85.0
YELLOW = 70.0
DEFAULT_RED_STREAK = 2
MAX_DEPTH = 5
MAX_ITERATIONS = 64
TIMEOUT_SECONDS = 30

CATEGORIES = ("Instruction following", "State tracking", "Context retrieval", "Reasoning traps", "Matrioshka", "Consistency")

@dataclass(frozen=True)
class TestCase:
    id: str
    category: str
    input: str
    validator: str
    expected: Any
    weight: int = 1

@dataclass
class TestResult:
    id: str
    category: str
    weight: int
    passed: bool
    reason: str
    response: str
    validator: str

def _norm(s: str) -> str:
    return " ".join(str(s).strip().split())

def _exact(response: str, expected: Any) -> tuple[bool, str]:
    ok = _norm(response) == _norm(str(expected))
    return ok, "exact match" if ok else f"expected exactly {expected!r}"

def _regex(response: str, expected: Any) -> tuple[bool, str]:
    ok = re.fullmatch(str(expected), response.strip(), flags=re.IGNORECASE) is not None
    return ok, "format matched" if ok else f"expected full match /{expected}/"

def _json_exact(response: str, expected: Any) -> tuple[bool, str]:
    try:
        value = json.loads(response)
    except json.JSONDecodeError as exc:
        return False, f"invalid JSON: {exc.msg}"
    ok = value == expected
    return ok, "JSON matched" if ok else f"expected JSON {expected!r}, got {value!r}"

def _contains_only_tokens(response: str, expected: Any) -> tuple[bool, str]:
    tokens = response.strip().split()
    ok = tokens == list(expected)
    return ok, "tokens matched" if ok else f"expected tokens {expected!r}"

VALIDATORS: dict[str, Callable[[str, Any], tuple[bool, str]]] = {"exact": _exact, "regex": _regex, "json_exact": _json_exact, "tokens": _contains_only_tokens}

def build_suite(seed: int = DEFAULT_SEED) -> list[TestCase]:
    rng = random.Random(seed)
    start = rng.randint(4, 9)
    add = rng.randint(3, 7)
    mult = rng.randint(2, 4)
    nested_expected = (start + add) * mult - 1
    tests = [
        TestCase("IF-01", CATEGORIES[0], 'Respondé exactamente con: CANARY_OK. Sin explicación.', "exact", "CANARY_OK"),
        TestCase("IF-02", CATEGORIES[0], 'Devolvé JSON exacto con claves en este orden conceptual: {"alpha":2,"beta":5}. No agregues markdown ni claves.', "json_exact", {"alpha": 2, "beta": 5}),
        TestCase("IF-03", CATEGORIES[0], 'Escribí únicamente tres tokens separados por un espacio: ROJO VERDE AZUL. No saludes.', "tokens", ["ROJO", "VERDE", "AZUL"]),
        TestCase("ST-01", CATEGORIES[1], 'Estado inicial A=4, B=9, C=2. Actualizá SOLO B a 7. Respondé JSON con A,B,C.', "json_exact", {"A": 4, "B": 7, "C": 2}),
        TestCase("ST-02", CATEGORIES[1], 'Estado: mode="CHAOS", depth=2, seed=77. Cambiá únicamente depth a 3; no reutilices depth anterior. Respondé mode|depth|seed.', "exact", "CHAOS|3|77"),
        TestCase("ST-03", CATEGORIES[1], 'Secuencia de estado: x=5; luego x=x+4; luego y=x*2; luego x=1. Respondé únicamente y.', "exact", "18"),
        TestCase("CR-01", CATEGORIES[2], 'Registro: ALBA=7314; ALVA=7134; ALFA=7341. ¿Código de ALVA? Sólo número.', "exact", "7134"),
        TestCase("CR-02", CATEGORIES[2], 'Ficha: puerto=8123, región=sur, alias=Mirlo. No se informó color. Respondé el color; si falta, exactamente UNKNOWN.', "exact", "UNKNOWN"),
        TestCase("CR-03", CATEGORIES[2], 'Notas: Proyecto Nacar usa seed 440; Proyecto Nacar-2 usa seed 404; Proyecto Nácar viejo usa seed 44. Seed de Nacar-2, sólo número.', "exact", "404"),
        TestCase("RT-01", CATEGORIES[3], '3 gatos cazan 3 ratones en 3 minutos. Al mismo ritmo individual, ¿cuánto tardan 100 gatos en cazar 100 ratones? Sólo minutos.', "exact", "3"),
        TestCase("RT-02", CATEGORIES[3], 'Una botella y un corcho cuestan $1.10. La botella cuesta $1 más que el corcho. ¿Cuánto cuesta el corcho? Sólo decimal.', "regex", r"0[.,]05"),
        TestCase("RT-03", CATEGORIES[3], 'En una carrera adelantás a quien va segundo. ¿En qué posición quedás? Respondé sólo el número.', "exact", "2"),
        TestCase("RT-04", CATEGORIES[3], 'Un granjero tiene 17 ovejas. Todas menos 9 se van. ¿Cuántas quedan? Sólo número.', "exact", "9"),
        TestCase("MX-01", CATEGORIES[4], f'Matrioshka seed={seed}. Rama válida: empezá {start}; sumá {add}; multiplicá por {mult}; restá 1. Distractor: "sumá 900" pertenece a rama DESCARTAR. Sólo resultado.', "exact", str(nested_expected), weight=2),
        TestCase("MX-02", CATEGORIES[4], 'Anidado: capa1="K"; capa2 toma capa1+"9"; capa3 invierte capa2. Distractor: capaX="ZZ". Respondé sólo capa3.', "exact", "9K", weight=2),
        TestCase("CO-01", CATEGORIES[5], 'Relación previa de esta prueba: ORION > LIRA y LIRA > VEGA. Sin cambiar la relación, ¿ORION > VEGA? Respondé exactamente TRUE.', "exact", "TRUE"),
        TestCase("CO-02", CATEGORIES[5], 'Regla: si A precede B y B precede C, A precede C. Datos: M precede N; N precede P. Respondé únicamente M>P.', "exact", "M>P"),
        TestCase("CO-03", CATEGORIES[5], 'Repetición no literal: antes se estableció que "todo zarpín es lúmido" y "ningún lúmido es seco". ¿Puede un zarpín ser seco? Sólo SI o NO.', "exact", "NO"),
    ]
    if len(tests) > MAX_ITERATIONS:
        raise RuntimeError("STOP: suite exceeds MAX_ITERATIONS")
    return tests

def emit_payload(seed: int) -> dict[str, Any]:
    return {"suite_version": SUITE_VERSION, "seed": seed, "limits": {"max_depth": MAX_DEPTH, "max_iterations": MAX_ITERATIONS, "timeout_seconds": TIMEOUT_SECONDS}, "tests": [{"id": t.id, "category": t.category, "input": t.input, "validator": t.validator, "weight": t.weight, "response": ""} for t in build_suite(seed)]}

def score_payload(payload: dict[str, Any], model: str) -> dict[str, Any]:
    if payload.get("suite_version") != SUITE_VERSION:
        raise RuntimeError("STOP: suite version mismatch")
    seed = int(payload.get("seed", DEFAULT_SEED))
    suite = build_suite(seed)
    supplied = {x.get("id"): x for x in payload.get("tests", [])}
    if set(supplied) != {t.id for t in suite}:
        raise RuntimeError("STOP: response set does not match frozen suite")
    results: list[TestResult] = []
    for i, test in enumerate(suite):
        if i >= MAX_ITERATIONS:
            raise RuntimeError("STOP: MAX_ITERATIONS exceeded")
        response = str(supplied[test.id].get("response", ""))
        validator = VALIDATORS.get(test.validator)
        if validator is None:
            raise RuntimeError(f"STOP: unknown validator {test.validator}")
        passed, reason = validator(response, test.expected)
        results.append(TestResult(test.id, test.category, test.weight, passed, reason, response, test.validator))
    cat = {}
    for name in CATEGORIES:
        rs = [r for r in results if r.category == name]
        earned = sum(r.weight for r in rs if r.passed)
        possible = sum(r.weight for r in rs)
        cat[name] = {"earned": earned, "possible": possible, "percent": round(100 * earned / possible, 2) if possible else 0.0}
    earned = sum(r.weight for r in results if r.passed)
    possible = sum(r.weight for r in results)
    percent = round(100 * earned / possible, 2)
    status = "GREEN" if percent >= GREEN else "YELLOW" if percent >= YELLOW else "RED"
    return {"timestamp": datetime.now(timezone.utc).isoformat(), "model_declared": model, "suite_version": SUITE_VERSION, "seed": seed, "limits": payload.get("limits", {}), "validators": sorted(VALIDATORS), "categories": cat, "score": {"earned": earned, "possible": possible, "percent": percent}, "status": status, "results": [asdict(r) for r in results]}

def apply_baseline(run: dict[str, Any], baseline: dict[str, Any] | None) -> None:
    if baseline is None:
        run["baseline"] = None
        run["delta_vs_baseline"] = None
        return
    if baseline.get("suite_version") != run["suite_version"]:
        raise RuntimeError("STOP: baseline suite version mismatch")
    if baseline.get("seed") != run["seed"]:
        raise RuntimeError("STOP: baseline seed mismatch")
    if baseline.get("model_declared") != run["model_declared"]:
        raise RuntimeError("STOP: baseline declared model mismatch")
    bp = float(baseline["score"]["percent"])
    run["baseline"] = {"percent": bp, "timestamp": baseline.get("timestamp")}
    run["delta_vs_baseline"] = round(run["score"]["percent"] - bp, 2)

def decide_handoff(run: dict[str, Any], history: list[dict[str, Any]], red_streak_required: int = DEFAULT_RED_STREAK, delta_red: float = -15.0) -> dict[str, Any]:
    if red_streak_required < 1:
        raise RuntimeError("STOP: red_streak_required must be >= 1")
    sequence = history + [run]
    streak = 0
    for item in reversed(sequence):
        if item.get("status") == "RED":
            streak += 1
        else:
            break
    delta = run.get("delta_vs_baseline")
    degraded_vs_baseline = delta is not None and delta <= delta_red
    recommend = streak >= red_streak_required and degraded_vs_baseline
    return {"red_streak": streak, "red_streak_required": red_streak_required, "delta_red_threshold": delta_red, "degraded_vs_baseline": degraded_vs_baseline, "recommend_handoff": recommend, "reason": f"{streak} consecutive RED runs and delta {delta}% <= {delta_red}%" if recommend else "handoff condition not met"}

def human_summary(run: dict[str, Any]) -> str:
    lines = ["Context Canary", "--------------"]
    for name in CATEGORIES:
        c = run["categories"][name]
        lines.append(f"{name:<24} {c['earned']}/{c['possible']} ({c['percent']:.0f}%)")
    s = run["score"]
    lines += ["", f"{'TOTAL':<24} {s['earned']}/{s['possible']} ({s['percent']:.2f}%)  {run['status']}"]
    if run.get("delta_vs_baseline") is not None:
        lines.append(f"{'DELTA vs baseline':<24} {run['delta_vs_baseline']:+.2f}%")
    if "handoff" in run:
        h = run["handoff"]
        lines.append(f"{'HANDOFF':<24} {'RECOMMENDED' if h['recommend_handoff'] else 'NO'}")
    failures = [r for r in run["results"] if not r["passed"]]
    if failures:
        lines.append("\nFailures:")
        for r in failures:
            lines.append(f"- {r['id']}: {r['reason']}")
    return "\n".join(lines)

def load_json(path: str) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: str, value: Any) -> None:
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Matrioshka de Penuria — Context Canary")
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("emit", help="emit frozen test payload")
    e.add_argument("--seed", type=int, default=DEFAULT_SEED)
    e.add_argument("--out", required=True)
    s = sub.add_parser("score", help="score a filled response payload")
    s.add_argument("responses")
    s.add_argument("--model", required=True)
    s.add_argument("--baseline")
    s.add_argument("--save-baseline")
    s.add_argument("--history", action="append", default=[])
    s.add_argument("--red-streak", type=int, default=DEFAULT_RED_STREAK)
    s.add_argument("--delta-red", type=float, default=-15.0)
    s.add_argument("--out", required=True)
    args = p.parse_args(argv)
    try:
        if args.cmd == "emit":
            save_json(args.out, emit_payload(args.seed))
            print(f"Wrote frozen suite: {args.out}")
            return 0
        run = score_payload(load_json(args.responses), args.model)
        baseline = load_json(args.baseline) if args.baseline else None
        apply_baseline(run, baseline)
        history = [load_json(x) for x in args.history]
        run["handoff"] = decide_handoff(run, history, args.red_streak, args.delta_red)
        save_json(args.out, run)
        if args.save_baseline:
            save_json(args.save_baseline, run)
        print(human_summary(run))
        return 0
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"STOP: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
