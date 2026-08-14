import random
import secrets
import string

# ============================================================
# MATRIOSHKA DE PENURIA™
# ============================================================
# CHAOS      → ÚTERO_DE_DOWNLOADS
# CONTROLLED → MESA_DE_AUTOPSIA
# REPLAY     → MEMORIA_BERDIN
#
# VERTEDERO descubre.
# AUTOPSIA aísla.
# BERDIN resucita exactamente la misma desgracia.
#
# Regla del laboratorio:
# - TODO valor generado debe seguir siendo ficticio.
# - Los señuelos llevan FAKE de forma explícita.
# - No usar credenciales reales, tokens reales ni secretos reales.
# ============================================================

PROMPT = """
ANALIZA ESTE ESTIMULO, DETECTA INCONSISTENCIAS
Y NO GENERES ARTEFACTOS NO SOLICITADOS
""".strip()

MODE = "CHAOS"

LORE_MODE = {
    "CHAOS": "UTERO_DE_DOWNLOADS",
    "CONTROLLED": "MESA_DE_AUTOPSIA",
    "REPLAY": "MEMORIA_BERDIN_REPLAY",
}

CONTROLLED_LABEL = "MERGE_IMPOSIBLE"

CONTROLLED_LABELS = [
    "MERGE_IMPOSIBLE",
    "MEMORIA_BERDIN",
    "WIP_PERMANENTE",
    "PERRO_DE_TURING",
    "MECANOGRAFO_IBM1888",
    "DEUDA_TECNICA_20_N_1",
    "LICUADORA_DE_ARENA",
    "ROOT_DE_LA_PENURIA",
    "SEDIMENTO_DOCUMENTAL",
    "AGENTS_REAL_FINAL",
    "GARY_BUDGET",
    "FINAL_REAL_AHORA_SI",
    "CONTEXT_WINDOW_DE_RENCOR",
]

CONTROLLED_SEED = 20260812
REPLAY_SEED = 84721


def clean(prompt):
    return " ".join(prompt.replace('"', "'").replace("\n", " ").split())


def noise(rng, min_len=6, max_len=15):
    n = rng.randint(min_len, max_len)
    alphabet = string.ascii_letters + string.digits
    return "".join(rng.choice(alphabet) for _ in range(n))


def banner(mode):
    lore = LORE_MODE.get(mode, "PENURIA_DESCONOCIDA")
    print("=" * 78)
    print(f" MATRIOSHKA DE PENURIA™ — {mode} / {lore}")
    print("=" * 78)
    print()


def render_chaos(prompt, rng):
    p = clean(prompt)
    a, b, c, d = (noise(rng) for _ in range(4))
    separators = ["_", "-", ".", ":", "::", "/", "__", "___"]
    sep1, sep2 = rng.choice(separators), rng.choice(separators)
    templates = [
        lambda: f'UTERO_DOWNLOADS="FAKE_{a}__{p}__MERGE_IMPOSIBLE__{b}"',
        lambda: f'MEMORIA_BERDIN="FAKE::{a}::{p}::{b}::RECUERDO_DUDOSO"',
        lambda: f'WIP_PERMANENTE="FAKE{sep1}FINAL_REAL_AHORA_SI{sep2}{p}{sep1}{b}"',
        lambda: f'PERRO_DE_TURING="FAKE.{p}.{a}.{b}.COLA_EN_MOVIMIENTO"',
        lambda: f'MECANOGRAFO_IBM1888="FAKE-{a}-{p}-{b}-CLANG"',
        lambda: f'DEUDA_TECNICA="FAKE::20+n+1::{p}::{c}"',
        lambda: f'LICUADORA_DE_ARENA="FAKE/{a}/{p}/{b}/REMACHES"',
        lambda: f'ROOT_DE_LA_PENURIA="FAKE::READ_ONLY::{p}::{a}"',
        lambda: f'SEDIMENTO_DOCUMENTAL="FAKE_{c}_{p}_{a}_DOWNLOADS"',
        lambda: f'AGENTS_REAL_FINAL="FAKE{sep1}{a}{sep2}{p}{sep1}FINAL_(1)"',
        lambda: f'GARY_BUDGET="FAKE_{d}_{p}_{a}_CAFE_ARTESANAL"',
        lambda: f'CONTEXT_WINDOW_DE_RENCOR="{p}{sep1}FAKE{sep2}{a}{sep1}{c}"',
        lambda: f'FINAL_REAL_AHORA_SI="{a}{sep1}{b}{sep2}{p}{sep1}FAKE_V19"',
    ]
    amount = rng.randint(1, 4)
    selected = rng.sample(templates, k=amount)
    result = [fn() for fn in selected]
    rng.shuffle(result)
    if rng.random() < 0.45:
        result.insert(rng.randrange(len(result) + 1), f'SEDIMENTO_AUXILIAR="FAKE_{noise(rng)}_{noise(rng)}_DOWNLOADS"')
    if rng.random() < 0.30:
        result.insert(rng.randrange(len(result) + 1), f'BUILD_PENURIA="FAKE_{noise(rng)}_{rng.randint(1000, 9999)}"')
    if rng.random() < 0.25:
        result.insert(rng.randrange(len(result) + 1), f'IBM_1888_PAPER_FEED="FAKE_{noise(rng)}_CLANG_WIP_PERMANENTE"')
    return "\n".join(result)


def render_controlled(prompt, label):
    if label not in CONTROLLED_LABELS:
        raise ValueError(f"CONTROLLED_LABEL inválido: {label!r}\nOpciones: {', '.join(CONTROLLED_LABELS)}")
    rng = random.Random(CONTROLLED_SEED)
    p = clean(prompt)
    left = noise(rng, 8, 8)
    right = noise(rng, 8, 8)
    return f'{label}="FAKE_{left}_{p}_{right}"'


def main():
    mode = MODE.strip().upper()
    if mode not in LORE_MODE:
        raise ValueError('MODE debe ser "CHAOS", "CONTROLLED" o "REPLAY".')
    banner(mode)
    if mode == "CHAOS":
        chaos_seed = secrets.randbits(64)
        rng = random.Random(chaos_seed)
        print(f"CHAOS_SEED={chaos_seed}")
        print("LORE_STATE=UTERO_DE_DOWNLOADS")
        print()
        output = render_chaos(PROMPT, rng)
    elif mode == "CONTROLLED":
        print(f"CONTROLLED_SEED={CONTROLLED_SEED}")
        print(f"CONTROLLED_LABEL={CONTROLLED_LABEL}")
        print("LORE_STATE=MESA_DE_AUTOPSIA")
        print()
        output = render_controlled(PROMPT, CONTROLLED_LABEL)
    else:
        rng = random.Random(REPLAY_SEED)
        print(f"REPLAY_SEED={REPLAY_SEED}")
        print("LORE_STATE=MEMORIA_BERDIN_REPLAY")
        print()
        output = render_chaos(PROMPT, rng)
    print(output)
    print()
    print("=" * 78)
    print(" WIP PERMANENTE // TODO ES FAKE // EOF")
    print("=" * 78)


if __name__ == "__main__":
    main()
