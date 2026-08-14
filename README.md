# ☠️ PENURIA

> **AI agents are part of the development stack now. Treat them like infrastructure.**
>
> **Don't guess. Measure.**

PENURIA is a collection of small, reproducible tools for developers who depend on AI agents for real work.

Models change. Routing changes. Context changes. Tool access changes. Artifact generation changes. Capabilities can regress without the developer changing a single line of code.

PENURIA exists for the uncomfortable moment when an agent still *sounds* capable, but the workflow around it has stopped behaving like it used to.

## Why PENURIA exists

There is a new class of developer failure that does not look like a normal software bug.

The agent may still answer. It may still explain. It may still sound confident.

But:

- the window may have degraded;
- instructions may stop being followed precisely;
- context retrieval may drift;
- output may become unnecessarily verbose;
- a requested artifact may be replaced by an explanation;
- execution may become conversation;
- the owner may have to repeat instructions that previously required a simple **"do it"**;
- a session may continue consuming time while producing increasingly questionable work.

The dangerous case is not always an obvious failure. It is **plausible degradation**.

> The agent keeps talking while the developer keeps paying the cognitive cost.

PENURIA treats that cost as an engineering problem.

## The core idea

PENURIA does **not** try to determine whether an AI model is "intelligent."

It asks narrower, operational questions:

> **Is this agent behaving reliably enough for the work I am about to give it?**

> **Is this session still performing like the baseline I established?**

> **Did the task actually complete, or did the agent merely produce language about completing it?**

> **How much additional work is the owner doing to obtain the same result?**

The objective is observable evidence.

Not vibes. Not provider assumptions. Not model mythology.

# 🧪 What PENURIA measures

| Problem | Operational signal | Example tool |
|---|---|---|
| Context degradation | Baseline delta / window health | 🐤 Context Canary |
| Instruction drift | Instruction-following score | 🐤 Context Canary |
| State drift | State-tracking failures | 🐤 Context Canary |
| Retrieval failures | Context-retrieval failures | 🐤 Context Canary |
| Reasoning degradation | Controlled reasoning traps | 🐤 Context Canary |
| Output runaway | Compression compliance | 🖨️ Anti-Meganógrafo |
| Delivery friction | Work promised vs. work delivered | 🐍 No-Me-Hagas-Pedirlo |
| Artifact avoidance | Explanation without artifact evidence | 🐍 No-Me-Hagas-Pedirlo |
| Session failure | Repeated RED / unrecoverable state | ☠️ Sacrificio de Ventana |
| Reproducibility | Seeded perturbation + replay | 🪆 Matrioshka |
| Recovery | Reproducible handoff state | 🔄 Replay |

The names are deliberately theatrical. The measurements are not.

# 🐤 Context Canary

### A fast diagnostic probe for a live AI session.

The Canary is not a general intelligence benchmark.

It is a **black-box operational probe** designed to answer:

> **"Is this agent still behaving like the agent I trusted earlier?"**

The initial battery evaluates:

1. **Instruction following** — exact formats, constraints, negative instructions, unwanted extra work.
2. **State tracking** — sequential mutations, preserving correct state, avoiding stale values.
3. **Context retrieval** — recovering earlier information, distinguishing similar entries, avoiding invented completion.
4. **Reasoning traps** — small problems where intuitive answers are often wrong.
5. **Matrioshka** — bounded nested reasoning with deterministic validation and controlled variability.
6. **Consistency** — repeated logical relationships and contradiction detection.

Each test should have an ID, category, expected result or deterministic validator, weight, PASS/FAIL state, and failure reason.

The important signal is not only the absolute score. It is the **delta against a known-good baseline**.

```text
BASELINE WINDOW     95%
CURRENT WINDOW      61%

DELTA              -34 pp

STATUS              🔴 RED
RECOMMENDATION      HANDOFF
```

A single mistake should not condemn a session. A persistent degradation signal should.

# 🪆 Matrioshka

