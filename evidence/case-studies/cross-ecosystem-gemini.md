# Case Study — Cross-Ecosystem Gemini

**Status:** observational evidence
**Purpose:** document a real-world interaction that motivated PENURIA's cross-provider framing.

## What was observed

A Gemini App conversation reproduced a familiar interaction pattern: the owner referenced PENURIA's diagnostic tooling and the model responded by discussing the Canary and the broader software-engineering problem around LLM behavior, while the conversation itself remained focused on whether the model would actually perform the requested work.

The accompanying screenshot is preserved as a contemporaneous artifact rather than treated as proof of the model's internal state.

## What this demonstrates

- The problem is not being framed as an OpenAI-only phenomenon.
- Similar owner-facing friction can appear across different AI ecosystems.
- A useful response is to measure observable behavior rather than speculate about hidden infrastructure.
- PENURIA therefore treats providers and models as replaceable test subjects, not adversaries.

## What this does NOT demonstrate

This case study does **not** establish intentional cost-cutting, deliberate degradation, hidden provider policies, or any specific internal mechanism. Those remain hypotheses unless independently verified.

The evidence supports a narrower claim: **the owner can observe a recurring operational pattern and use a portable diagnostic toolkit to measure it.**

## Related tools

- `context_canary.py` — preflight diagnostics
- `matrioshka_de_penuria.py` — controlled/replay experiments
- `script_ruido.py` — stimulus-resilience experiments
- `ANTI_MEGAÑOGRAFO.py` — output-compression compliance
- `penuria_index.py` — aggregate observational metrics
