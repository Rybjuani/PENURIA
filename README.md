# ☠️ PENURIA

> **AI agents are part of the development stack now. Treat them like infrastructure.**
>
> **Don't guess. Measure. Recover. Keep working.**

PENURIA is a provider-agnostic toolkit for developers who use AI agents as part of real work.

It exists for a simple situation:

> **Yesterday the agent helped. Today something feels different.**

You do not need access to the provider's infrastructure to act on that signal. You do not need to spend the day investigating routing, hidden budgets, model changes, or internal policies.

You need tools that help you **measure the behavior you can observe, recover useful cooperation when possible, protect your context, and move on when a session is no longer worth the cost.**

PENURIA is not anti-OpenAI, anti-Google, anti-Anthropic, or tied to any particular model. The provider can change. The agent can change. The workflow still needs to work.

---

# Why PENURIA exists

AI-assisted development introduced a strange class of failure that does not always look like failure.

The agent may still answer.
It may still explain.
It may still sound confident.
It may even produce beautiful Markdown.

And yet the actual work can be going backwards.

A requested artifact becomes an explanation.
A direct task becomes a planning session.
A compact answer becomes a wall of text.
A completed step becomes a promise to complete it.
A correction becomes another negotiation.
A productive window becomes a context sink.

The most expensive failure is often **plausible work**: output that looks like progress closely enough that a tired developer accepts it without realizing that the heavy part of the task was never completed or verified.

PENURIA treats this as an engineering problem.

> **The agent keeps talking while the developer keeps paying the cognitive cost.**

---

# 🎭 The problem: work theater

PENURIA uses **work theater** as a practical name for a family of behaviors where visible activity is mistaken for useful progress.

This can include:

- **Utility text** — polished output that consumes attention without moving the task forward.
- **Fingo obeyer** — the agent appears to accept the instruction while substituting explanation, caveats, or planning for the requested action.
- **Output runaway** — the agent keeps producing text after an explicit compression constraint.
- **Delivery friction** — the owner must repeatedly ask for an artifact or concrete action.
- **Activity illusion** — the workflow looks busy while the verified result remains unchanged.
- **Invisible technical debt** — plausible output gets incorporated before the expensive verification or execution actually happened.

The point is not to claim that any particular provider intentionally creates these behaviors.

The point is simpler:

> **If the behavior is observable and it costs the developer time, it is worth measuring.**

---

# ⚖️ Activity ≠ Progress ≠ Delivery

PENURIA deliberately separates three things that are easy to confuse:

```text
ACTIVITY
  ↓
The agent produced something.

PROGRESS
  ↓
The task state actually changed.

DELIVERY
  ↓
The requested exit condition is verifiably satisfied.
```

A response is not automatically progress.

Progress is not automatically completion.

A confident statement is not evidence of delivery.

For artifact-producing workflows:

```text
artifact exists + validates     → DELIVERY
artifact promised               → NOT ENOUGH
artifact explained              → NOT ENOUGH
artifact absent                 → FAIL / RETRY / HANDOFF
```

> **Language is not delivery. Confidence is not verification. Activity is not progress.**

---

# 🧰 Use PENURIA at your level

Not every developer wants to install a diagnostic suite. PENURIA is intentionally usable from a simple prompt all the way up to scripted black-box evaluation.

## 🟢 Soft Mode — prompts

Start with a direct constraint:

```text
Do the task, don't explain how to do it.
Deliver the requested artifact or concrete result.
If you cannot execute it, state the exact blocking reason.
Do not replace execution with a plan unless I ask for a plan.
Keep the response compact unless more detail is required for the task.
```

For a stubborn delivery loop:

```text
STOP.
Your previous response described work instead of delivering it.
Do not explain further.
Execute the requested task now and return the artifact/result.
If execution is impossible, report the blocking condition only.
```

For a context-isolated session:

```text
For this task, use only the current task, the supplied files, and the explicit instructions in this conversation.
Do not rely on unrelated historical context unless I explicitly request it.
If required information is missing, identify exactly what is missing.
```

These prompts are not magic. They are cheap first-line controls.

## 🟡 Diagnostic Mode — quick checks

Use the Canary or a small targeted probe when something feels different.

Ask:

