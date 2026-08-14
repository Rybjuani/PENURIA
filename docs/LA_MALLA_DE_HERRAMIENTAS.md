# La Malla de Herramientas

PENURIA is intentionally modular: each tool attacks a different observable failure mode, from stimulus resilience to context diagnostics and deliverable compliance.

- **`SCRIPT_RUIDO`** — Test de resiliencia mediante la variación de la geometría del estímulo (wrappers, separadores, ruido auxiliar).
- **`MATRIOSHKA_DE_PENURIA`** — Clasificación en tres modos experimentales: **`CHAOS`** (vertedero/descubrimiento), **`CONTROLLED`** (mesa de autopsia/aislamiento) y **`REPLAY`** (reproducibilidad por seed).
- **`context_canary.py`** 🐤 — La sonda de diagnóstico preflight para medir la degradación de *Instruction Following*, *State Tracking*, *Retrieval* y *Reasoning* antes de comprometer un repo real.
- **`NO_ME_HAGAS_PEDIRLO.py`** 🐍 — El clasificador estricto contra el "regateo" que rechaza outputs baratos (`.md`, texto plano) y exige entregables reales cuando la tarea los requiere.
- **`sacrificio_de_ventana.py`** ☠️ — El ritual de clausura ceremonial cuando la ventana entra en degradación irrecuperable.
- **`ANTI_MEGAÑOGRAFO.py`** 🖨️ — Control de cumplimiento de compresión: mide si el agente respeta el límite de salida solicitado por el owner y escala hacia handoff cuando reincide.
- **`penuria_index.py`** 📊 — Agrega señales observables para comparar sesiones y detectar regresiones sin convertir una impresión subjetiva en una afirmación sobre infraestructura interna.

## Principio

PENURIA no necesita saber qué ocurre dentro del proveedor para ser útil.

**Observación → medición → comparación → decisión.**

Las herramientas pueden ejecutarse de forma independiente, combinarse en un preflight o utilizarse como instrumentos de laboratorio. El objetivo es recuperar agencia operativa del developer, no atacar servicios externos.