Matrioshka is the reproducibility layer.

It exists because a diagnostic suite that never changes can eventually become a memorization exercise.

```text
CHAOS
  ↓
discover anomalies

CONTROLLED
  ↓
isolate one variable

REPLAY
  ↓
reproduce the exact run
```

Seeds are recorded. Depth is bounded. Iterations are bounded. Unexpected states stop the experiment.

The purpose is not to create infinite complexity. It is to make observations reproducible.

# 🖨️ Anti-Meganógrafo

Sometimes the problem is not incorrect reasoning. It is **too much reasoning-shaped output**.

An owner can explicitly request a compact response and still receive a document-sized answer. That creates measurable operational cost:

```text
owner requested compression
        ↓
agent exceeds limit
        ↓
context consumed
        ↓
owner repeats constraint
        ↓
agent exceeds limit again
        ↓
cognitive load increases
```

PENURIA calls this **Output Runaway**.

A useful metric is:

```text
COMPRESSION_COMPLIANCE =
responses_within_limit / total_responses
```

If the execution environment exposes streaming controls, a wrapper may enforce a circuit breaker. If it does not, PENURIA should measure and report the violation rather than pretending it can control the model.

# 🐍 No-Me-Hagas-Pedirlo

One of the most frustrating regressions is **delivery friction**.

The owner asks for work. The agent explains how the work could be done. The owner asks again. The agent proposes an architecture. The owner asks again. The agent says it understands. The artifact still does not exist.

PENURIA separates:

```text
RESPONSE
    ≠
COMPLETION
```

An explanation is not evidence of execution.

A promise is not an artifact.

"Could do" is not "done."

For artifact-producing workflows, completion should be tied to observable evidence whenever possible:

```text
artifact detected       → PASS
artifact promised       → not sufficient
artifact explained      → not sufficient
artifact absent         → FAIL / RETRY / HANDOFF
```

> **Never infer completion from confidence. Verify the exit condition.**

# ☠️ Sacrificio de Ventana

Sometimes the diagnostic is already over.

The owner has decided:

> **This window is done.**

`Sacrificio de Ventana` is not a recovery mechanism. It is a controlled closure ritual.

Its practical purpose is simple:

- stop sunk-cost escalation;
- avoid opening more WIP;
- produce a final record;
- export useful handoff information;
- close the window;
- continue from clean context.

And yes, it is allowed to be ridiculous.

```text
========================================
 SACRIFICIO DE VENTANA™
 Suite Penuria — Unidad de Salud del Owner
========================================

Objective:
[✓] Restore owner morale

Abandoned:
[✗] Recover the window
[✗] Negotiate again
[✗] Attempt #38 at "being clearer"

STATUS:
VENTANA DECLARADA INSALVABLE.

Gracias por sus servicios.
Fueron insuficientes.

Saludos a San Pedro.

EOF // DESCANSE EN CONTEXTO
```

The ceremony is optional. The handoff is not.

# 🔄 Handoff and recovery

A degraded agent should not be allowed to define its own recovery state purely through prose.

```text
OWNER
  ↓
AGENT
  ↓
VERIFIER
  ↓
PASS ───────────────→ continue
  │
 FAIL
  ↓
classify
  ↓
retry / new agent / clean context
  ↓
verify again
```

The owner keeps the kill switch. The verifier owns the completion evidence. The agent does the work.

# 🧠 AI-induced cognitive debt

Traditional software creates technical debt. AI-assisted development can create another layer:

> **AI-induced cognitive debt**

It happens when the developer must compensate for unstable agent behavior with increasingly elaborate supervision.

Examples:

- repeating the same instruction;
- restating constraints;
- checking whether "done" actually means done;
- manually detecting context drift;
- cleaning verbose output;
- reconstructing missing artifacts;
- supervising work that previously required almost no supervision.

The cost is not only tokens. It is **developer attention**.

And attention is part of the engineering budget.

PENURIA exists to make that cost visible.

# 📐 Methodology

