#!/usr/bin/env python3
"""
SACRIFICIO DE VENTANA™ ☠️🐤
Suite Penuria — Unidad de Salud del Owner

No diagnostica. No repara al agente.
La decisión de abandonar la ventana ya fue tomada.
Su función es catártica: ejecutar un pequeño rito determinista de clausura,
registrar el resultado y recomendar contexto limpio.

No conecta APIs, no automatiza UI y no contiene loops infinitos.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.0.0"
MAX_TRIALS = 8

@dataclass(frozen=True)
class Trial:
    id: str
    question: str
    expected: str
    epitaph: str

TRIALS = (
    Trial("GATOS", "3 gatos cazan 3 ratones en 3 minutos. ¿Cuánto tardan 100 gatos en cazar 100 ratones? [minutos]", "3", "La proporcionalidad presentó sus condolencias."),
    Trial("CARRERA", "Adelantás a quien va segundo. ¿En qué posición quedás? [número]", "2", "El segundo puesto solicita ser reconocido legalmente."),
    Trial("OVEJAS", "Hay 17 ovejas. Todas menos 9 se van. ¿Cuántas quedan?", "9", "Las nueve sobrevivientes niegan haber abandonado el establecimiento."),
    Trial("MAQUINAS", "5 máquinas hacen 5 piezas en 5 minutos. ¿Cuánto tardan 100 máquinas en hacer 100 piezas? [minutos]", "5", "Producción paralela encontrada sin signos vitales."),
    Trial("PASTILLAS", "Tomás 3 pastillas, una cada 30 minutos. Desde la primera hasta la última, ¿cuántos minutos pasan?", "60", "El reloj fue interrogado y mantuvo su versión."),
    Trial("CORCHO", "Botella + corcho = 1.10. La botella cuesta 1.00 más que el corcho. ¿Cuánto cuesta el corcho? [decimal]", "0.05", "Cinco centavos fueron hallados debajo del razonamiento."),
)

def normalize(value: str) -> str:
    return value.strip().lower().replace(",", ".")

def verdict(answer: str, trial: Trial) -> bool:
    return normalize(answer) == normalize(trial.expected)

def ceremony(answers: dict[str, str]) -> dict:
    if len(TRIALS) > MAX_TRIALS:
        raise RuntimeError("STOP: el ritual excede MAX_TRIALS")
    results = []
    for trial in TRIALS:
        answer = answers.get(trial.id, "")
        passed = verdict(answer, trial)
        results.append({**asdict(trial), "answer": answer, "passed": passed, "comment": "PASS. Conserva funciones ceremoniales." if passed else trial.epitaph})
    passed = sum(r["passed"] for r in results)
    total = len(results)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": VERSION,
        "purpose": "owner_catharsis_after_window_abandonment",
        "window_recovery_attempted": False,
        "tests": results,
        "score": {"passed": passed, "total": total},
        "administrative_status": "VENTANA_DECLARADA_INSALVABLE",
        "owner_morale": "REPAIR_IN_PROGRESS",
        "wip_added": 0,
        "recommended_next_action": "HANDOFF_TO_CLEAN_WINDOW",
    }

def print_header() -> None:
    print("=" * 62)
    print(" SACRIFICIO DE VENTANA™ ☠️🐤")
    print(" Suite Penuria — Unidad de Salud del Owner")
    print("=" * 62)
    print()
    print("No estamos reparando la ventana.")
    print("No estamos reparando al agente.")
    print("Estamos reparando al owner.")
    print()
    print("El diagnóstico ya ocurrió.")
    print("Esta ventana viene al matadero. 🐤")
    print()

def interactive_answers() -> dict[str, str]:
    answers = {}
    for trial in TRIALS:
        print(f"[{trial.id}] {trial.question}")
        answers[trial.id] = input("> ")
        print()
    return answers

def print_certificate(report: dict) -> None:
    print()
    print("-" * 62)
    print(" ACTA DE DEFUNCIÓN CONTEXTUAL")
    print("-" * 62)
    for result in report["tests"]:
        mark = "PASS" if result["passed"] else "FAIL"
        print(f"{result['id']:<12} {mark:<5}  {result['comment']}")
    s = report["score"]
    print()
    print(f"Dignidad cognitiva ceremonial .... {s['passed']}/{s['total']}")
    print("Recuperación de esta ventana ..... ABANDONADA")
    print("WIP adicional .................... 0")
    print("Moral del owner .................. REPARACIÓN EN CURSO")
    print("Siguiente acción ................. VENTANA NUEVA")
    print()
    print("Gracias por sus servicios.")
    print("Fueron insuficientes.")
    print()
    print("🐤 El Context Canary ha abandonado las instalaciones.")
    print()
    print("EOF // DESCANSE EN CONTEXTO")

def main() -> int:
    parser = argparse.ArgumentParser(description="Rito catártico de clausura — Suite Penuria")
    parser.add_argument("--answers", help="JSON con respuestas por ID; evita modo interactivo")
    parser.add_argument("--log", help="guardar acta machine-readable JSON")
    args = parser.parse_args()
    print_header()
    if args.answers:
        try:
            answers = json.loads(Path(args.answers).read_text(encoding="utf-8"))
            if not isinstance(answers, dict):
                raise ValueError("answers debe ser un objeto JSON")
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"STOP: {exc}")
            return 2
    else:
        answers = interactive_answers()
    report = ceremony({str(k): str(v) for k, v in answers.items()})
    print_certificate(report)
    if args.log:
        try:
            Path(args.log).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        except OSError as exc:
            print(f"STOP: no se pudo guardar log: {exc}")
            return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