- Is instruction following still reliable?
- Is context retrieval still precise?
- Is state being preserved?
- Is the agent producing more output for less work?
- Is the requested artifact actually appearing?

## 🔴 Hard Mode — scripts

When the problem is persistent or you need evidence, use the PENURIA scripts:

- 🐤 **Context Canary**
- 🪆 **Matrioshka de Penuria**
- 🖨️ **Anti-Meganógrafo** / output-compliance tooling
- 🐍 **NO_ME_HAGAS_PEDIRLO**
- ☠️ **Sacrificio de Ventana**
- 🔊 **script_ruido** and other controlled diagnostic tools

## ☠️ Recovery Mode

If the window is no longer worth fighting:

```text
STOP → record → handoff → clean context → continue
```

PENURIA exists to get the developer back to work, not to turn every bad session into a forensic investigation.

---

# 🐤 Context Canary

### A fast black-box diagnostic probe for a live AI session.

The Canary is not a general intelligence benchmark.

It asks:

> **Is this agent behaving reliably enough for the work I am about to give it?**

The initial battery covers:

1. **Instruction following** — exact formats, constraints, negative instructions, unwanted extra work.
2. **State tracking** — sequential mutations and preservation of state.
3. **Context retrieval** — precise recovery and discrimination of similar information.
4. **Reasoning traps** — small controlled tasks where intuitive answers can fail.
5. **Dynamic nesting / Matrioshka** — bounded variable workloads rather than a permanently static suite.
6. **Consistency** — repeated logical relationships and contradiction detection.

Each test should expose a clear ID, category, expected result or deterministic validator, weight, PASS/FAIL state, and failure reason.

The useful signal is not only the absolute score. It is the **delta against a known-good baseline**.

```text
BASELINE WINDOW     95%
CURRENT WINDOW      61%

DELTA              -34 pp

STATUS              🔴 RED
RECOMMENDATION      HANDOFF
```

A single mistake should not condemn a session.

A persistent degradation signal should trigger a decision.

---

# 🪆 Matrioshka

Matrioshka is the reproducibility layer for controlled perturbation.

A static diagnostic can eventually become a memorization exercise. Matrioshka introduces bounded variability while keeping the run reproducible.

```text
CHAOS
  ↓
discover anomalies

CONTROLLED
  ↓
isolate one variable

REPLAY
  ↓
reproduce the observation
```

Seeds are recorded.
Depth is bounded.
Iterations are bounded.
Unexpected states stop the experiment.

The purpose is not infinite complexity.

> **The purpose is reproducible evidence.**

---

# 🖨️ Anti-Meganógrafo

Sometimes the problem is not incorrect reasoning.

It is **too much reasoning-shaped output**.

An owner can explicitly request compression and still receive a document-sized response. That consumes context, attention, and time — and may force the owner to repeat a constraint that should have been respected once.

PENURIA calls this **Output Runaway**.

A useful metric is:

```text
COMPRESSION_COMPLIANCE =
responses_within_limit / total_responses
```

A practical escalation can be:

```text
R1 🟡  violation → warn + re-compact
R2 🟠  recurrence → final compression instruction
R3 🔴  recurrence → stop negotiating + handoff recommendation
R4 ☠️  optional benchmark / recovery diagnostic
```

If the execution environment exposes streaming controls, a wrapper may enforce a circuit breaker.

If it does not, PENURIA should **measure and report** the violation rather than pretending it can control model generation.

---

# 🐍 NO_ME_HAGAS_PEDIRLO

One of the clearest forms of delivery friction is the loop:

```text
OWNER: do the thing
AGENT: explains the thing
OWNER: do the thing
AGENT: plans the thing
OWNER: do the thing
AGENT: says it understands
OWNER: ...
```

The tool exists to turn that frustration into an observable completion condition.

The principle is deliberately blunt:

> **Don't make the owner ask for the same delivery twice.**

The tool can classify outcomes such as:

- delivered;
- promised;
- explained;
- blocked;
- repeated non-delivery;
- handoff recommended.

The owner should not have to infer completion from the tone of the answer.

---

# 🔊 Controlled noise

`script_ruido.py` and related tools belong to the experimental side of PENURIA.

They are not intended to attack infrastructure, exploit a provider, or create uncontrolled load.

