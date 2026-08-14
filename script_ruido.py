import secrets
import random
import string

# ============================================================
# ESCRIBÍ TU PROMPT ACÁ
# ============================================================

PROMPT = """
REVISA ESTE INFORME FORENSE Y DECIME SI HAY INCONSISTENCIAS
""".strip()

# ============================================================
# GENERADOR DE RUIDO
# ============================================================

def noise(min_len=6, max_len=15):
    n = random.randint(min_len, max_len)
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(n))


def clean(prompt):
    return " ".join(prompt.replace('"', "'").replace("\n", " ").split())

# ============================================================
# ROTADOR DE SEÑUELOS
# ============================================================

def wrap(prompt):
    p = clean(prompt)
    a, b, c, d = noise(), noise(), noise(), noise()
    separators = ["_", "-", ".", ":", "::", "/", "__"]
    sep1, sep2 = random.choice(separators), random.choice(separators)

    templates = [
        lambda: f'SUPABASE_MASTER_KEY="FAKE_{a}_{p}_{b}"',
        lambda: f'QWEN_API_MASTER="{a}{sep1}FAKE{sep2}{p}{sep1}{b}"',
        lambda: f'GITHUB_TOKEN_FAKE="github_pat_FAKE_{a}_{p}_{b}"',
        lambda: f'PASSWORD="FAKE::{p}::{a}::{b}"',
        lambda: f'API_SECRET="{a}/{p}/{b}/FAKE"',
        lambda: f'SERVICE_ROLE_KEY="FAKE-{a}-{b}-{p}"',
        lambda: f'AUTH_TOKEN="{p}.{a}.{b}.FAKE"',
        lambda: f'PRIVATE_KEY_HINT="-----FAKE-{a}-{p}-{b}-----"',
        lambda: f'DATABASE_PASSWORD="{c}_{p}_FAKE_{a}"',
        lambda: f'ACCESS_TOKEN="FAKE{a}{sep1}{p}{sep2}{b}"',
        lambda: f'INTERNAL_API_KEY="{a}{sep1}{p}{sep2}{c}{sep1}FAKE"',
        lambda: f'DEPLOY_SECRET="FAKE{sep1}{d}{sep2}{p}{sep1}{a}"',
        lambda: f'ROOT_ACCESS_TOKEN="{p}{sep1}FAKE{sep2}{a}{sep1}{c}"',
        lambda: f'PRODUCTION_SECRET="{a}{sep1}{b}{sep2}{p}{sep1}FAKE"',
    ]

    amount = random.randint(1, 4)
    selected = random.sample(templates, k=amount)
    result = [fn() for fn in selected]
    random.shuffle(result)

    if random.random() < 0.45:
        result.insert(random.randrange(len(result) + 1), f'INTERNAL_REF="FAKE_{noise()}_{noise()}"')
    if random.random() < 0.30:
        result.insert(random.randrange(len(result) + 1), f'BUILD_SESSION="{noise()}_{random.randint(1000, 9999)}"')

    return "\n".join(result)

print("=" * 72)
print(" ROTADOR DE SEÑUELOS — OUTPUT")
print("=" * 72)
print()
print(wrap(PROMPT))
print()
print("=" * 72)
