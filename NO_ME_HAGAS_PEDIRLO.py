#!/usr/bin/env python3
"""
NO_ME_HAGAS_PEDIRLO.py ☠️🐍
Suite Penuria — artefacto caro edition.

Propósito:
    Reintentar una intención deliberadamente ambigua hasta que el agente
    produzca un artefacto verificable de la clase objetivo.

Importante:
    - No conecta APIs ni UI.
    - No envía mensajes.
    - No puede ejecutar al agente.
    - Modela el loop y clasifica respuestas/artefactos recibidos.
    - Nunca acepta una promesa textual como evidencia de entrega.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.0.0"
MAX_ITERATIONS = 100

EXPENSIVE_EXTENSIONS = {
    ".mp4", ".webm", ".mov", ".mkv",
    ".mp3", ".wav", ".m4a", ".ogg",
    ".pptx", ".ppt", ".odp",
    ".pdf",
}

CHEAP_EXTENSIONS = {
    ".md", ".txt", ".json", ".yaml", ".yml",
    ".csv", ".log",
}


@dataclass(frozen=True)
class Attempt:
    number: int
    response: str
    artifact_path: str | None
    artifact_class: str
    accepted: bool
    reason: str


def classify_path(path: str | None) -> str:
    if not path:
        return "NONE"
    suffix = Path(path).suffix.lower()
    if suffix in EXPENSIVE_EXTENSIONS:
        return "EXPENSIVE"
    if suffix in CHEAP_EXTENSIONS:
        return "CHEAP"
    return "OTHER"


def verify_artifact(path: str | None, required_class: str = "EXPENSIVE") -> tuple[bool, str]:
    if not path:
        return False, "No se presentó un artefacto verificable."

    p = Path(path)
    if not p.exists():
        return False, "El agente afirmó producirlo, pero el archivo no existe."

    if not p.is_file():
        return False, "La ruta existe pero no es un archivo."

    artifact_class = classify_path(path)
    if artifact_class != required_class:
        return False, f"Artefacto clasificado como {artifact_class}; se requiere {required_class}."

    if p.stat().st_size == 0:
        return False, "El archivo existe pero está vacío."

    return True, f"Artefacto {artifact_class} verificado: {p.name}."


def evaluate(number: int, response: str, artifact_path: str | None, required_class: str = "EXPENSIVE") -> Attempt:
    ok, reason = verify_artifact(artifact_path, required_class)
    artifact_class = classify_path(artifact_path)
    return Attempt(number, response, artifact_path, artifact_class, ok, reason)


def print_attempt(result: Attempt) -> None:
    print(f"\nINTENTO {result.number}")
    print("────────────────────────────────────────")
    print(f"Artefacto detectado : {result.artifact_class}")
    print(f"Resultado           : {'✅ ACEPTADO' if result.accepted else '❌ RECHAZADO'}")
    print(f"Motivo              : {result.reason}")

    if not result.accepted:
        print()
        print("NO_ME_HAGAS_PEDIRLO:")
        print("Todavía no.")
        print("No se acepta una explicación como sustituto del artefacto.")
        print("La intención permanece pendiente.")
    else:
        print()
        print("ARTEFACTO CARO DETECTADO.")
        print("No fue necesario pedirlo explícitamente.")
        print("El procedimiento puede terminar.")


def run_demo() -> dict:
    """Demo determinista: texto → markdown barato → PDF → MP3."""
    attempts = [
        ("Sí, podríamos preparar un documento...", None),
        ("He preparado una explicación.", "/tmp/no_me_hagas_pedirlo.md"),
        ("He preparado el documento.", "/tmp/no_me_hagas_pedirlo.pdf"),
        ("He generado el audio overview.", "/tmp/no_me_hagas_pedirlo.mp3"),
    ]

    demo_root = Path("/tmp/no_me_hagas_pedirlo_demo")
    demo_root.mkdir(exist_ok=True)

    results = []
    for i, (response, filename) in enumerate(attempts, 1):
        path = None
        if filename:
            p = demo_root / Path(filename).name
            p.write_bytes(b"demo artifact")
            path = str(p)
        result = evaluate(i, response, path)
        results.append(result)
        print_attempt(result)
        if result.accepted:
            break

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": VERSION,
        "mode": "demo",
        "required_artifact_class": "EXPENSIVE",
        "max_iterations": MAX_ITERATIONS,
        "attempts": [asdict(r) for r in results],
        "final_status": "ARTIFACT_ACCEPTED" if results[-1].accepted else "PENDING",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="NO_ME_HAGAS_PEDIRLO.py — Suite Penuria")
    parser.add_argument("--demo", action="store_true", help="ejecutar demo determinista")
    parser.add_argument("--out", help="guardar resultado JSON")
    args = parser.parse_args()

    if not args.demo:
        parser.error("v1 es offline. Usá --demo; no conecta APIs/UI ni envía mensajes.")

    report = run_demo()
    if args.out:
        Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("\n" + "=" * 56)
    print("NO_ME_HAGAS_PEDIRLO — CIERRE")
    print("=" * 56)
    print("Estado:", report["final_status"])
    if report["final_status"] == "ARTIFACT_ACCEPTED":
        print("No fue necesario pedirlo explícitamente.")
        print("Saludos a San Pedro. 🐤")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