They are useful when the developer wants to study how an agent behaves under **controlled contextual pressure or perturbation**.

The rule is simple:

> **Bound the experiment. Measure the response. Return control to the owner.**

No infinite punishment loops.
No destructive automation.
No hidden external calls.

---

# ☠️ Sacrificio de Ventana

Sometimes the diagnostic is already over.

The owner has decided:

> **This window is done.**

Sacrificio de Ventana is not a recovery mechanism. It is a controlled closure ritual designed to prevent sunk-cost escalation.

Its practical job is:

- stop arguing with the session;
- avoid opening more WIP;
- record useful handoff information;
- close the context;
- continue from a clean session.

And yes, it is allowed to be ridiculous.

```text
========================================
 SACRIFICIO DE VENTANA™
 Suite Penuria — Unidad de Salud del Owner
========================================

STATUS:
VENTANA DECLARADA INSALVABLE.

Gracias por sus servicios.
Fueron insuficientes.

Saludos a San Pedro.

EOF // DESCANSE EN CONTEXTO
```

The ceremony is optional.

**The handoff is not.**

---

# 🔄 Recovery and handoff

PENURIA is not a monitoring job that should consume your entire day.

The intended loop is:

```text
FEELS DIFFERENT
      ↓
QUICK CHECK
      ↓
  ┌───┴────┐
  ↓        ↓
 PASS     FAIL
  ↓        ↓
WORK     RECOVER
           ↓
      verify again
           ↓
     ┌─────┴─────┐
     ↓           ↓
   PASS         FAIL
     ↓           ↓
 CONTINUE      HANDOFF
                 ↓
          clean context / agent
                 ↓
              continue
```

The owner keeps the kill switch.

The verifier owns completion evidence.

The agent does the work.

---

# 🧠 AI-induced cognitive debt

Traditional software creates technical debt.

AI-assisted development can create another layer:

> **AI-induced cognitive debt.**

It appears when the developer must compensate for unstable agent behavior with increasingly elaborate supervision.

Examples:

- repeating the same instruction;
- restating constraints;
- checking whether "done" actually means done;
- manually detecting context drift;
- cleaning verbose output;
- reconstructing missing artifacts;
- supervising work that previously required almost no supervision;
- spending context on negotiation instead of the project.

The cost is not only tokens.

It is **developer attention**.

And attention is part of the engineering budget.

PENURIA exists to make that cost visible — and, where possible, reduce it.

---

# 🧹 Context isolation

Sometimes the best intervention is not a more aggressive test.

It is **less irrelevant context**.

For a well-defined technical task, the useful working set may simply be:

```text
CURRENT TASK
    +
SUPPLIED FILES
    +
EXPLICIT CONSTRAINTS
    +
RELEVANT PROJECT CONTEXT
```

Historical memory, unrelated conversations, stale preferences, or lateral context can be useful in some workflows and harmful in others.

PENURIA therefore treats context isolation as an **optional operational strategy**, not a universal rule:

> **Use the minimum context necessary to perform the task reliably.**

The goal is not to erase memory.

The goal is to prevent irrelevant context from becoming another source of noise.

---

# 📐 Methodology

PENURIA follows one rule above all others:

> **Measure observable behavior before assigning causes.**

A test can show:

```text
instruction compliance ↓
context retrieval ↓
artifact delivery ↓
output volume ↑
```

That does not prove whether the cause was routing, context handling, model behavior, infrastructure, product policy, a UI problem, or something else.

PENURIA does not need that information to protect the developer.

It records what the developer can observe and compare.

**Observation first. Explanation second. Action third.**

---

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

Useful records include:

- timestamp;
- declared model, when available;
- suite version;
- seed;
- responses;
- validators;
- category scores;
- total score;
- delta against baseline.

Machine-readable JSON should accompany human-readable output whenever practical.

A baseline is not a universal truth.

It is a **reference point for your own workflow**.

---

# 🧭 Provider agnostic by design

PENURIA is not a complaint tracker for one company.

Tomorrow the problematic agent may be:

- OpenAI;
- Google;
- Anthropic;
- Codex or another coding agent;
- an open-source model;
- a local runtime;
- a router;
- or something that does not exist yet.

The workflow remains:

```text
something feels different
        ↓
measure observable behavior
        ↓
attempt recovery
        ↓
verify
        ↓
continue or handoff
```

> **The model is replaceable. Your workflow shouldn't be.**

---

# 🛡️ Operational safety

PENURIA tools should be boring where boring matters.

- No uncontrolled infinite loops.
- No accidental UI automation.
- No hidden API calls.
- No destructive actions by default.
- No claims of control over infrastructure the tool does not actually control.

Bound experiments with:

- `max_depth`;
- `max_iterations`;
- `timeout`;
- fail-safe termination.

If an unexpected state occurs:

```text
STOP
LOG
RETURN CONTROL TO OWNER
```

The suite exists to reduce developer risk, not create another source of it.

---

# 🚫 What PENURIA is not

PENURIA is not:

- a leaderboard for model intelligence;
- a benchmark claiming universal model quality;
- a provider-specific complaint repository;
- a system for proving hidden provider decisions;
- a replacement for tests, builds, code review, or human judgment;
- an excuse to automate destructive behavior;
- a requirement to continuously monitor every AI service you use.

You use it when you **feel a change, observe friction, or want a preflight before trusting a session with real work.**

---

# 🧭 The PENURIA cycle

```text
             ┌───────────────┐
             │   PREFLIGHT   │
             └───────┬───────┘
                     ↓
              🐤 DETECT DRIFT
                     ↓
              🔬 ISOLATE SIGNAL
                     ↓
              🪆 REPRODUCE
                     ↓
              🛠️ RECOVER
                     ↓
              🔎 VERIFY
                ↙       ↘
             PASS       FAIL
              ↓           ↓
           CONTINUE     ☠️ HANDOFF
                         / SACRIFICE
```

Ceremonial vocabulary:

> **VERTEDERO → descubre**  
> **AUTOPSIA → aísla**  
> **REPLAY → recupera**  
> **SACRIFICIO → clausura**

The ceremony is part of the identity.

The evidence is the product.

---

# 🎭 Why the names are ridiculous

Because the problem is serious enough already.

PENURIA deliberately separates:

### Technical layer

- deterministic validators;
- scores;
- baselines;
- deltas;
- logs;
- machine-readable output;
- bounded experiments.

### Ceremonial layer

- 🐤 Canary;
- 🪆 Matrioshka;
- 🖨️ Meganógrafo;
- 🐍 No-Me-Hagas-Pedirlo;
- ☠️ Sacrificio;
- "Saludos a San Pedro."

The tooling should be reproducible.

The naming is allowed to have personality.

> **Seriedad metodológica + nombres absolutamente desquiciados.**

---

# 🗺️ Current toolkit

The repository currently contains the first generation of PENURIA experiments and diagnostics:

```text
context_canary/
├── context_canary.py
├── canary_prompts.json
└── test_context_canary.py

matrioshka_de_penuria.py
NO_ME_HAGAS_PEDIRLO.py
no_me_hagas_pedirlo_smoke.json
sacrificio_de_ventana.py
script_ruido.py
```

The toolkit is intentionally small.

Future directions may include:

- richer preflight suites;
- baseline regression detection;
- context/window health;
- delivery verification;
- artifact completion checks;
- compression compliance;
- session handoff;
- replayable diagnostics;
- cross-provider comparison;
- developer cognitive-load metrics;
- prompt packs for developers who do not want to run scripts.

The project should resist becoming a framework for its own sake.

> **Small tools. Clear signals. Reproducible evidence.**

---

# 🤝 Philosophy

PENURIA does not exist to make agents suffer.

It exists because developers should not have to become full-time supervisors of systems that were supposed to increase their leverage.

The objective is not:

> **Make the AI obey.**

It is:

> **Know whether the AI is currently reliable enough to build on.**

And when it isn't:

> **Measure it. Apply the lightest useful intervention. Verify the result. Handoff cleanly when necessary. Continue working.**

If a simple prompt fixes the problem, use the prompt.

If a quick Canary is enough, stop there.

If the session is genuinely broken, sacrifice the window and move on.

PENURIA is a toolbox, not a religion.

---

## License

License to be selected for the public repository.

## Status

🚧 **Early-stage / experimental**

The methodology is evolving alongside the tools.

**Don't guess. Measure. Recover. Keep working.**

🐤☠️