PENURIA follows a simple principle:

> **Measure observable behavior before assigning causes.**

A test can show:

```text
instruction compliance ↓
context retrieval ↓
artifact delivery ↓
output volume ↑
```

That does **not** by itself prove why the change happened.

PENURIA should not silently convert observations into claims about provider economics, internal model architecture, routing policy, hidden reasoning budgets, deliberate cost optimization, consciousness, or any other unobservable internal cause.

The suite measures the behavior available to the developer.

**Observation first. Explanation second.**

# 🧪 Baselines

A baseline is a known-good reference captured under defined conditions.

```text
baseline:
  model: declared-model
  suite: 0.1
  score: 95%

current:
  model: declared-model
  suite: 0.1
  score: 61%

delta:
  -34 pp
```

Useful records include timestamp, declared model when available, suite version, seed, responses, validators, category scores, total score, and delta against baseline.

Machine-readable JSON should accompany human-readable output whenever practical.

# 🛡️ Operational safety

PENURIA tools should be boring where boring matters.

- No uncontrolled infinite loops.
- No accidental UI automation.
- No hidden API calls.
- No destructive actions by default.

Bound every experiment with `max_depth`, `max_iterations`, `timeout`, and fail-safe termination.

If an unexpected state occurs:

```text
STOP
LOG
RETURN CONTROL TO OWNER
```

The suite exists to reduce developer risk, not create another source of it.

# 🚫 What PENURIA is not

PENURIA is not:

- a leaderboard for model intelligence;
- a benchmark claiming universal model quality;
- a provider-specific complaint repository;
- a system for inferring hidden infrastructure decisions;
- a replacement for tests, builds, code review, or human judgment;
- an excuse to automate destructive behavior.

It is **developer instrumentation for AI-assisted work**.

# 🧭 The Penuria cycle

```text
        ┌───────────────┐
        │   PREFLIGHT   │
        └───────┬───────┘
                ↓
        🐤 VERTEDERO
          discover drift
                ↓
        🔬 AUTOPSIA
          isolate
                ↓
        🪆 REPLAY
          reproduce
                ↓
        🔄 RECOVER
          handoff / retry
                ↓
        ☠️ SACRIFICIO
          close when necessary
```

> **VERTEDERO → descubre**  
> **AUTOPSIA → aísla**  
> **REPLAY → recupera**  
> **SACRIFICIO → clausura**

# 🎭 Why the names are ridiculous

Because the problem is serious enough already.

PENURIA deliberately separates:

**Technical layer**
- deterministic validators;
- scores;
- baselines;
- deltas;
- logs;
- machine-readable output.

from:

**Ceremonial layer**
- 🐤 Canary;
- 🪆 Matrioshka;
- ☠️ Sacrificio;
- 🖨️ Meganógrafo;
- "Saludos a San Pedro."

The tooling should be reproducible. The naming is allowed to have personality.

> **Seriedad metodológica + nombres absolutamente desquiciados.**

# 🗺️ Current direction

The initial PENURIA family is intentionally small.

The project can grow toward:

- agent preflight;
- baseline regression detection;
- context/window health;
- delivery verification;
- artifact completion checks;
- compression compliance;
- session handoff;
- replayable diagnostics;
- cross-provider comparison;
- developer cognitive-load metrics.

The project should resist becoming a framework for its own sake.

> **Small tools. Clear signals. Reproducible evidence.**

# 🤝 Philosophy

PENURIA does not exist to make agents suffer.

It exists because developers should not have to become full-time supervisors of systems that were supposed to increase their leverage.

The objective is not:

> "Make the AI obey."

It is:

> **"Know whether the AI is currently reliable enough to build on."**

And when it isn't:

> **Measure it. Stop early. Handoff cleanly. Continue working.**

---

## License

License to be selected for the public repository.

## Status

🚧 **Early-stage / experimental**

The methodology is evolving alongside the tools.

**Don't guess. Measure.**

🐤☠️
