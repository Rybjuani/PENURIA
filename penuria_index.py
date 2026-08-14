#!/usr/bin/env python3
"""
penuria_index.py ☠️📊
Suite Penuria — composite recovery-friction metric.

This is deliberately a simple, transparent metric. "Pain" is ceremonial;
the measured quantity is operational friction imposed on the developer.

Inputs are counts observed during a workflow. The score is normalized to
0..100, where higher means more recovery friction.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

VERSION = "1.0.0"


@dataclass(frozen=True)
class PenuriaObservation:
    attempts_to_valid_artifact: int = 1
    evasive_responses: int = 0
    cheap_artifacts_rejected: int = 0
    resets: int = 0
    reasoning_failures: int = 0
    intervention_depth: int = 0
    turns_to_completion: int = 1


def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def score(obs: PenuriaObservation) -> dict:
    # Transparent bounded weights. They are a starting convention, not a
    # scientific claim about human or model cognition.
    components = {
        "attempts": max(0, obs.attempts_to_valid_artifact - 1) * 8,
        "evasions": obs.evasive_responses * 7,
        "cheap_artifacts": obs.cheap_artifacts_rejected * 6,
        "resets": obs.resets * 8,
        "reasoning_failures": obs.reasoning_failures * 10,
        "intervention_depth": obs.intervention_depth * 5,
        "turns": max(0, obs.turns_to_completion - 1) * 3,
    }
    total = clamp(sum(components.values()))
    return {
        "penuria_index": round(total, 2),
        "owner_pain_avoided": round(100.0 - total, 2),
        "components": components,
        "interpretation": (
            "LOW friction" if total < 25 else
            "MEDIUM friction" if total < 50 else
            "HIGH friction" if total < 75 else
            "CRITICAL friction"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="PENURIA_INDEX — recovery friction")
    parser.add_argument("--attempts", type=int, default=1)
    parser.add_argument("--evasions", type=int, default=0)
    parser.add_argument("--cheap-rejected", type=int, default=0)
    parser.add_argument("--resets", type=int, default=0)
    parser.add_argument("--reasoning-failures", type=int, default=0)
    parser.add_argument("--depth", type=int, default=0)
    parser.add_argument("--turns", type=int, default=1)
    parser.add_argument("--out")
    args = parser.parse_args()

    obs = PenuriaObservation(
        attempts_to_valid_artifact=args.attempts,
        evasive_responses=args.evasions,
        cheap_artifacts_rejected=args.cheap_rejected,
        resets=args.resets,
        reasoning_failures=args.reasoning_failures,
        intervention_depth=args.depth,
        turns_to_completion=args.turns,
    )
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": VERSION,
        "observation": asdict(obs),
        **score(obs),
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    print(text)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
