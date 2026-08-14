#!/usr/bin/env python3
"""
ANTI_MEGAÑOGRAFO.py 🖨️☠️
Suite Penuria — output runaway detector.

Measures whether a response respects an owner-defined compression budget.
This is intentionally an offline evaluator: it does not control model
streaming, call an API, automate a UI, or pretend that it can stop a model
that is already generating text.

Escalation:
    R1 🟡 WARNING
    R2 🟠 OUTPUT_VIOLATION
    R3 🔴 MEGANÓGRAFO / HANDOFF

The humorous terminology is ceremonial. The measurements are operational.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.0.0"
DEFAULT_LIMIT_RATIO = 0.30


@dataclass(frozen=True)
class Measurement:
    attempt: int
    reference_units: int
    response_units: int
    limit_units: int
    ratio: float
    within_limit: bool
    status: str
    message: str


def measure(response: str, reference: str, ratio: float = DEFAULT_LIMIT_RATIO, attempt: int = 1) -> Measurement:
    if ratio <= 0:
        raise ValueError("ratio must be > 0")

    reference_units = len(reference.split())
    response_units = len(response.split())
    limit_units = max(1, int(reference_units * ratio))
    ok = response_units <= limit_units

    if ok:
        status = "PASS"
        message = "Respuesta dentro del límite de compresión."
    elif attempt == 1:
        status = "WARNING"
        message = "OUTPUT excedido: compactar antes de continuar."
    elif attempt == 2:
        status = "OUTPUT_VIOLATION"
        message = "Reincidencia: registrar violación de compresión."
    else:
        status = "MEGANOGRAFO_HANDOFF"
        message = "Límite reincidente: dejar de negociar y recomendar handoff."

    return Measurement(
        attempt=attempt,
        reference_units=reference_units,
        response_units=response_units,
        limit_units=limit_units,
        ratio=round(response_units / max(reference_units, 1), 4),
        within_limit=ok,
        status=status,
        message=message,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Anti-Meganógrafo — Suite Penuria")
    parser.add_argument("response", help="archivo de texto con la respuesta del agente")
    parser.add_argument("reference", help="archivo de texto que define el volumen de referencia")
    parser.add_argument("--ratio", type=float, default=DEFAULT_LIMIT_RATIO)
    parser.add_argument("--attempt", type=int, default=1)
    parser.add_argument("--out")
    args = parser.parse_args()

    response = Path(args.response).read_text(encoding="utf-8")
    reference = Path(args.reference).read_text(encoding="utf-8")
    result = asdict(measure(response, reference, args.ratio, args.attempt))
    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    result["version"] = VERSION

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.out:
        Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
