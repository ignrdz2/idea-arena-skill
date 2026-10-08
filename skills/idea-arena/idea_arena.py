#!/usr/bin/env python3
"""idea_arena.py: the pipeline behind /idea-arena.

/arena's tournament, turned into a funnel for engineering thesis ideas: research
(evidence cards whose URLs really open), generation, a hard filter plus scope and
dedup checks, a tournament with persona attacks and a blind judge, and a shortlist
for humans to validate with the market.

    python idea_arena.py plan [--pilot] [--seed S] [--json]   # dry run: phases, calls, caps. Writes nothing
    python idea_arena.py init [--pilot] [--seed S] [--dry-run]
    python idea_arena.py next                                 # what to do now, and the exact command
    python idea_arena.py prompts <phase>                      # write the briefs, list the jobs left, in waves
    python idea_arena.py check <phase>                        # which outputs are still missing
    python idea_arena.py step                                 # run the pending Python step
    python idea_arena.py palabras <idea.json>                 # schema, cost and page words, as the filter counts them
    python idea_arena.py status [--json]
    python idea_arena.py record <match_id> <idea_id> [--reason "..."]
    python idea_arena.py deepen <idea_id>                     # queue the deep dive for one idea
    python idea_arena.py calibrate [--dry-run]                # a calibration run over calibration/
    python idea_arena.py doctor                               # placeholders and consistency checks
    python idea_arena.py audit                                # anything changed outside runs/ since init

Agent phases: research, generate, scope, dedup, attack, defend, judge, questions,
deepen, calibrate. Every file the pipeline writes goes under runs/<YYYYMMDD-HHMM>/,
and runs/LATEST names the current run. Every command takes --run.

Python 3.8+, standard library only.
"""
import sys

sys.dont_write_bytecode = True   # never leave __pycache__ next to the skills

import argparse  # noqa: E402
import collections  # noqa: E402
import copy  # noqa: E402
import datetime  # noqa: E402
import itertools  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import os  # noqa: E402
import random  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import time  # noqa: E402

import ia_evidence as E  # noqa: E402
import ia_schema as S  # noqa: E402
import ia_tournament as T  # noqa: E402

B = T.B
HERE = os.path.dirname(os.path.abspath(__file__))
SELF = os.path.abspath(__file__)
ROOT = os.path.abspath(os.environ.get("IDEA_ARENA_ROOT") or os.path.dirname(os.path.dirname(HERE)))
RUNS = "runs"
LATEST = "runs/LATEST"
STATE_FILE = "state.json"
NO_OUTPUT = "NO OUTPUT"
PY = "python" if os.name == "nt" else "python3"

CONFIG_PATH = os.path.join(HERE, "config.json")
CONSTRAINTS_PATH = os.path.join(HERE, "constraints.md")
RUBRIC_PATH = os.path.join(HERE, "rubric.md")
STRATEGIES_PATH = os.path.join(HERE, "strategies.json")
PERSONAS_PATH = os.path.join(HERE, "personas.json")
BRIEFS_DIR = os.path.join(HERE, "briefs")
TEMPLATES_DIR = os.path.join(HERE, "templates")
CALIBRATION_DIR = os.path.join(HERE, "calibration")

AGENT_PHASES = ("research", "generate", "scope", "dedup", "attack", "defend", "judge", "questions",
                "deepen", "calibrate")
TOURNAMENT_PHASES = ("attack", "defend", "judge")
BRIEF_OF = {"research": "01_investigacion", "generate": "02_generacion", "scope": "03_alcance",
            "dedup": "03_dedup", "attack": "04_ataque", "defend": "04_defensa", "judge": "04_juez",
            "questions": "05_preguntas", "calibrate": "07_calibracion"}
# Thousands of tokens per call, low and high. A rough guess until the pilot measures it.
TOKENS_K = {"research": (60, 200), "generate": (30, 60), "scope": (15, 30), "dedup": (30, 60),
            "attack": (15, 40), "defend": (15, 35), "judge": (25, 50), "questions": (15, 25),
            "deepen": (40, 120), "calibrate": (20, 40)}
FICHA_FILES = ("evidence/fichas.json", "evidence/fichas_torneo.json", "evidence/fichas_profundizar.json")
PLACEHOLDER_RE = re.compile(r"<<(COMPLETAR|REVISAR)(:[^<>]*)?>>")   # may span lines; `quoted` ones are examples

_RUN_SUFFIX = ""


class IdeaArenaError(Exception):
    pass


# ---------------------------------------------------------------- paths and files

def _slash(p):
    return p.replace("\\", "/")


def j(*parts):
    return _slash(os.path.join(*parts))


def rel(path):
    return _slash(os.path.relpath(os.path.abspath(path)))


def ab(path):
    return os.path.abspath(path)


def inside_runs(path):
    runs = os.path.realpath(os.path.abspath(RUNS))
    real = os.path.realpath(os.path.abspath(path))
    return real == runs or real.startswith(runs + os.sep)


def guard(path):
    if not inside_runs(path):
        raise IdeaArenaError("idea-arena solo escribe dentro de runs/. Bloqueado: %s" % path)


def write_text(path, text):
    guard(path)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(E.sanitize_text(text))
    os.replace(tmp, path)


def write_json(path, obj):
    write_text(path, json.dumps(E.sanitize_obj(obj), ensure_ascii=False, indent=1) + "\n")


def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def read_json(path, default=None):
    if not os.path.isfile(path):
        return default
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_json_file(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def has_output(path):
    return os.path.isfile(path) and os.path.getsize(path) > 0


def is_no_output(path):
    return has_output(path) and read_text(path).strip() == NO_OUTPUT


def parse_json_output(path):
    """The JSON object an agent wrote, or None. Tolerates a code fence around it."""
    v = B.extract_json(read_text(path))
    return v if isinstance(v, dict) else None


def reject_output(path, fallback=True, max_attempts=2):
    """Set an unusable output aside as <path>.invalido<k>, so its job shows up as missing.
    Before max_attempts the job is re-run ("rerun"). At max_attempts the output becomes
    NO OUTPUT when the pipeline has a fallback ("fallback"), or the job needs a human ("manual")."""
    guard(path)
    k = 1
    while os.path.exists("%s.invalido%d" % (path, k)):
        k += 1
    os.replace(path, "%s.invalido%d" % (path, k))
    if k < max_attempts:
        return "rerun"
    if fallback:
        write_text(path, NO_OUTPUT + "\n")
        return "fallback"
    return "manual"


def now_iso():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def fmt(x):
    return "?" if x is None else ("%g" % x)


def _script():
    try:
        r = os.path.relpath(SELF, ROOT)
    except ValueError:
        r = ".."
    p = _slash(SELF if r.startswith("..") else r)
    return '"%s"' % p if " " in p else p


def _cmd(*parts):
    return "%s %s %s%s" % (PY, _script(), " ".join(parts), _RUN_SUFFIX)


def _word_check(d, path):
    """The command a generator or defender runs on its own output: absolute paths, any working dir."""
    q = lambda p: '"%s"' % _slash(p) if " " in p else _slash(p)  # noqa: E731
    return "%s %s palabras --run %s %s" % (PY, q(SELF), q(ab(d)), q(ab(path)))


# ---------------------------------------------------------------- config and inputs

def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def effective_config(src, pilot):
    cfg = deep_merge(src, (src.get("pilot") or {}).get("overrides") or {}) if pilot else copy.deepcopy(src)
    cfg.pop("pilot", None)
    cfg["mode"] = "pilot" if pilot else "full"
    return cfg


def pick_sectors(src, pilot, seed):
    sectors = src["sectors"]
    if not pilot:
        return list(sectors), "todos los de config.json"
    p = src.get("pilot") or {}
    chosen = p.get("sectors") or []
    if chosen:
        by = {s["id"]: s for s in sectors}
        unknown = [x for x in chosen if x not in by]
        if unknown:
            raise IdeaArenaError("pilot.sectors tiene sectores que no están en config.json: %s" % ", ".join(unknown))
        return [by[x] for x in chosen], "elegidos en pilot.sectors"
    n = min(int(p.get("sectors_count", 3)), len(sectors))
    picked = set(s["id"] for s in random.Random("idea-arena-sectors:%s" % seed).sample(sectors, n))
    return [s for s in sectors if s["id"] in picked], "sorteados con la semilla %s" % seed


def assign_generators(strategies, sectors, gcfg, seed):
    """Strategy i mod S. The sectors split into one focus group per generator (or one per sector,
    if there are fewer sectors than generators), so each generator works its own slice of the
    evidence. When every generator saw every sector, they all chased the same few problems."""
    n, per = int(gcfg["agents"]), int(gcfg["ideas_per_agent"])
    k = len(strategies)
    groups_n = max(1, min(len(sectors), n))
    order = [s["id"] for s in sectors]
    ids = list(order)
    random.Random("idea-arena-gen:%s" % seed).shuffle(ids)
    groups = [sorted(ids[g::groups_n], key=order.index) for g in range(groups_n)]
    return [{"id": "g%02d" % (i + 1), "strategy": strategies[i % k]["id"],
             "focus": groups[i % groups_n], "ideas": per} for i in range(n)]


def team_hours(cfg):
    t = cfg["team"]
    return t["size"] * t["hours_per_week"][0] * t["weeks"], t["size"] * t["hours_per_week"][1] * t["weeks"]


def fill_constraints(text, cfg):
    lo, hi = team_hours(cfg)
    for k, v in (("infra_budget_usd", cfg["infra_budget_usd"]), ("infra_budget_target_usd", cfg["infra_budget_target_usd"]),
                 ("horas_min", lo), ("horas_max", hi)):
        text = text.replace("{{%s}}" % k, "%g" % v)
    return text


_R_BULLET = re.compile(r"^\s*-\s*\*\*(R\d+)\*\*")


def hard_restrictions(text):
    """(confirmed ids, ids still marked [A CONFIRMAR]) from the hard-restrictions section."""
    confirmed, pending = [], []
    section = re.split(r"^## 1\. Restricciones duras\s*$", text, maxsplit=1, flags=re.M)
    if len(section) < 2:
        return confirmed, pending
    body = re.split(r"^## ", section[1], maxsplit=1, flags=re.M)[0]
    current, block = None, []

    def close():
        if current:
            (pending if "[A CONFIRMAR]" in " ".join(block) else confirmed).append(current)

    for line in body.splitlines():
        m = _R_BULLET.match(line)
        if m:
            close()
            current, block = m.group(1), [line]
        elif current and line.strip() and not line.lstrip().startswith("-"):
            block.append(line)
        else:
            close()
            current, block = None, []
    close()
    return confirmed, pending


def run_hard_ids(d):
    return set(hard_restrictions(read_text(j(d, "inputs", "constraints.md")))[0])


def load_personas(path=PERSONAS_PATH):
    data = load_json_file(path)
    return {p["id"]: p for p in data["personas"]}


def load_strategies(path=STRATEGIES_PATH):
    data = load_json_file(path)
    items = data.get("strategies") or []
    ids = [s["id"] for s in items]
    if not items or len(set(ids)) != len(ids):
        raise IdeaArenaError("strategies.json necesita estrategias con ids únicos")
    return items


# ---------------------------------------------------------------- the plan

def scope_batch_size(n_ideas, cfg):
    return max(int(cfg["filter"]["scope_batch"]), int(math.ceil(n_ideas / float(max(1, cfg["limits"]["scope"])))))


def build_plan(cfg, n_sectors):
    g, f, lim, w, t = cfg["generation"], cfg["filter"], cfg["limits"], cfg["wave"], cfg["tournament"]
    ideas = g["agents"] * g["ideas_per_agent"]
    scope = int(math.ceil(ideas / float(scope_batch_size(ideas, cfg)))) if ideas else 0
    dedup = 1 if f["dedup_agent"] and ideas > 1 else 0
    n = min(cfg["selection"]["max_candidates"], ideas)
    k, both = t["personas_per_match"], t["judge_both_orders"]
    trows = T.tournament_plan(n, k, both, w)
    matches = sum(r["matches"] for r in trows)
    q = min(cfg["shortlist"]["size"], n)

    def wv(c):
        return int(math.ceil(c / float(w))) if c else 0

    rows = [
        {"phase": "research", "label": "F1  investigación", "kind": "agentes", "calls": n_sectors, "waves": wv(n_sectors), "limit": lim["research"]},
        {"phase": "verify", "label": "F1b verificación de URLs", "kind": "python", "calls": 0},
        {"phase": "generate", "label": "F2  generación (%d ideas)" % ideas, "kind": "agentes", "calls": g["agents"], "waves": wv(g["agents"]), "limit": lim["generate"]},
        {"phase": "hard", "label": "F3a filtro duro", "kind": "python", "calls": 0},
        {"phase": "scope", "label": "F3b alcance", "kind": "agentes", "calls": scope, "waves": wv(scope), "limit": lim["scope"], "max": True},
        {"phase": "dedup", "label": "F3c deduplicación", "kind": "agentes", "calls": dedup, "waves": wv(dedup), "limit": lim["dedup"], "max": True},
        {"phase": "select", "label": "F3d selección (hasta %d)" % n, "kind": "python", "calls": 0},
        {"phase": "tournament", "label": "F4  torneo (%d ideas, %d rondas)" % (n, len(trows)), "kind": "agentes",
         "calls": sum(r["calls"] for r in trows), "waves": sum(r["waves"] for r in trows), "limit": lim["tournament"], "max": True},
        {"phase": "questions", "label": "F5  preguntas de validación", "kind": "agentes", "calls": q, "waves": wv(q), "limit": lim["questions"], "max": True},
        {"phase": "shortlist", "label": "F5  shortlist.md", "kind": "python", "calls": 0},
    ]
    counts = {"research": n_sectors, "generate": g["agents"], "scope": scope, "dedup": dedup,
              "attack": 2 * k * matches, "defend": 2 * matches, "judge": (2 if both else 1) * matches, "questions": q}
    lo = sum(TOKENS_K[p][0] * c for p, c in counts.items())
    hi = sum(TOKENS_K[p][1] * c for p, c in counts.items())
    return {"rows": rows, "tournament": trows, "ideas": ideas, "candidates": n,
            "calls": sum(r["calls"] for r in rows), "waves": sum(r.get("waves", 0) for r in rows),
            "tokens_k": [lo, hi]}


def over_limits(plan):
    return [r for r in plan["rows"] if r["kind"] == "agentes" and r["calls"] > r["limit"]]


def _millions(k):
    return ("%.1f" % (k / 1000.0)).replace(".", ",")


def print_plan(plan, cfg, sectors, how, seed, header):
    print(header)
    print("semilla %s (repetila con --seed %s para el mismo sorteo y los mismos cruces)" % (seed, seed))
    print("sectores (%d, %s): %s" % (len(sectors), how, ", ".join(s["nombre"] for s in sectors)))
    print("tope de infraestructura: USD %g por año (objetivo USD %g)" % (cfg["infra_budget_usd"], cfg["infra_budget_target_usd"]))
    print("")
    print("  %-38s %-8s %9s %8s %6s  %s" % ("fase", "tipo", "llamadas", "oleadas", "tope", "estado"))
    for r in plan["rows"]:
        if r["kind"] == "python":
            print("  %-38s %-8s %9s %8s %6s  %s" % (r["label"], "python", "0", "-", "-", "-"))
            continue
        calls = ("hasta %d" % r["calls"]) if r.get("max") else str(r["calls"])
        print("  %-38s %-8s %9s %8d %6d  %s" % (r["label"], "agentes", calls, r["waves"], r["limit"],
                                               "ok" if r["calls"] <= r["limit"] else "EXCEDE EL TOPE"))
    print("  %-38s %-8s %9s %8d" % ("total", "", "hasta %d" % plan["calls"], plan["waves"]))
    print("")
    t = cfg["tournament"]
    print("  torneo por ronda (%d llamadas por cruce: %d ataque(s), 2 defensas, %d juez(es)):"
          % (T.calls_per_match(t["personas_per_match"], t["judge_both_orders"]), 2 * t["personas_per_match"],
             2 if t["judge_both_orders"] else 1))
    print("  %5s  %5s  %6s  %3s  %-24s %8s %8s" % ("ronda", "vivas", "cruces", "bye", "persona", "llamadas", "oleadas"))
    fake = {"persona_order": t["persona_order"], "personas_per_match": t["personas_per_match"]}
    for r in plan["tournament"]:
        print("  %5d  %5d  %6d  %3s  %-24s %8d %8d" % (r["round"], r["alive"], r["matches"], "sí" if r["bye"] else "-",
                                                     ", ".join(T.round_personas(fake, r["round"])), r["calls"], r["waves"]))
    print("")
    lo, hi = plan["tokens_k"]
    print("  tokens, a ojo: entre %s y %s millones (el piloto lo mide de verdad)" % (_millions(lo), _millions(hi)))
    print("  'hasta': máximos; dependen de cuántas ideas pasen los filtros.")
    print("  aparte: calibrate (2 llamadas por par de ideas de calibración) y deepen (%d por idea)." % len(cfg["deepen"]["aspects"]))
    over = over_limits(plan)
    if over:
        print("")
        print("  EXCEDE: %s. Bajá los tamaños o subí limits en config.json." % ", ".join(r["phase"] for r in over))


# ---------------------------------------------------------------- run state

def run_dir_from(args):
    d = getattr(args, "run", None)
    if not d:
        if not os.path.isfile(LATEST):
            raise IdeaArenaError("no hay ningún run. Empezá con init (o pasá --run)")
        d = read_text(LATEST).strip()
    d = rel(d)
    if not os.path.isfile(j(d, STATE_FILE)):
        raise IdeaArenaError("no hay %s en %s" % (STATE_FILE, d))
    return d


def load_run(args):
    d = run_dir_from(args)
    return d, read_json(j(d, STATE_FILE)), read_json(j(d, "inputs", "config.json"))


def save_state(d, st):
    write_json(j(d, STATE_FILE), st)


def new_run_dir():
    base = time.strftime("%Y%m%d-%H%M")
    d, k = j(RUNS, base), 2
    while os.path.exists(d):
        d, k = j(RUNS, "%s-%d" % (base, k)), k + 1
    guard(d)
    os.makedirs(d)
    return d


def copy_inputs(d, cfg, schema_names):
    write_text(j(d, "inputs", "constraints.md"), fill_constraints(read_text(CONSTRAINTS_PATH), cfg))
    write_text(j(d, "inputs", "rubric.md"), read_text(RUBRIC_PATH))
    write_text(j(d, "inputs", "strategies.json"), read_text(STRATEGIES_PATH))
    write_text(j(d, "inputs", "personas.json"), read_text(PERSONAS_PATH))
    write_json(j(d, "inputs", "config.json"), cfg)
    for name in schema_names:
        write_text(j(d, "inputs", "schemas", "%s.schema.json" % name),
                   read_text(os.path.join(S.SCHEMA_DIR, "%s.schema.json" % name)))


SCHEMAS = ("ficha", "idea", "alcance", "dedup", "ataque", "defensa", "veredicto", "preguntas")


def git_status_lines():
    try:
        out = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=ROOT,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return [line for line in out.stdout.splitlines() if line.strip()]


def _status_path(line):
    p = line[3:]
    if " -> " in p:
        p = p.split(" -> ")[-1]
    return p.strip().strip('"')


def load_fichas(d):
    out = {}
    for name in FICHA_FILES:
        for f in (read_json(j(d, name), {}) or {}).get("fichas", []):
            out[f["id"]] = f
    return out


def write_all_fichas(d):
    fichas = load_fichas(d)
    write_json(j(d, "evidence", "fichas_todas.json"), {"fichas": [fichas[k] for k in sorted(fichas)]})


def add_fichas(d, name, new):
    path = j(d, name)
    data = read_json(path, {"fichas": []})
    data["fichas"].extend(new)
    write_json(path, data)


def add_discarded(d, items):
    if not items:
        return
    path = j(d, "evidence", "descartadas_posteriores.json")
    data = read_json(path, {"descartadas": []})
    data["descartadas"].extend(items)
    write_json(path, data)


def check_urls_cached(d, cfg, urls):
    """{url: {"estado", "http", "checked_at", "texto"}}. Each URL is fetched once per run;
    "texto" is only there for URLs fetched in this call."""
    path = j(d, "evidence", "urls.json")
    cache = read_json(path, {})
    todo = sorted(set(u for u in urls if E.is_url(u) and u not in cache))
    texts = {}
    if todo:
        res = E.check_urls(todo, timeout=cfg["evidence"]["timeout_s"], workers=cfg["evidence"]["workers"])
        stamp = now_iso()
        for u, r in res.items():
            cache[u] = {"estado": r["estado"], "http": r["http"], "checked_at": stamp}
            texts[u] = r.get("texto")
        write_json(path, cache)
    return {u: dict(cache[u], texto=texts.get(u)) for u in set(urls) if u in cache}


def accept_new_fichas(d, cfg, raw, prefix, target, context):
    """Validate and URL-check cards written during the tournament or a deep dive.
    Returns (accepted ids, discarded)."""
    raw = [f for f in (raw or []) if isinstance(f, dict)] if isinstance(raw, list) else []
    if not raw:
        return [], []
    res = check_urls_cached(d, cfg, [f.get("source_url") for f in raw])
    acc, dis = S.process_fichas(raw, prefix, res, cfg, seen_ids=load_fichas(d).keys())
    if acc:
        add_fichas(d, target, acc)
    add_discarded(d, [dict(x, contexto=context) for x in dis])
    return [f["id"] for f in acc], dis


def ficha_prefix(kind, mid=None, iid=None, persona=None, aspect=None):
    if kind == "attack":
        return "F-ataque-%s-%s-%s-" % (mid, iid, persona)
    if kind == "defend":
        return "F-defensa-%s-%s-" % (mid, iid)
    return "F-prof-%s-%s-" % (iid, aspect)


def tournament_path(d):
    return j(d, "tournament", "bracket.json")


def load_tournament(d):
    return read_json(tournament_path(d))


def save_tournament(d, ts):
    write_json(tournament_path(d), ts)


def latest_idea(d, iid, ts=None):
    """(idea json, page path) of an idea's latest version."""
    ts = ts if ts is not None else load_tournament(d)
    if ts and iid in ts["agents"]:
        ag = ts["agents"][iid]
        return read_json(ag["idea_json"]), ag["solution"]
    return read_json(j(d, "ideas", iid + ".json")), j(d, "ideas", iid + ".md")


def primary_sector(idea, fichas, fallback):
    counts, first = collections.Counter(), {}
    for i, cid in enumerate(S.cited_ids(idea)):
        f = fichas.get(cid)
        if f and f["sector"] != "transversal":
            counts[f["sector"]] += 1
            first.setdefault(f["sector"], i)
    if not counts:
        return fallback
    return min(counts, key=lambda s: (-counts[s], first[s]))


def evidence_strength(idea, fichas):
    valid = [c for c in S.cited_ids(idea) if c in fichas]
    ok = [c for c in valid if S.ficha_estado(fichas[c]) == E.OK]
    return len(ok), len(valid)


# ---------------------------------------------------------------- jobs

def phase_jobs(d, st, phase):
    jobs = []
    if phase == "research":
        for s in st["sectors"]:
            jobs.append({"id": "investigacion.%s" % s["id"], "kind": "research", "sector": s,
                         "outputs": [j(d, "evidence", "raw", s["id"] + ".json")]})
    elif phase == "generate":
        for g in st["generators"]:
            jobs.append({"id": "generacion.%s" % g["id"], "kind": "generate", "gen": g,
                         "outputs": [j(d, "ideas", "raw", g["id"] + ".json")]})
    elif phase == "scope":
        nb = len(st.get("scope_batches") or [])
        for i, batch in enumerate(st.get("scope_batches") or [], start=1):
            jobs.append({"id": "alcance.lote-%02d" % i, "kind": "scope", "batch": batch,
                         "label": "lote %d de %d" % (i, nb), "outputs": [j(d, "filter", "alcance", "lote-%02d.json" % i)]})
    elif phase == "dedup":
        if st.get("dedup_needed"):
            jobs.append({"id": "dedup", "kind": "dedup", "outputs": [j(d, "filter", "dedup.json")]})
    elif phase in TOURNAMENT_PHASES:
        ts = load_tournament(d)
        if ts:
            jobs = T.tournament_jobs(ts, phase)
    elif phase == "questions":
        for iid in st.get("shortlist") or []:
            jobs.append({"id": "preguntas.%s" % iid, "kind": "questions", "idea": iid,
                         "outputs": [j(d, "shortlist", "preguntas", iid + ".json")]})
    elif phase == "deepen":
        for iid, req in sorted((st.get("deepen") or {}).items()):
            if req.get("collected"):
                continue
            for a in req["aspects"]:
                jobs.append({"id": "profundizar.%s.%s" % (iid, a), "kind": "deepen", "idea": iid, "aspect": a,
                             "outputs": [j(d, "deepen", iid, a + ".md"), j(d, "deepen", iid, a + ".fichas.json")]})
    elif phase == "calibrate":
        for c in (st.get("calibration") or {}).get("jobs", []):
            jobs.append(dict(c, kind="calibrate"))
    else:
        raise IdeaArenaError("fase desconocida '%s' (una de: %s)" % (phase, ", ".join(AGENT_PHASES)))
    for job in jobs:
        job["phase"] = phase
        job["prompt"] = j(d, "prompts", phase, job["id"] + ".md")
    return jobs


def missing_jobs(jobs):
    return [x for x in jobs if not all(has_output(p) for p in x["outputs"])]


def _stuck(left):
    for job in left:
        for p in job["outputs"]:
            if os.path.exists(p + ".invalido3"):
                return job
    return None


def next_action(d, st):
    """("phase", name, left, jobs), ("step", name, what), ("stuck", job) or ("done",)."""
    steps = st["steps"]

    def phase(name):
        jobs = phase_jobs(d, st, name)
        left = missing_jobs(jobs)
        if not left:
            return None
        if name in ("judge", "calibrate"):
            job = _stuck(left)
            if job:
                return ("stuck", job)
        return ("phase", name, left, jobs)

    if st.get("deepen"):
        r = phase("deepen")
        if r:
            return r
        if any(not v.get("collected") for v in st["deepen"].values()):
            return ("step", "deepen-collect", "verificar las fichas nuevas de la profundización")
    if st["mode"] == "calibration":
        r = phase("calibrate")
        if r:
            return r
        if "calibration-report" not in steps:
            return ("step", "calibration-report", "comparar el juez con tu ranking")
        return ("done",)
    r = phase("research")
    if r:
        return r
    if "verify" not in steps:
        return ("step", "verify", "verificar las fichas y abrir cada URL por HTTP")
    r = phase("generate")
    if r:
        return r
    if "ingest" not in steps:
        return ("step", "ingest", "validar las ideas, asignar IDs, verificar precios y aplicar el filtro duro")
    r = phase("scope")
    if r:
        return r
    if "scope-collect" not in steps:
        return ("step", "scope-collect", "aplicar el chequeo de alcance y la similitud léxica")
    r = phase("dedup")
    if r:
        return r
    if "select" not in steps:
        return ("step", "select", "agrupar duplicados, elegir los candidatos y armar el bracket")
    ts = load_tournament(d)
    if ts and not ts["champion"]:
        rd = B.current_round(ts)
        open_ms = [m for m in rd["matches"] if not m["winner"]]
        r = phase("attack")
        if r:
            return r
        if any(not m.get("attacks_checked") for m in open_ms):
            return ("step", "check-attacks", "verificar la evidencia de los ataques")
        r = phase("defend")
        if r:
            return r
        if any(not m.get("revised") for m in open_ms):
            return ("step", "revise", "validar y renderizar las ideas revisadas")
        r = phase("judge")
        if r:
            return r
        if open_ms:
            return ("step", "collect", "aplicar la rúbrica a los veredictos")
        return ("step", "advance", "cerrar la ronda %d" % rd["n"])
    if "rank" not in steps:
        return ("step", "rank", "ordenar las ideas y elegir el top")
    r = phase("questions")
    if r:
        return r
    if "shortlist" not in steps:
        return ("step", "shortlist", "escribir shortlist.md y los guiones")
    return ("done",)


# ---------------------------------------------------------------- briefs

def _strip_comment(text):
    """Templates open with an HTML comment for humans; the agents never see it."""
    return re.sub(r"^\s*<!--.*?-->\s*", "", text, count=1, flags=re.S).rstrip("\n")


def brief_template(name):
    return _strip_comment(read_text(os.path.join(BRIEFS_DIR, name + ".md")))


def page_template(name):
    return _strip_comment(read_text(os.path.join(TEMPLATES_DIR, name + ".md")))


def _search_rule(cfg, prefix, schema):
    if not cfg["tournament"]["attackers_can_search"]:
        return "No busques en la web: usá solo las fichas disponibles, y nuevas_fichas va vacía."
    return ("Podés buscar en la web (WebSearch y WebFetch) lo que la idea o los ataques ignoran. Cada fuente nueva va "
            "como ficha en nuevas_fichas, con el esquema %s, sector \"transversal\" o el del tema, e IDs que empiecen "
            "con %s (por ejemplo %s001); después la citás por ese ID. Python la verifica igual que las demás: si la "
            "URL no existe, la ficha se descarta y lo que se apoyaba en ella pasa a ser opinión." % (schema, prefix, prefix))


def render_brief(d, st, cfg, job, ts=None, personas=None, strategies=None):
    kind = job["kind"]
    inp = lambda *p: ab(j(d, "inputs", *p))  # noqa: E731
    schema = lambda name: inp("schemas", "%s.schema.json" % name)  # noqa: E731
    v = {"constraints": inp("constraints.md"), "rubric": inp("rubric.md"), "run_dir": ab(d),
         "scratch_dir": ab(j(d, "scratch", job["id"])), "fichas": ab(j(d, "evidence", "fichas_todas.json")),
         "out": ab(job["outputs"][0]), "budget": "%g" % cfg["infra_budget_usd"],
         "budget_target": "%g" % cfg["infra_budget_target_usd"], "max_words": cfg["filter"]["idea_max_words"],
         "schema_ficha": schema("ficha"), "schema_idea": schema("idea")}
    v["reglas_comunes"] = B.fill(brief_template("_comunes"), v)
    if kind == "research":
        s = job["sector"]
        v.update(sector_id=s["id"], sector_nombre=s["nombre"], fichas_min=cfg["research"]["fichas_min"],
                 fichas_max=cfg["research"]["fichas_max"], max_age=cfg["research"]["max_source_age_years"])
    elif kind == "generate":
        g = job["gen"]
        strat = {s["id"]: s for s in strategies}[g["strategy"]]
        names = {s["id"]: s["nombre"] for s in st["sectors"]}
        v.update(generator=g["id"], ideas_n=g["ideas"], strategy_name=strat["name"], strategy_how=strat["how"],
                 focus=", ".join("%s (%s)" % (names.get(x, x), x) for x in g["focus"]),
                 min_evidence=cfg["filter"]["min_evidence_per_idea"], min_local=cfg["filter"]["min_local_evidence"],
                 word_check=_word_check(d, job["outputs"][0]))
    elif kind == "scope":
        lo, hi = team_hours(cfg)
        v.update(batch=job["label"], hours_low=lo, hours_high=hi, schema=schema("alcance"), ids=", ".join(job["batch"]),
                 ideas_list="\n".join("- %s: %s" % (iid, ab(j(d, "ideas", iid + ".md"))) for iid in job["batch"]))
    elif kind == "dedup":
        v.update(n=len(st["candidates"]), candidates=ab(j(d, "filter", "candidatos.md")),
                 lexical=ab(j(d, "filter", "dedup_lexico.json")), schema=schema("dedup"), ids=", ".join(st["candidates"]))
    elif kind == "attack":
        p = personas[job["persona"]]
        prefix = ficha_prefix("attack", job["match"], job["idea"], job["persona"])
        v.update(round=job["round"], match=job["match"], persona_id=p["id"], persona_name=p["name"],
                 persona_lens=p["lens"], persona_asks="\n".join("- %s" % q for q in p["asks"]),
                 target=ab(ts["agents"][job["idea"]]["solution"]), target_id=job["idea"],
                 search_rule=_search_rule(cfg, prefix, schema("ficha")), schema=schema("ataque"))
    elif kind == "defend":
        iid, n, mid = job["idea"], job["round"], job["match"]
        v.update(round=n, match=mid, idea_id=iid, own_page=ab(ts["agents"][iid]["solution"]),
                 own_json=ab(ts["agents"][iid]["idea_json"]), attacks=ab(T.attacks_md(ts, n, mid, iid)),
                 schema_defense=schema("defensa"), defense_out=ab(job["outputs"][0]), idea_out=ab(job["outputs"][1]),
                 search_rule=_search_rule(cfg, ficha_prefix("defend", mid, iid), schema("ficha")),
                 word_check=_word_check(d, job["outputs"][1]))
    elif kind == "judge":
        n, mid, x, y = job["round"], job["match"], job["x"], job["y"]
        m = next(mm for mm in B.current_round(ts)["matches"] if mm["id"] == mid)
        v.update(round=n, match=mid, persona_name=" y ".join(personas[p]["name"] for p in m["personas"]),
                 x_page=ab(T.solution_md(ts, n, mid, x)), x_attacks=ab(T.attacks_md(ts, n, mid, x)),
                 x_defense=ab(T.defense_md(ts, n, mid, x)), y_page=ab(T.solution_md(ts, n, mid, y)),
                 y_attacks=ab(T.attacks_md(ts, n, mid, y)), y_defense=ab(T.defense_md(ts, n, mid, y)),
                 schema=schema("veredicto"))
    elif kind == "questions":
        iid = job["idea"]
        v.update(idea_id=iid, n_questions=cfg["shortlist"]["questions_per_idea"], page=ab(latest_idea(d, iid, ts)[1]),
                 trail=ab(j(d, "shortlist", "rastro", iid + ".md")), schema=schema("preguntas"))
    elif kind == "deepen":
        iid = job["idea"]
        v.update(idea_id=iid, page=ab(latest_idea(d, iid, ts)[1]), out_md=ab(job["outputs"][0]),
                 out_fichas=ab(job["outputs"][1]), ficha_prefix=ficha_prefix("deepen", iid=iid, aspect=job["aspect"]))
    elif kind == "calibrate":
        v.update(pair=job["pair"], x_page=ab(j(d, "calibration", "ideas", job["x"] + ".md")),
                 y_page=ab(j(d, "calibration", "ideas", job["y"] + ".md")), schema=schema("veredicto"))
    name = "06_profundizar_%s" % job["aspect"] if kind == "deepen" else BRIEF_OF[kind]
    return B.fill(brief_template(name), v)


# ---------------------------------------------------------------- python steps

def step_verify(d, st, cfg):
    lines, readable, pending = [], [], False
    for job in phase_jobs(d, st, "research"):
        path, sid = job["outputs"][0], job["sector"]["id"]
        if is_no_output(path):
            readable.append((sid, []))
            continue
        data = parse_json_output(path)
        if data is None or not isinstance(data.get("fichas"), list):
            res = reject_output(path)
            pending = pending or res == "rerun"
            lines.append("  %s: salida ilegible, %s" % (sid, "se vuelve a correr" if res == "rerun" else "queda sin fichas"))
            if res != "rerun":
                readable.append((sid, []))
            continue
        readable.append((sid, data["fichas"]))
    if pending:
        return lines + ["hay investigaciones para volver a correr: %s" % _cmd("next")]
    res = check_urls_cached(d, cfg, [f.get("source_url") for _, fs in readable for f in fs if isinstance(f, dict)])
    accepted, discarded, seen, per = [], [], set(), {}
    for sid, fs in readable:
        acc, dis = S.process_fichas(fs, "F-%s-" % sid, res, cfg, seen_ids=seen)
        seen.update(f["id"] for f in acc)
        accepted += acc
        discarded += [dict(x, sector=sid) for x in dis]
        per[sid] = {"recibidas": len(fs), "aceptadas": len(acc), "bloqueadas": sum(1 for f in acc if S.ficha_estado(f) == E.BLOCKED),
                    "descartadas": len(dis)}
    write_json(j(d, "evidence", "fichas.json"), {"fichas": accepted})
    write_json(j(d, "evidence", "descartadas.json"), {"descartadas": discarded})
    write_all_fichas(d)
    reasons = collections.Counter(x["motivo"] for x in discarded)
    blocked = sum(1 for f in accepted if S.ficha_estado(f) == E.BLOCKED)
    st["steps"]["verify"] = {"aceptadas": len(accepted), "ok": len(accepted) - blocked, "bloqueadas": blocked,
                             "descartadas": len(discarded), "motivos": dict(reasons), "por_sector": per}
    lines.append("fichas: %d aceptadas (%d ok, %d bloqueadas), %d descartadas%s"
                 % (len(accepted), len(accepted) - blocked, blocked, len(discarded),
                    " (%s)" % ", ".join("%s %d" % kv for kv in sorted(reasons.items())) if reasons else ""))
    for sid in sorted(per):
        lines.append("  %-22s %d de %d" % (sid, per[sid]["aceptadas"], per[sid]["recibidas"]))
    if not accepted:
        lines.append("ATENCIÓN: ninguna ficha válida. Mirá evidence/descartadas.json antes de seguir.")
    return lines


def make_batches(ids, cfg):
    size = scope_batch_size(len(ids), cfg)
    return [ids[i:i + size] for i in range(0, len(ids), size)]


def step_ingest(d, st, cfg):
    lines, readable, pending = [], [], False
    gens = {g["id"]: g for g in st["generators"]}
    for job in phase_jobs(d, st, "generate"):
        path, gid = job["outputs"][0], job["gen"]["id"]
        if is_no_output(path):
            continue
        data = parse_json_output(path)
        if data is None or not isinstance(data.get("ideas"), list):
            res = reject_output(path)
            pending = pending or res == "rerun"
            lines.append("  %s: salida ilegible, %s" % (gid, "se vuelve a correr" if res == "rerun" else "queda sin ideas"))
            continue
        readable.append((gid, data["ideas"]))
    if pending:
        return lines + ["hay generadores para volver a correr: %s" % _cmd("next")]
    fichas = load_fichas(d)
    schema = S.load_schema("idea")
    valid, rejected = [], []
    for gid, ideas in readable:
        for k, idea in enumerate(ideas, start=1):
            local = (idea.get("local_id") if isinstance(idea, dict) else None) or "%s-%d" % (gid, k)
            if not isinstance(idea, dict):
                rejected.append({"generador": gid, "local_id": local, "motivo": "esquema", "errores": ["no es un objeto"]})
                continue
            body = E.sanitize_obj(S.idea_body(idea))
            errs = S.validate(body, schema)
            if errs:
                rejected.append({"generador": gid, "local_id": local, "titulo": body.get("titulo"), "motivo": "esquema",
                                 "errores": errs[:6]})
                continue
            valid.append((gid, local, body))
    random.Random("idea-arena-ids:%s" % st["seed"]).shuffle(valid)
    width = max(3, len(str(len(valid))))
    prices = check_urls_cached(d, cfg, [it.get("fuente_precio_url") for _, _, b in valid for it in b["costo_infra"]["items"]])
    meta, hard, passing = {}, {}, []
    for i, (gid, local, body) in enumerate(valid, start=1):
        iid = "i%0*d" % (width, i)
        idea = {"id": iid}
        idea.update(body)
        _, words = S.render_page(idea, fichas, cfg)
        problems = S.hard_check(idea, fichas, prices, cfg, page_words=words)
        page, words = S.render_page(idea, fichas, cfg, problems)
        write_json(j(d, "ideas", iid + ".json"), idea)
        write_text(j(d, "ideas", iid + ".md"), page)
        g = gens[gid]
        meta[iid] = {"generador": gid, "local_id": local, "estrategia": g["strategy"], "foco": g["focus"]}
        blocking = S.blocking(problems)
        hard[iid] = {"titulo": idea["titulo"], "pasa": not blocking, "palabras": words,
                     "costo_anual_usd": idea["costo_infra"]["total_anual_usd"],
                     "problemas": [{"codigo": c, "detalle": msg} for c, msg in blocking],
                     "avisos": [{"codigo": c, "detalle": msg} for c, msg in problems if (c, msg) not in blocking]}
        if not blocking:
            passing.append(iid)
    write_json(j(d, "ideas", "meta.json"), {"about": "Lo que el juez no ve: de qué generador y estrategia salió cada idea.",
                                             "ideas": meta})
    write_json(j(d, "ideas", "rechazadas.json"), {"rechazadas": rejected})
    write_json(j(d, "filter", "duro.json"), {"ideas": hard})
    st["scope_batches"] = make_batches(passing, cfg)
    codes = collections.Counter(p["codigo"] for h in hard.values() for p in h["problemas"])
    warns = collections.Counter(p["codigo"] for h in hard.values() for p in h["avisos"])
    st["steps"]["ingest"] = {"recibidas": len(valid) + len(rejected), "validas": len(valid), "rechazadas_esquema": len(rejected),
                             "pasan_filtro_duro": len(passing), "problemas": dict(codes), "avisos": dict(warns)}
    lines.append("ideas: %d recibidas, %d con esquema válido, %d pasan el filtro duro%s%s"
                 % (len(valid) + len(rejected), len(valid), len(passing),
                    " (fallas: %s)" % ", ".join("%s %d" % kv for kv in sorted(codes.items())) if codes else "",
                    "; avisos que no descartan: %s" % ", ".join("%s %d" % kv for kv in sorted(warns.items())) if warns else ""))
    lines.append("chequeo de alcance: %d lote(s)" % len(st["scope_batches"]))
    return lines


def _clip(text, n):
    text = re.sub(r"\s+", " ", str(text)).strip()
    return text if len(text) <= n else text[:n - 3].rstrip() + "..."


def step_scope_collect(d, st, cfg):
    lines, verdicts, pending = [], {}, False
    schema = S.load_schema("alcance")
    for job in phase_jobs(d, st, "scope"):
        path, batch = job["outputs"][0], job["batch"]
        if is_no_output(path):
            for iid in batch:
                verdicts[iid] = {"id": iid, "veredicto": "sin_chequeo", "motivo": "el revisor no produjo salida"}
            continue
        data = parse_json_output(path)
        errs = S.validate(data, schema) if data is not None else ["no es JSON"]
        if not errs and sorted(e["id"] for e in data["evaluaciones"]) != sorted(batch):
            errs = ["las evaluaciones no cubren exactamente el lote: %s" % ", ".join(batch)]
        if errs:
            res = reject_output(path)
            pending = pending or res == "rerun"
            lines.append("  %s: %s" % (job["id"], errs[0]))
            if res != "rerun":
                for iid in batch:
                    verdicts[iid] = {"id": iid, "veredicto": "sin_chequeo", "motivo": "el revisor falló dos veces"}
            continue
        for e in data["evaluaciones"]:
            verdicts[e["id"]] = e
    if pending:
        return lines + ["hay lotes para volver a correr: %s" % _cmd("next")]
    order = [iid for b in st["scope_batches"] for iid in b]
    survivors = [iid for iid in order if verdicts.get(iid, {}).get("veredicto") != "inviable"]
    write_json(j(d, "filter", "alcance.json"), {"evaluaciones": [verdicts[i] for i in order if i in verdicts]})
    ideas = {iid: read_json(j(d, "ideas", iid + ".json")) for iid in survivors}
    groups, links = E.clusters({iid: E.idea_text(ideas[iid]) for iid in survivors}, cfg["filter"]["lexical_threshold"])
    write_json(j(d, "filter", "dedup_lexico.json"), {"umbral": cfg["filter"]["lexical_threshold"],
                                                     "grupos": [g for g in groups if len(g) > 1],
                                                     "pares": [{"a": a, "b": b, "similitud": s} for a, b, s in links]})
    md = ["# Candidatos para deduplicar", ""]
    for iid in survivors:
        idea = ideas[iid]
        md += ["## %s: %s" % (iid, idea["titulo"]), "",
               "- Usuario: %s" % _clip(idea["usuario"], 300),
               "- Problema: %s" % _clip(idea["problema"], 450),
               "- Solución: %s" % _clip(idea["solucion"], 450), ""]
    write_text(j(d, "filter", "candidatos.md"), "\n".join(md))
    st["candidates"] = survivors
    st["dedup_needed"] = bool(cfg["filter"]["dedup_agent"]) and len(survivors) > 1
    tally = collections.Counter(v.get("veredicto") for v in verdicts.values())
    st["steps"]["scope-collect"] = {"evaluadas": len(order), "veredictos": dict(tally), "sobreviven": len(survivors),
                                    "grupos_lexicos": len([g for g in groups if len(g) > 1])}
    lines.append("alcance: %s; siguen %d de %d" % (", ".join("%s %d" % kv for kv in sorted(tally.items())),
                                                    len(survivors), len(order)))
    lines.append("similitud léxica: %d grupo(s) de casi-duplicados" % len([g for g in groups if len(g) > 1]))
    return lines


def step_select(d, st, cfg):
    lines, cands = [], list(st["candidates"])
    agent_groups = []
    if st.get("dedup_needed"):
        path = j(d, "filter", "dedup.json")
        if not is_no_output(path):
            data = parse_json_output(path)
            errs = S.validate(data, S.load_schema("dedup")) if data is not None else ["no es JSON"]
            if not errs:
                flat = [x for g in data["grupos"] for x in g]
                if sorted(flat) != sorted(cands):
                    errs = ["cada candidato tiene que estar en exactamente un grupo"]
            if errs:
                res = reject_output(path)
                if res == "rerun":
                    return ["  dedup: %s" % errs[0], "hay que volver a correr el deduplicador: %s" % _cmd("next")]
                lines.append("  dedup: falló dos veces; se usa solo la similitud léxica")
            else:
                agent_groups = data["grupos"]
    ideas = {iid: read_json(j(d, "ideas", iid + ".json")) for iid in cands}
    meta = read_json(j(d, "ideas", "meta.json"), {}).get("ideas", {})
    fichas = load_fichas(d)
    groups, _ = E.clusters({iid: E.idea_text(ideas[iid]) for iid in cands}, cfg["filter"]["lexical_threshold"],
                           extra_groups=agent_groups)
    rng = random.Random("idea-arena-select:%s" % st["seed"])
    tie = {iid: rng.random() for iid in sorted(cands)}
    strength = {iid: evidence_strength(ideas[iid], fichas) for iid in cands}
    reps, merged = [], []
    for g in groups:
        best = max(g, key=lambda i: (strength[i][0], strength[i][1], -float(ideas[i]["costo_infra"]["total_anual_usd"]), tie[i]))
        reps.append(best)
        if len(g) > 1:
            merged.append({"queda": best, "fuera": [x for x in g if x != best]})
    sector_of = {iid: primary_sector(ideas[iid], fichas, (meta.get(iid, {}).get("foco") or ["transversal"])[0])
                 for iid in reps}
    themes, _ = E.clusters({iid: [c for c in S.problem_ids(ideas[iid]) if c in fichas] for iid in reps},
                           cfg["filter"].get("theme_overlap", 0.5), sim=E.overlap)
    theme_of = {iid: k for k, g in enumerate(themes) for iid in g}
    by = {}
    for iid in reps:
        by.setdefault(sector_of[iid], []).append(iid)
    for s, lst in by.items():
        lst.sort(key=lambda i: (-strength[i][0], -strength[i][1], tie[i]))
        by[s] = theme_first(lst, theme_of)
    sector_order = [s["id"] for s in st["sectors"] if s["id"] in by] + sorted(s for s in by if s not in [x["id"] for x in st["sectors"]])
    limit = cfg["selection"]["max_candidates"]
    selected = []
    while len(selected) < limit and any(by.values()):
        for s in sector_order:
            if by[s] and len(selected) < limit:
                selected.append(by[s].pop(0))
    shared = [g for g in themes if len(g) > 1]
    write_json(j(d, "filter", "seleccion.json"), {"seleccionadas": selected, "fusionadas": merged,
                                                  "sector_principal": sector_of, "temas_compartidos": shared,
                                                  "fuera_por_cupo": [x for lst in by.values() for x in lst]})
    write_filter_report(d, st, cfg, ideas, selected, merged, shared)
    if not selected:
        raise IdeaArenaError("ninguna idea llegó al torneo. Mirá %s" % j(d, "filter", "reporte.md"))
    tcfg = cfg["tournament"]
    entries = [(iid, sector_of[iid], j(d, "ideas", iid + ".md"), j(d, "ideas", iid + ".json")) for iid in sorted(selected)]
    ts = T.new_tournament(entries, st["seed"], j(d, "tournament"), tcfg["persona_order"],
                          tcfg["personas_per_match"], tcfg["judge_both_orders"])
    save_tournament(d, ts)
    st["selected"] = selected
    st["steps"]["select"] = {"grupos": len(groups), "fusionadas": sum(len(m["fuera"]) for m in merged),
                             "seleccionadas": len(selected)}
    rounds = len(B.bracket_sizes(len(selected))) - 1
    lines.append("selección: %d ideas al torneo (%d fusionadas como duplicadas). %d ronda(s)."
                 % (len(selected), sum(len(m["fuera"]) for m in merged), rounds))
    if ts["champion"]:
        lines.append("una sola idea: no hay cruces, es la campeona directamente")
    return lines


def theme_first(ids, theme_of):
    """ids in their order, but the first idea of every theme before the second of any. When the
    bracket has fewer slots than ideas, distinct problems get in before variations of one."""
    seen, rank = collections.Counter(), {}
    for i in ids:
        rank[i] = seen[theme_of[i]]
        seen[theme_of[i]] += 1
    return sorted(ids, key=lambda i: rank[i])


def write_filter_report(d, st, cfg, ideas, selected, merged, shared_themes=()):
    hard = read_json(j(d, "filter", "duro.json"), {}).get("ideas", {})
    scope = read_json(j(d, "filter", "alcance.json"), {}).get("evaluaciones", [])
    rejected = read_json(j(d, "ideas", "rechazadas.json"), {}).get("rechazadas", [])
    steps = st["steps"]
    L = ["# Reporte del filtro", "", "Run `%s`." % st["run"], "", "## Embudo", ""]
    v = steps.get("verify", {})
    L.append("- Fichas: %s aceptadas (%s ok, %s bloqueadas), %s descartadas."
             % (v.get("aceptadas"), v.get("ok"), v.get("bloqueadas"), v.get("descartadas")))
    ing = steps.get("ingest", {})
    L.append("- Ideas: %s recibidas, %s con esquema válido, %s pasan el filtro duro."
             % (ing.get("recibidas"), ing.get("validas"), ing.get("pasan_filtro_duro")))
    sc = steps.get("scope-collect", {})
    L.append("- Alcance: %s siguen." % sc.get("sobreviven"))
    L.append("- Deduplicación: %d fusionadas." % sum(len(m["fuera"]) for m in merged))
    L.append("- Torneo: %d ideas." % len(selected))
    L += ["", "## Filtro duro", "", "Los avisos no descartan la idea: se muestran en su página para que el juez los pese.", "",
          "| Idea | Título | Pasa | Problemas | Avisos |", "| --- | --- | --- | --- | --- |"]
    for iid in sorted(hard):
        h = hard[iid]
        L.append("| %s | %s | %s | %s | %s |" % (iid, S.cell(h["titulo"]), "sí" if h["pasa"] else "no",
                                               S.cell("; ".join(p["detalle"] for p in h["problemas"]) or "-"),
                                               S.cell("; ".join(p["detalle"] for p in h.get("avisos", [])) or "-")))
    if rejected:
        L += ["", "## Rechazadas por esquema", ""]
        L += ["- %s (%s): %s" % (r["local_id"], r.get("titulo") or "sin título", "; ".join(r["errores"][:3])) for r in rejected]
    L += ["", "## Alcance", "", "| Idea | Veredicto | Horas | Motivo | Recorte sugerido |", "| --- | --- | --- | --- | --- |"]
    for e in scope:
        L.append("| %s | %s | %s | %s | %s |" % (e["id"], e.get("veredicto"), e.get("horas_estimadas", "-"),
                                               S.cell(e.get("motivo", "")), S.cell(e.get("recorte_sugerido", "") or "-")))
    L += ["", "## Duplicados", ""]
    L += ["- Queda %s; salen %s." % (m["queda"], ", ".join(m["fuera"])) for m in merged] or ["- Ninguno."]
    L += ["", "## Temas compartidos", "",
          "Ideas distintas cuyo problema se apoya en casi las mismas fichas: atacan el mismo dolor. Si sobran "
          "ideas para el cupo del torneo, entra primero una por tema.", ""]
    L += ["- %s" % ", ".join("%s (%s)" % (iid, ideas[iid]["titulo"]) for iid in g) for g in shared_themes] or ["- Ninguno."]
    L += ["", "## Al torneo", ""]
    L += ["- %s: %s" % (iid, ideas[iid]["titulo"]) for iid in selected] or ["- Ninguna."]
    write_text(j(d, "filter", "reporte.md"), "\n".join(L) + "\n")


def relabel_attacks(attacks, fichas):
    out = []
    for a in attacks:
        a = dict(a)
        cited = [e for e in (a.get("evidencia") or []) if isinstance(e, str)]
        a["evidencia"] = [e for e in cited if e in fichas]
        dropped = [e for e in cited if e not in fichas]
        if a["tipo"] == "evidencia" and not a["evidencia"]:
            a["tipo"] = "opinion"
            a["reetiquetado"] = ("sus citas no existen o se descartaron: %s" % ", ".join(dropped)) if dropped else "no citó evidencia"
        elif dropped:
            a["citas_descartadas"] = dropped
        out.append(a)
    return out


def render_attacks(entries, personas, n):
    L = ["# Ataques recibidos (ronda %d)" % n, "",
         "Python verificó las citas: un ataque sin evidencia verificable figura como opinión.", ""]
    k = 0
    for pid, attacks, discarded in entries:
        L += ["## Persona: %s" % personas[pid]["name"], ""]
        if attacks is None:
            L += ["El atacante no produjo salida: no hubo ataques de esta persona.", ""]
            continue
        if not attacks:
            L += ["No hubo ataques.", ""]
        for a in attacks:
            k += 1
            if a["tipo"] == "evidencia":
                backing = "evidencia %s" % ", ".join(a["evidencia"])
            else:
                backing = "opinión" + (" (reetiquetado: %s)" % a["reetiquetado"] if a.get("reetiquetado") else "")
            L += ["ATAQUE %d [%s] %s" % (k, a["severidad"], a["titulo"]), "Dónde: %s" % (a.get("donde") or "-"),
                  "Problema: %s" % a["problema"], "Respaldo: %s" % backing, ""]
        if discarded:
            L += ["Fichas nuevas descartadas por Python: %s" % "; ".join("%s (%s)" % (x.get("id"), x["motivo"]) for x in discarded), ""]
    if k == 0:
        L += ["En total: no hubo ataques.", ""]
    return "\n".join(L)


def step_check_attacks(d, st, cfg):
    ts = load_tournament(d)
    rd = B.current_round(ts)
    n, lines = rd["n"], []
    personas = load_personas(j(d, "inputs", "personas.json"))
    schema = S.load_schema("ataque")
    for m in rd["matches"]:
        if m["winner"] or m.get("attacks_checked"):
            continue
        pending, parsed = False, {}
        for iid in (m["first"], m["second"]):
            for p in m["personas"]:
                path = T.attack_json(ts, n, m["id"], iid, p)
                if not has_output(path):
                    pending = True
                    continue
                if is_no_output(path):
                    parsed[(iid, p)] = None
                    continue
                data = parse_json_output(path)
                errs = S.validate(data, schema) if data is not None else ["no es JSON"]
                if errs:
                    res = reject_output(path)
                    lines.append("  %s %s: ataque ilegible (%s), %s" % (m["id"], iid, errs[0],
                                                                         "se vuelve a correr" if res == "rerun" else "queda sin ataques"))
                    if res == "rerun":
                        pending = True
                    else:
                        parsed[(iid, p)] = None
                    continue
                parsed[(iid, p)] = data
        if pending:
            continue
        for iid in (m["first"], m["second"]):
            entries = []
            for p in m["personas"]:
                data = parsed[(iid, p)]
                if data is None:
                    entries.append((p, None, []))
                    continue
                _, dis = accept_new_fichas(d, cfg, data.get("nuevas_fichas"), ficha_prefix("attack", m["id"], iid, p),
                                           "evidence/fichas_torneo.json", "%s ataque %s a %s" % (m["id"], p, iid))
                entries.append((p, relabel_attacks(data["ataques"], load_fichas(d)), dis))
            write_text(T.attacks_md(ts, n, m["id"], iid), render_attacks(entries, personas, n))
        m["attacks_checked"] = True
        lines.append("  %s: ataques verificados" % m["id"])
    save_tournament(d, ts)
    write_all_fichas(d)
    return lines


def render_defense(defense, notes):
    L = ["# Defensa", ""]
    if defense is None:
        L.append("El defensor no produjo una defensa válida.")
    elif not defense["respuestas"]:
        L.append("Sin respuestas (no hubo ataques, o no respondió ninguno).")
    for r in (defense or {}).get("respuestas", []):
        ev = " (evidencia: %s)" % ", ".join(r["evidencia"]) if r.get("evidencia") else ""
        L.append("ATAQUE %d: %s. %s%s" % (r["ataque"], r["decision"], r["detalle"], ev))
    if notes:
        L += ["", "## Notas de Python", ""] + ["- %s" % x for x in notes]
    return "\n".join(L) + "\n"


def step_revise(d, st, cfg):
    ts = load_tournament(d)
    rd = B.current_round(ts)
    n, lines = rd["n"], []
    sdef, sidea = S.load_schema("defensa"), S.load_schema("idea")
    for m in rd["matches"]:
        if m["winner"] or m.get("revised"):
            continue
        pending, staged = False, {}
        for iid in (m["first"], m["second"]):
            dpath, ipath = T.defense_json(ts, n, m["id"], iid), T.revised_json(ts, n, m["id"], iid)
            if not has_output(dpath) or not has_output(ipath):
                pending = True
                continue
            defense = None
            if not is_no_output(dpath):
                defense = parse_json_output(dpath)
                errs = S.validate(defense, sdef) if defense is not None else ["no es JSON"]
                if errs:
                    res = reject_output(dpath)
                    lines.append("  %s %s: defensa ilegible (%s)" % (m["id"], iid, errs[0]))
                    defense = None
                    if res == "rerun":
                        pending = True
                        continue
            idea = None
            if not is_no_output(ipath):
                idea = parse_json_output(ipath)
                errs = S.validate(S.idea_body(idea), sidea) if idea is not None else ["no es JSON"]
                if errs:
                    res = reject_output(ipath)
                    lines.append("  %s %s: idea revisada inválida (%s)" % (m["id"], iid, errs[0]))
                    idea = None
                    if res == "rerun":
                        pending = True
                        continue
            staged[iid] = (defense, idea)
        if pending:
            continue
        m["det_fatal"], m["hard_notes"] = {}, {}
        for iid, (defense, idea) in staged.items():
            notes = []
            if defense:
                _, dis = accept_new_fichas(d, cfg, defense.get("nuevas_fichas"), ficha_prefix("defend", m["id"], iid),
                                           "evidence/fichas_torneo.json", "%s defensa de %s" % (m["id"], iid))
                notes += ["ficha nueva descartada: %s (%s)" % (x.get("id"), x["motivo"]) for x in dis]
            if idea is None:
                idea = read_json(ts["agents"][iid]["idea_json"])
                notes.append("la revisión no fue válida: se juzga la versión anterior")
            fichas = load_fichas(d)
            full = {"id": iid}
            full.update(E.sanitize_obj(S.idea_body(idea)))
            prices = check_urls_cached(d, cfg, [it.get("fuente_precio_url") for it in full["costo_infra"]["items"]])
            _, words = S.render_page(full, fichas, cfg)
            problems = S.hard_check(full, fichas, prices, cfg, page_words=words)
            page, _ = S.render_page(full, fichas, cfg, problems)
            write_json(T.revised_json(ts, n, m["id"], iid), full)
            write_text(T.solution_md(ts, n, m["id"], iid), page)
            write_text(T.defense_md(ts, n, m["id"], iid), render_defense(defense, notes))
            m["det_fatal"][iid] = S.fatal_codes(problems)
            m["hard_notes"][iid] = ["%s: %s" % (c, msg) for c, msg in problems] + notes
        m["revised"] = True
        fat = ["%s (%s)" % (iid, ", ".join(c)) for iid, c in sorted(m["det_fatal"].items()) if c]
        lines.append("  %s: ideas revisadas%s" % (m["id"], "; fatal determinístico: %s" % "; ".join(fat) if fat else ""))
    save_tournament(d, ts)
    write_all_fichas(d)
    return lines


def _read_verdict(path, x, y):
    v = None if is_no_output(path) else parse_json_output(path)
    return T.normalize_verdict(v, x, y)


def step_collect(d, st, cfg):
    ts = load_tournament(d)
    rd = B.current_round(ts)
    n, lines = rd["n"], []
    hard_ids = run_hard_ids(d)
    for m in rd["matches"]:
        if m["winner"]:
            continue
        paths = [(T.verdict_json(ts, n, m["id"]), m["first"], m["second"])]
        if ts["judge_both_orders"]:
            paths.append((T.verdict_json(ts, n, m["id"], True), m["second"], m["first"]))
        nvs, bad = [], False
        for path, x, y in paths:
            if not has_output(path):
                lines.append("  %s: falta el veredicto" % m["id"])
                bad = True
                continue
            try:
                nvs.append(_read_verdict(path, x, y))
            except T.ArenaError as e:
                res = reject_output(path, fallback=False, max_attempts=3)
                lines.append("  %s: veredicto ilegible (%s), %s" % (m["id"], e, "se vuelve a correr el juez" if res == "rerun"
                                                                   else "tercer intento: decidilo con record"))
                bad = True
        if bad:
            continue
        nv = T.merge_verdicts(nvs, m["a"], m["b"])
        try:
            winner, totals, fatal, notes = T.decide(nv, m["a"], m["b"], hard_ids, m.get("det_fatal"))
        except T.ArenaError as e:
            for path, _, _ in paths:
                reject_output(path, fallback=False, max_attempts=3)
            lines.append("  %s: %s; se vuelve a correr el juez" % (m["id"], e))
            continue
        if len(nvs) == 2:
            per = []
            for one in nvs:
                try:
                    per.append(T.decide(one, m["a"], m["b"], hard_ids, m.get("det_fatal"))[0])
                except T.ArenaError:
                    per.append(None)
            if per[0] != per[1]:
                notes.append("los dos órdenes de presentación no coinciden: decidió el promedio")
        B.record(ts, m["id"], winner, reason=" | ".join(r for r in nv["reasons"] if r)[:400],
                 survived=nv["survived"], scores=totals, source="judge")
        m["fatal"] = fatal
        m["criteria"] = {iid: {k: v for k, v in (nv["scores"].get(iid) or {}).items() if k != "fatal_claims"}
                         for iid in (m["a"], m["b"])}
        m["fatal_motivos"] = {iid: [mot for c, mot in (nv["scores"].get(iid) or {}).get("fatal_claims", []) if c]
                              for iid in (m["a"], m["b"])}
        m["standing"] = nv["standing"]
        m["notes"] = notes
        lines.append("  %s: %s le gana a %s, %s a %s%s" % (m["id"], winner, m["loser"], fmt(totals[winner]),
                                                           fmt(totals[m["loser"]]), ". " + "; ".join(notes) if notes else ""))
    save_tournament(d, ts)
    return lines


def step_advance(d, st, cfg):
    ts = load_tournament(d)
    closing = B.current_round(ts)["n"]
    survivors = T.advance_round(ts)
    save_tournament(d, ts)
    total = len(B.bracket_sizes(ts["agents_n"])) - 1
    if ts["champion"]:
        idea, _ = latest_idea(d, ts["champion"], ts)
        return ["ronda %d de %d cerrada. Campeona: %s, %s" % (closing, total, ts["champion"], idea["titulo"])]
    return ["ronda %d de %d cerrada: quedan %d de %d ideas" % (closing, total, len(survivors), ts["agents_n"])]


def _trail(d, ts, iid, personas):
    """(markdown table and lists of an idea's matches, the attacks left standing)."""
    L = ["| Ronda | Rival | Persona | Puntaje | Resultado | Motivo del juez |", "| --- | --- | --- | --- | --- | --- |"]
    standing, notes = [], []
    for r in T.trail(ts, iid):
        if r["bye"]:
            L.append("| %d | (bye) | - | - | pasa sin cruce | - |" % r["round"])
            continue
        opp_title = latest_idea(d, r["opponent"], ts)[0]["titulo"]
        res = "ganó" if r["won"] else "perdió" if r["won"] is False else "abierto"
        if r["fatal"]:
            res += ", con fallo fatal"
        L.append("| %d | %s (%s) | %s | %s a %s | %s | %s |" % (
            r["round"], S.cell(opp_title), r["opponent"], ", ".join(personas[p]["name"] for p in r["personas"]),
            fmt(r["score"]), fmt(r["opponent_score"]), res, S.cell(r["reason"] or "-")))
        standing += ["ronda %d: %s" % (r["round"], s) for s in r["standing"]]
        notes += ["ronda %d: %s" % (r["round"], x) for x in r["notes"]]
    L += ["", "Ataques que quedaron en pie:", ""] + (["- %s" % s for s in standing] or ["- Ninguno registrado."])
    if notes:
        L += ["", "Notas de Python:", ""] + ["- %s" % x for x in notes]
    return "\n".join(L), standing


def _trail_md(d, ts, iid, personas):
    idea, page = latest_idea(d, iid, ts)
    body, _ = _trail(d, ts, iid, personas)
    return "\n".join(["# Paso por el torneo: %s (%s)" % (idea["titulo"], iid), "", body, "",
                      "Página de la idea (última versión): %s" % _slash(os.path.relpath(page, j(d, "shortlist", "rastro")))]) + "\n"


def step_rank(d, st, cfg):
    ts = load_tournament(d)
    personas = load_personas(j(d, "inputs", "personas.json"))
    rows = T.ranking(ts)
    for r in rows:
        r["titulo"] = latest_idea(d, r["id"], ts)[0]["titulo"]
    # A verified fatal flaw breaks a hard restriction: those ideas are ranked but never recommended.
    eligible = [r for r in rows if not r["fatal"]]
    k = min(cfg["shortlist"]["size"], cfg["limits"]["questions"], len(eligible))
    shortlist = [r["id"] for r in eligible[:k]]
    excluded = [r["id"] for r in rows if r["fatal"]]
    for iid in shortlist:
        write_text(j(d, "shortlist", "rastro", iid + ".md"), _trail_md(d, ts, iid, personas))
    write_json(j(d, "shortlist", "ranking.json"), {"ranking": rows, "top": shortlist, "excluidas_por_fallo_fatal": excluded})
    st["shortlist"] = shortlist
    st["steps"]["rank"] = {"top": shortlist, "excluidas_por_fallo_fatal": excluded}
    lines = ["top %d: %s" % (k, ", ".join("%s %s" % (r["id"], _clip(r["titulo"], 50)) for r in eligible[:k]))]
    if excluded:
        lines.append("fuera de la shortlist por fallo fatal en su último cruce: %s" % ", ".join(excluded))
    return lines


MODE_NAMES = {"pilot": "piloto", "full": "completo", "calibration": "calibración"}


def _result_line(r, titles):
    if r["champion"]:
        line = "campeona"
    elif r["eliminated_in"]:
        line = "eliminada en la ronda %d por %s" % (r["eliminated_in"], _clip(titles.get(r["eliminated_by"], r["eliminated_by"]), 40))
    else:
        line = "sin cruces"
    return line + (", con fallo fatal" if r.get("fatal") else "")


def step_shortlist(d, st, cfg):
    nq = cfg["shortlist"]["questions_per_idea"]
    schema = S.load_schema("preguntas")
    questions, lines, pending = {}, [], False
    for job in phase_jobs(d, st, "questions"):
        path, iid = job["outputs"][0], job["idea"]
        if is_no_output(path):
            questions[iid] = None
            continue
        data = parse_json_output(path)
        errs = S.validate(data, schema) if data is not None else ["no es JSON"]
        if not errs and len(data["preguntas"]) != nq:
            errs = ["hacen falta exactamente %d preguntas" % nq]
        if errs:
            res = reject_output(path)
            lines.append("  %s: preguntas inválidas (%s)" % (iid, errs[0]))
            if res == "rerun":
                pending = True
            else:
                questions[iid] = None
            continue
        questions[iid] = data["preguntas"]
    if pending:
        return lines + ["hay preguntas para volver a correr: %s" % _cmd("next")]
    ts = load_tournament(d)
    personas = load_personas(j(d, "inputs", "personas.json"))
    rows = read_json(j(d, "shortlist", "ranking.json"))["ranking"]
    titles = {r["id"]: r["titulo"] for r in rows}
    fichas = load_fichas(d)
    template = page_template("guion_entrevista")
    top = [r for r in rows if r["id"] in st["shortlist"]]
    L = ["# Shortlist de ideas de tesis", "",
         "Run `%s`, modo %s, semilla %s, creado %s. Generado por /idea-arena." % (st["run"], MODE_NAMES.get(st["mode"], st["mode"]),
                                                                                   st["seed"], st["created"]),
         "", "Cómo leer esto:",
         "- El puesto 1 ganó todos sus cruces y el 2 perdió solo la final. Más abajo, el orden de una eliminación simple es "
         "ruidoso: dos ideas eliminadas en la misma ronda se ordenan por el puntaje que sacaron al perder, contra rivales distintos.",
         "- Cada idea es la última versión revisada que tuvo en el torneo.",
         "- Nada de esto reemplaza hablar con el mercado: para eso están las preguntas y el guion de cada idea.",
         "- Una idea que perdió su último cruce con un fallo fatal verificado (viola una restricción dura o se apoya en "
         "una afirmación sin evidencia) no se recomienda. Fuera por eso: %s." % (", ".join(
             "%s (%s)" % (titles[x], x) for x in st["steps"]["rank"].get("excluidas_por_fallo_fatal", [])) or "ninguna"),
         "", "## Resumen", "",
         "| # | Idea | Resultado en el torneo | Costo USD/año | Fichas citadas (ok / bloqueadas) |",
         "| --- | --- | --- | --- | --- |"]
    blocks = []
    for r in top:
        iid = r["id"]
        idea, page = latest_idea(d, iid, ts)
        valid = [c for c in S.cited_ids(idea) if c in fichas]
        ok = sum(1 for c in valid if S.ficha_estado(fichas[c]) == E.OK)
        L.append("| %d | %s (%s) | %s | %g | %d / %d |" % (r["rank"], S.cell(idea["titulo"]), iid, _result_line(r, titles),
                                                         idea["costo_infra"]["total_anual_usd"], ok, len(valid) - ok))
        trail_body, standing = _trail(d, ts, iid, personas)
        qs = questions.get(iid)
        q_lines = (["%d. %s (a quién: %s; valida: %s)" % (i, q["pregunta"], q["a_quien"], q["que_valida"])
                    for i, q in enumerate(qs, start=1)] if qs else
                   ["Sin preguntas: el agente no produjo una salida válida. Corré deepen o escribilas a mano."])
        guion = B.fill(template, {
            "titulo": idea["titulo"], "usuario": idea["usuario"], "problema": idea["problema"], "run": st["run"],
            "preguntas": "\n".join(q_lines),
            "supuestos": "\n".join("- %s" % s for s in idea["supuestos"]) or "- Ninguno declarado.",
            "en_pie": "\n".join("- %s" % s for s in standing) or "- Ninguno registrado."})
        write_text(j(d, "shortlist", "guiones", iid + ".md"), guion)
        blocks +=["", "## %d. %s (%s)" % (r["rank"], idea["titulo"], iid), "",
                   "Página completa: [%s](%s). Resultado: %s." % (_slash(os.path.relpath(page, d)), _slash(os.path.relpath(page, d)),
                                                                 _result_line(r, titles)), "",
                   "**Problema.** %s" % idea["problema"], "", "**Usuario.** %s" % idea["usuario"], "",
                   "**Solución.** %s" % idea["solucion"], "",
                   "**Costo de infraestructura.** USD %g por año (tope USD %g)." % (idea["costo_infra"]["total_anual_usd"], cfg["infra_budget_usd"]),
                   "", "### Rastro de veredictos", "", trail_body, "",
                   "### Preguntas para validar con el mercado", ""] + q_lines + [
                   "", "### Guion de entrevista", "", "[shortlist/guiones/%s.md](shortlist/guiones/%s.md)" % (iid, iid), "",
                   "### Profundizar", "", "`%s`" % _cmd("deepen", iid)]
    sv, ing, sc, sel = (st["steps"].get(k, {}) for k in ("verify", "ingest", "scope-collect", "select"))
    L += blocks + ["", "## El embudo", "",
                   "- Fichas: %s aceptadas (%s ok, %s bloqueadas), %s descartadas." % (sv.get("aceptadas"), sv.get("ok"), sv.get("bloqueadas"), sv.get("descartadas")),
                   "- Ideas: %s recibidas, %s pasan el filtro duro, %s pasan el alcance." % (ing.get("recibidas"), ing.get("pasan_filtro_duro"), sc.get("sobreviven")),
                   "- Torneo: %s ideas, %d ronda(s)." % (sel.get("seleccionadas"), len(ts["rounds"])),
                   "- Detalle del filtro: [filter/reporte.md](filter/reporte.md).", ""]
    write_text(j(d, "shortlist.md"), "\n".join(L))
    st["steps"]["shortlist"] = {"ideas": [r["id"] for r in top]}
    return lines + ["shortlist: %s" % j(d, "shortlist.md")]


def step_deepen_collect(d, st, cfg):
    lines, pending = [], False
    for iid, req in sorted(st["deepen"].items()):
        if req.get("collected"):
            continue
        summary = []
        for a in req["aspects"]:
            path = j(d, "deepen", iid, a + ".fichas.json")
            if is_no_output(path):
                summary.append("- %s: sin fichas nuevas (salida vacía)" % a)
                continue
            data = parse_json_output(path)
            if data is None or not isinstance(data.get("nuevas_fichas"), list):
                res = reject_output(path)
                lines.append("  %s %s: fichas ilegibles" % (iid, a))
                if res == "rerun":
                    pending = True
                continue
            acc, dis = accept_new_fichas(d, cfg, data["nuevas_fichas"], ficha_prefix("deepen", iid=iid, aspect=a),
                                         "evidence/fichas_profundizar.json", "profundizar %s %s" % (iid, a))
            summary.append("- [%s](%s.md): %d ficha(s) verificadas, %d descartadas%s"
                           % (a, a, len(acc), len(dis), " (%s)" % ", ".join("%s: %s" % (x.get("id"), x["motivo"]) for x in dis) if dis else ""))
        if pending:
            continue
        idea, page = latest_idea(d, iid, load_tournament(d))
        write_text(j(d, "deepen", iid, "README.md"), "\n".join(
            ["# Profundización: %s (%s)" % (idea["titulo"], iid), "",
             "Idea: %s" % _slash(os.path.relpath(page, j(d, "deepen", iid))), ""] + summary +
            ["", "Las fichas nuevas verificadas están en evidence/fichas_profundizar.json."]) + "\n")
        req["collected"] = True
        lines.append("  %s: profundización lista en %s" % (iid, j(d, "deepen", iid)))
    write_all_fichas(d)
    return lines


# ---------------------------------------------------------------- calibration

_RANK_RE = re.compile(r"^\s*(\d+)[.)]\s*`?([A-Za-z0-9_-]+)`?", re.M)


def parse_ranking(text, names):
    found = sorted((int(n), name) for n, name in _RANK_RE.findall(text) if name in names)
    order = [name for _, name in found]
    if sorted(order) != sorted(names):
        raise IdeaArenaError("my_ranking.md tiene que listar cada idea exactamente una vez: %s" % ", ".join(sorted(names)))
    return order


def kendall_tau(a, b):
    pos = {x: i for i, x in enumerate(b)}
    c = dd = 0
    for x, y in itertools.combinations(a, 2):
        if pos[x] < pos[y]:
            c += 1
        else:
            dd += 1
    total = c + dd
    return round((c - dd) / float(total), 3) if total else 1.0


def calibration_metrics(user_order, results):
    """results: [{"x", "y", "winner", "totals": {name: total}, "criteria": {name: {criterion: score}}}]."""
    pos = {name: i for i, name in enumerate(user_order)}
    pairs = {}
    for r in results:
        pairs.setdefault(tuple(sorted((r["x"], r["y"]), key=pos.get)), []).append(r)
    rows, agree, consistent = [], 0, 0
    for (a, b), rs in sorted(pairs.items(), key=lambda kv: (pos[kv[0][0]], pos[kv[0][1]])):
        winners = [r["winner"] for r in rs]
        cons = len(set(winners)) == 1
        if cons:
            pref = winners[0]
        else:
            sa = sum(r["totals"].get(a) or 0 for r in rs)
            sb = sum(r["totals"].get(b) or 0 for r in rs)
            pref = a if sa >= sb else b
        ok = pref == a   # a is the one you ranked higher
        agree += ok
        consistent += cons
        diffs = {}
        for key, _ in T.CRITERIA:
            va = [T._num(r["criteria"].get(a, {}).get(key)) for r in rs]
            vb = [T._num(r["criteria"].get(b, {}).get(key)) for r in rs]
            va, vb = [x for x in va if x is not None], [x for x in vb if x is not None]
            if va and vb:
                diffs[key] = round(sum(va) / len(va) - sum(vb) / len(vb), 2)
        rows.append({"tu_preferida": a, "otra": b, "juez_prefiere": pref, "coincide": ok, "ordenes_coinciden": cons,
                     "diferencia_por_criterio": diffs})
    wins = collections.Counter(r["winner"] for r in results)
    tot = collections.Counter()
    for r in results:
        for name, t in r["totals"].items():
            tot[name] += t or 0
    judge_order = sorted(user_order, key=lambda n: (-wins[n], -tot[n], n))
    means = {}
    for name in user_order:
        means[name] = {}
        for key, _ in T.CRITERIA:
            vals = [T._num(r["criteria"].get(name, {}).get(key)) for r in results if name in r["criteria"]]
            vals = [v for v in vals if v is not None]
            means[name][key] = round(sum(vals) / len(vals), 2) if vals else None
    return {"pares": rows, "acuerdo": agree, "total_pares": len(rows), "consistencia": consistent,
            "kendall_tau": kendall_tau(user_order, judge_order), "orden_juez": judge_order, "orden_tuyo": list(user_order),
            "x_gana": round(sum(1 for r in results if r["winner"] == r["x"]) / float(len(results)), 3) if results else None,
            "medias_por_criterio": means}


def calibration_report(st, met):
    L = ["# Calibración del juez", "", "Run `%s`, semilla %s." % (st["run"], st["seed"]), "",
         "## Resultado", "",
         "- Acuerdo por pares con tu ranking: **%d de %d**." % (met["acuerdo"], met["total_pares"]),
         "- Tau de Kendall entre tu orden y el del juez: **%s** (1 = mismo orden, -1 = invertido)." % met["kendall_tau"],
         "- Tu orden: %s. El del juez: %s." % (" > ".join(met["orden_tuyo"]), " > ".join(met["orden_juez"])),
         "- Pares en los que los dos órdenes de presentación dieron el mismo ganador: %d de %d." % (met["consistencia"], met["total_pares"]),
         "- La idea mostrada primero (X) ganó el %s de las veces. Lejos del 50%% indica sesgo de posición." %
         ("%d%%" % round(100 * met["x_gana"]) if met["x_gana"] is not None else "?"),
         "", "## Por par", "",
         "| Tu preferida | La otra | El juez prefiere | Coincide | Órdenes coinciden | Criterios en contra de tu preferida |",
         "| --- | --- | --- | --- | --- | --- |"]
    for p in met["pares"]:
        against = ", ".join("%s %+g" % (k, v) for k, v in sorted(p["diferencia_por_criterio"].items(), key=lambda kv: kv[1]) if v < 0)
        L.append("| %s | %s | %s | %s | %s | %s |" % (p["tu_preferida"], p["otra"], p["juez_prefiere"], "sí" if p["coincide"] else "no",
                                                     "sí" if p["ordenes_coinciden"] else "no", against or "-"))
    L += ["", "## Puntaje medio por criterio", "", "| Idea | %s |" % " | ".join(k for k, _ in T.CRITERIA),
          "| --- |%s" % (" --- |" * len(T.CRITERIA))]
    for name in met["orden_tuyo"]:
        L.append("| %s | %s |" % (name, " | ".join(fmt(met["medias_por_criterio"][name][k]) for k, _ in T.CRITERIA)))
    L += ["", "## Cómo usar esto", "",
          "- Si el juez no coincide con vos, mirá la columna de criterios en contra: son los criterios en los que tu idea "
          "preferida puntuó menos. Si creés que ese criterio no debería pesar tanto, ajustá su peso (en rubric.md, "
          "constraints.md y CRITERIA en ia_tournament.py) o sus anclas en rubric.md.",
          "- Si los dos órdenes no coinciden seguido, o X gana mucho más del 50%, activá tournament.judge_both_orders en config.json.",
          "- Con 3 ideas la señal es gruesa: un desacuerdo puede ser ruido. Agregá ideas en calibration/ideas/ si querés más señal.",
          "- Corré la calibración de nuevo después de cada ajuste."]
    return "\n".join(L) + "\n"


def step_calibration_report(d, st, cfg):
    hard_ids = run_hard_ids(d)
    results, lines, pending = [], [], False
    for job in phase_jobs(d, st, "calibrate"):
        path = job["outputs"][0]
        try:
            nv = _read_verdict(path, job["x"], job["y"])
            winner, totals, fatal, notes = T.decide(nv, job["x"], job["y"], hard_ids)
        except T.ArenaError as e:
            res = reject_output(path, fallback=False, max_attempts=3)
            lines.append("  %s: %s, %s" % (job["id"], e, "se vuelve a correr" if res == "rerun" else "tercer intento fallido"))
            pending = True
            continue
        results.append({"x": job["x"], "y": job["y"], "winner": winner, "totals": totals, "fatal": fatal, "notes": notes,
                        "criteria": {k: {c: v for c, v in s.items() if c != "fatal_claims"} for k, s in nv["scores"].items()}})
    if pending:
        return lines + ["hay jueces de calibración para volver a correr: %s" % _cmd("next")]
    met = calibration_metrics(st["calibration"]["ranking"], results)
    write_json(j(d, "calibration", "resultados.json"), {"veredictos": results, "metricas": met})
    write_text(j(d, "calibration_report.md"), calibration_report(st, met))
    st["steps"]["calibration-report"] = {"acuerdo": met["acuerdo"], "pares": met["total_pares"], "kendall_tau": met["kendall_tau"]}
    return lines + ["acuerdo %d de %d pares, tau de Kendall %s. Reporte: %s"
                    % (met["acuerdo"], met["total_pares"], met["kendall_tau"], j(d, "calibration_report.md"))]


STEPS = {"verify": step_verify, "ingest": step_ingest, "scope-collect": step_scope_collect, "select": step_select,
         "check-attacks": step_check_attacks, "revise": step_revise, "collect": step_collect, "advance": step_advance,
         "rank": step_rank, "shortlist": step_shortlist, "deepen-collect": step_deepen_collect,
         "calibration-report": step_calibration_report}


# ---------------------------------------------------------------- commands

def _seed(args, src):
    if getattr(args, "seed", None) is not None:
        return args.seed
    if src.get("seed") is not None:
        return src["seed"]
    return random.SystemRandom().randrange(1, 1000000)


def cmd_plan(args):
    src = load_json_file(args.config or CONFIG_PATH)
    seed = _seed(args, src)
    cfg = effective_config(src, args.pilot)
    sectors, how = pick_sectors(src, args.pilot, seed)
    plan = build_plan(cfg, len(sectors))
    if args.json:
        print(json.dumps(dict(plan, seed=seed, mode=cfg["mode"], sectors=[s["id"] for s in sectors]), ensure_ascii=False, indent=1))
        return 0
    print_plan(plan, cfg, sectors, how, seed, "idea-arena, modo %s. Dry-run: no escribe nada ni llama a modelos ni a la red."
               % ("piloto" if args.pilot else "completo"))
    return 0


def cmd_init(args):
    if args.dry_run:
        return cmd_plan(args)
    src = load_json_file(args.config or CONFIG_PATH)
    seed = _seed(args, src)
    cfg = effective_config(src, args.pilot)
    sectors, how = pick_sectors(src, args.pilot, seed)
    plan = build_plan(cfg, len(sectors))
    over = over_limits(plan)
    if over:
        raise IdeaArenaError("el plan supera los topes de config.json: %s. Mirá %s"
                             % (", ".join("%s %d > %d" % (r["phase"], r["calls"], r["limit"]) for r in over), _cmd("plan")))
    strategies = load_strategies()
    personas = load_personas()
    missing = [p for p in cfg["tournament"]["persona_order"] if p not in personas]
    if missing:
        raise IdeaArenaError("tournament.persona_order nombra personas que no existen: %s" % ", ".join(missing))
    baseline = git_status_lines()
    d = new_run_dir()
    cfg["seed"] = seed
    copy_inputs(d, cfg, SCHEMAS)
    st = {"version": 1, "run": os.path.basename(d), "dir": d, "mode": cfg["mode"], "seed": seed, "created": now_iso(),
          "sectors": sectors, "sectors_how": how, "generators": assign_generators(strategies, sectors, cfg["generation"], seed),
          "steps": {}, "scope_batches": [], "candidates": [], "dedup_needed": False, "selected": [], "shortlist": [],
          "deepen": {}, "plan": {"calls": plan["calls"], "waves": plan["waves"], "tokens_k": plan["tokens_k"]},
          "git_baseline": baseline}
    save_state(d, st)
    write_text(LATEST, d + "\n")
    pending = sum(len(x[1]) for x in placeholder_report())
    print("run listo: %s (modo %s, semilla %s)" % (d, "piloto" if args.pilot else "completo", seed))
    print("sectores (%s): %s" % (how, ", ".join(s["id"] for s in sectors)))
    print("hasta %d llamadas a sub-agentes en unas %d oleadas de %d" % (plan["calls"], plan["waves"], cfg["wave"]))
    if pending:
        print("aviso: quedan %d placeholder(s) sin completar en constraints.md o calibration/ (%s)" % (pending, _cmd("doctor")))
    print("next: %s" % _cmd("next"))
    return 0


def describe(act):
    if act[0] == "phase":
        return "NEXT es la fase %s" % act[1]
    if act[0] == "step":
        return "NEXT es el paso %s" % act[1]
    if act[0] == "stuck":
        return "trabado en %s" % act[1]["id"]
    return "DONE"


def cmd_next(args):
    d, st, cfg = load_run(args)
    E.sweep_dashes(d)
    act = next_action(d, st)
    ts = load_tournament(d)
    head = "run %s (modo %s, semilla %s)" % (d, MODE_NAMES.get(st["mode"], st["mode"]), st["seed"])
    if ts and not ts["champion"] and B.current_round(ts):
        rd = B.current_round(ts)
        head += ", torneo ronda %d de %d, %d ideas vivas" % (rd["n"], len(B.bracket_sizes(ts["agents_n"])) - 1, len(rd["alive"]))
    print(head)
    if act[0] == "phase":
        _, name, left, jobs = act
        print("NEXT: %s. %d de %d trabajo(s) por correr." % (name, len(left), len(jobs)))
        print("  1. %s" % _cmd("prompts", name))
        print("  2. lanzá los trabajos que lista, una oleada de %d por vez" % cfg["wave"])
        print("  3. %s" % _cmd("next"))
    elif act[0] == "step":
        print("NEXT: step (%s): %s." % (act[1], act[2]))
        print("  %s" % _cmd("step"))
    elif act[0] == "stuck":
        job = act[1]
        print("STUCK: %s falló 3 veces (salidas en %s.invalido1..3)." % (job["id"], job["outputs"][0]))
        if job["phase"] == "judge":
            print("  decidí ese cruce a mano solo si el usuario lo pide: %s" % _cmd("record", job["match"], "<id ganador>", '--reason "..."'))
        return 1
    else:
        if st["mode"] == "calibration":
            print("DONE. Reporte: %s" % j(d, "calibration_report.md"))
        else:
            print("DONE. Shortlist: %s" % j(d, "shortlist.md"))
    return 0


def cmd_prompts(args):
    d, st, cfg = load_run(args)
    E.sweep_dashes(d)
    phase = args.phase
    jobs = phase_jobs(d, st, phase)
    if not jobs:
        print("nada para correr en %s ahora. %s" % (phase, _cmd("next")))
        return 0
    if phase not in TOURNAMENT_PHASES and len(jobs) > cfg["limits"][phase]:
        raise IdeaArenaError("%s tiene %d trabajos y el tope es %d (limits.%s en config.json)" % (phase, len(jobs), cfg["limits"][phase], phase))
    if load_fichas(d):
        write_all_fichas(d)
    ts = load_tournament(d)
    personas = load_personas(j(d, "inputs", "personas.json"))
    strategies = load_strategies(j(d, "inputs", "strategies.json"))
    left = missing_jobs(jobs)
    for job in jobs:
        if job in left or not os.path.isfile(job["prompt"]):
            write_text(job["prompt"], render_brief(d, st, cfg, job, ts, personas, strategies) + "\n")
    w = cfg["wave"]
    waves = [left[i:i + w] for i in range(0, len(left), w)]
    print("%s: %d trabajo(s), %d por correr, %d oleada(s) de hasta %d" % (phase, len(jobs), len(left), len(waves), w))
    for k, wave in enumerate(waves, start=1):
        print("oleada %d" % k)
        for job in wave:
            print("  %-34s %s" % (job["id"], ab(job["prompt"])))
    if left:
        model = (cfg.get("models") or {}).get(phase)
        print("")
        print("Cada trabajo es una llamada al Agent tool: subagent_type general-purpose, description \"idea-arena <id>\",")
        print("prompt \"Leé <ruta> y seguilo exactamente. Es tu brief completo.\"%s" % (", model \"%s\"" % model if model else ""))
        print("Una oleada es un solo mensaje con todas sus llamadas. Esperá que termine antes de la siguiente.")
    print("then: %s" % _cmd("next"))
    return 0


def cmd_check(args):
    d, st, cfg = load_run(args)
    jobs = phase_jobs(d, st, args.phase)
    left = missing_jobs(jobs)
    print("%s: %d de %d trabajo(s) hechos" % (args.phase, len(jobs) - len(left), len(jobs)))
    for job in left:
        print("  falta %-34s %s" % (job["id"], ", ".join(p for p in job["outputs"] if not has_output(p))))
    return 1 if left else 0


def cmd_palabras(args):
    """Schema, cost and page words of one idea, or of every idea in a generator's file, counted the
    way the hard filter counts them. For the agents that write ideas: they cannot see the filter."""
    d, st, cfg = load_run(args)
    data = parse_json_output(args.path) if os.path.isfile(args.path) else None
    if data is None:
        print("no es un JSON válido: %s" % args.path)
        return 1
    ideas = data["ideas"] if isinstance(data.get("ideas"), list) else [data]
    schema, cap, ok = S.load_schema("idea"), cfg["filter"]["idea_max_words"], True
    for k, idea in enumerate(ideas, start=1):
        body = E.sanitize_obj(S.idea_body(idea)) if isinstance(idea, dict) else idea
        name = (idea.get("local_id") or idea.get("titulo") or "idea %d" % k) if isinstance(idea, dict) else "idea %d" % k
        errs = S.validate(body, schema)
        if errs:
            ok = False
            print("MAL  %s: no sigue el esquema: %s" % (name, "; ".join(errs[:4])))
            continue
        _, words = S.render_page(body, {}, cfg)
        cost = [(c, m) for c, m in S.hard_check(body, {}, {}, cfg) if c in ("costo_tope", "costo_suma")]
        bad = words > cap or cost
        ok = ok and not bad
        print("%s %s: %d palabras (máximo %d)%s%s" % ("MAL " if bad else "OK  ", name, words, cap,
                                                      ": recortá %d" % (words - cap) if words > cap else "",
                                                      "".join("; %s" % m for _, m in cost)))
    return 0 if ok else 1


def cmd_step(args):
    d, st, cfg = load_run(args)
    E.sweep_dashes(d)
    act = next_action(d, st)
    if act[0] != "step":
        print("no hay un paso de Python pendiente: %s. %s" % (describe(act), _cmd("next")))
        return 0
    lines = STEPS[act[1]](d, st, cfg)
    save_state(d, st)
    print("paso %s" % act[1])
    for line in lines:
        print(line)
    print("then: %s" % _cmd("next"))
    return 0


def cmd_status(args):
    d, st, cfg = load_run(args)
    ts = load_tournament(d)
    info = {"run": d, "mode": st["mode"], "seed": st["seed"], "created": st["created"],
            "sectors": [s["id"] for s in st["sectors"]], "steps": st["steps"], "deepen": st.get("deepen")}
    if ts:
        rd = B.current_round(ts)
        info["tournament"] = {"ideas": ts["agents_n"], "round": rd["n"] if rd else None,
                              "alive": len(B.alive_ids(ts)), "champion": ts["champion"]}
    if args.json:
        print(json.dumps(info, ensure_ascii=False, indent=1))
        return 0
    print("run %s, modo %s, semilla %s, creado %s" % (d, MODE_NAMES.get(st["mode"], st["mode"]), st["seed"], st["created"]))
    if st["mode"] != "calibration":
        print("sectores: %s" % ", ".join(info["sectors"]))
    for name, summary in st["steps"].items():
        print("  %-18s %s" % (name, json.dumps(summary, ensure_ascii=False)[:150]))
    if ts:
        t = info["tournament"]
        print("torneo: %d ideas, %s" % (t["ideas"], "campeona %s" % t["champion"] if t["champion"]
                                        else "ronda %s, %d vivas" % (t["round"], t["alive"])))
    for iid, req in sorted((st.get("deepen") or {}).items()):
        print("profundizar %s: %s" % (iid, "listo" if req.get("collected") else "pendiente"))
    print("next: %s" % _cmd("next"))
    return 0


def cmd_record(args):
    d, st, cfg = load_run(args)
    ts = load_tournament(d)
    if not ts:
        raise IdeaArenaError("este run todavía no tiene torneo")
    m, previous = B.record(ts, args.match_id, args.idea_id, reason=args.reason, source="manual")
    m.setdefault("notes", []).append("decidido a mano")
    save_tournament(d, ts)
    print("%s: %s le gana a %s%s (a mano)" % (m["id"], m["winner"], m["loser"],
                                               " (antes %s)" % previous if previous and previous != m["winner"] else ""))
    return 0


def cmd_deepen(args):
    d, st, cfg = load_run(args)
    iid = args.idea_id.strip().lower()
    if not os.path.isfile(j(d, "ideas", iid + ".json")):
        raise IdeaArenaError("no existe la idea %s en %s" % (iid, j(d, "ideas")))
    aspects = list(cfg["deepen"]["aspects"])
    if len(aspects) > cfg["limits"]["deepen"]:
        raise IdeaArenaError("deepen pide %d llamadas y el tope es %d" % (len(aspects), cfg["limits"]["deepen"]))
    unknown = [a for a in aspects if not os.path.isfile(os.path.join(BRIEFS_DIR, "06_profundizar_%s.md" % a))]
    if unknown:
        raise IdeaArenaError("no hay brief para: %s" % ", ".join(unknown))
    st.setdefault("deepen", {})[iid] = {"aspects": aspects, "collected": False, "requested": now_iso()}
    save_state(d, st)
    print("profundización de %s en cola: %s (%d llamadas)" % (iid, ", ".join(aspects), len(aspects)))
    print("next: %s" % _cmd("next"))
    return 0


def placeholder_report(calibration_dir=None):
    """[(path, [(line number, text)])] for every <<COMPLETAR>> or <<REVISAR>> left."""
    cdir = calibration_dir or CALIBRATION_DIR
    files = [CONSTRAINTS_PATH, os.path.join(cdir, "my_ranking.md")]
    idir = os.path.join(cdir, "ideas")
    if os.path.isdir(idir):
        files += [os.path.join(idir, f) for f in sorted(os.listdir(idir)) if f.endswith(".md")]
    out = []
    for path in files:
        if not os.path.isfile(path):
            continue
        text = read_text(path)
        lines = text.splitlines()
        hits = []
        for m in PLACEHOLDER_RE.finditer(text):
            if text[m.start() - 1:m.start()] == "`":
                continue
            n = text.count("\n", 0, m.start()) + 1
            hits.append((n, lines[n - 1].strip() if "\n" not in m.group(0) else re.sub(r"\s+", " ", m.group(0))))
        if hits:
            out.append((path, hits))
    return out


def cmd_calibrate(args):
    cdir = os.path.abspath(args.calibration_dir or CALIBRATION_DIR)
    idir = os.path.join(cdir, "ideas")
    names = sorted(f[:-3] for f in os.listdir(idir) if f.endswith(".md")) if os.path.isdir(idir) else []
    if len(names) < 2:
        raise IdeaArenaError("hacen falta al menos 2 ideas en %s" % idir)
    pend = [(p, h) for p, h in placeholder_report(cdir) if os.path.abspath(p).startswith(cdir)]
    if pend:
        raise IdeaArenaError("la calibración tiene placeholders sin completar:\n%s" % "\n".join(
            "  %s:%d %s" % (os.path.relpath(p, ROOT), n, _clip(t, 80)) for p, hits in pend for n, t in hits))
    ranking = parse_ranking(read_text(os.path.join(cdir, "my_ranking.md")), names)
    src = load_json_file(args.config or CONFIG_PATH)
    cfg = effective_config(src, False)
    pairs = list(itertools.combinations(names, 2))
    calls = 2 * len(pairs)
    if args.dry_run:
        print("calibración: %d ideas, %d pares, %d llamadas al juez (los dos órdenes de cada par). Tope %d."
              % (len(names), len(pairs), calls, cfg["limits"]["calibrate"]))
        return 0
    if calls > cfg["limits"]["calibrate"]:
        raise IdeaArenaError("la calibración pide %d llamadas y el tope es %d (limits.calibrate)" % (calls, cfg["limits"]["calibrate"]))
    seed = _seed(args, src)
    baseline = git_status_lines()
    d = new_run_dir()
    cfg["seed"], cfg["mode"] = seed, "calibration"
    copy_inputs(d, cfg, ("veredicto",))
    for name in names:   # without the HTML comments meant for you, which the judge does not need
        write_text(j(d, "calibration", "ideas", name + ".md"),
                   re.sub(r"<!--.*?-->\s*", "", read_text(os.path.join(idir, name + ".md")), flags=re.S))
    write_text(j(d, "calibration", "my_ranking.md"), read_text(os.path.join(cdir, "my_ranking.md")))
    jobs = []
    for a, b in pairs:
        for x, y in ((a, b), (b, a)):
            jobs.append({"id": "calibracion.%s__%s" % (x, y), "x": x, "y": y, "pair": "%s contra %s" % (x, y),
                         "outputs": [j(d, "calibration", "veredictos", "%s__%s.json" % (x, y))]})
    st = {"version": 1, "run": os.path.basename(d), "dir": d, "mode": "calibration", "seed": seed, "created": now_iso(),
          "sectors": [], "steps": {}, "deepen": {}, "git_baseline": baseline,
          "calibration": {"ideas": names, "ranking": ranking, "jobs": jobs}}
    save_state(d, st)
    write_text(LATEST, d + "\n")
    print("calibración lista: %s. %d ideas, %d llamadas al juez." % (d, len(names), calls))
    print("next: %s" % _cmd("next"))
    return 0


def _weights_table(path):
    with open(path, encoding="utf-8") as fh:
        return [(k, int(w)) for k, w in re.findall(r"^\| (\w+) \| (\d+) \|", fh.read(), re.M)]


def cmd_doctor(args):
    problems, notes = [], []
    pend = placeholder_report(args.calibration_dir)
    try:
        src = load_json_file(args.config or CONFIG_PATH)
    except (OSError, ValueError) as e:
        print("config.json no se puede leer: %s" % e)
        return 1
    for path in (CONSTRAINTS_PATH, RUBRIC_PATH, CONFIG_PATH, STRATEGIES_PATH, PERSONAS_PATH):
        text = read_text(path)
        if E.EM_DASH in text or E.EN_DASH in text:
            problems.append("%s tiene rayas largas o semirrayas: el test del repo falla" % os.path.relpath(path, ROOT))
    for path, _ in pend:
        text = read_text(path)
        if E.EM_DASH in text or E.EN_DASH in text:
            problems.append("%s tiene rayas largas o semirrayas" % os.path.relpath(path, ROOT))
    code = list(T.CRITERIA)
    if _weights_table(RUBRIC_PATH) != code:
        problems.append("los pesos de rubric.md no coinciden con CRITERIA en ia_tournament.py")
    if _weights_table(CONSTRAINTS_PATH) != code:
        problems.append("los pesos de constraints.md no coinciden con CRITERIA en ia_tournament.py")
    ids = [s["id"] for s in src["sectors"]]
    if len(set(ids)) != len(ids) or not all(re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", x) for x in ids):
        problems.append("los ids de sectores tienen que ser únicos, en minúscula y con guiones")
    personas = load_personas()
    for mode in (False, True):
        cfg = effective_config(src, mode)
        miss = [p for p in cfg["tournament"]["persona_order"] if p not in personas]
        if miss:
            problems.append("persona_order (%s) nombra personas inexistentes: %s" % (cfg["mode"], ", ".join(miss)))
        over = over_limits(build_plan(cfg, len(pick_sectors(src, mode, 1)[0])))
        if over:
            problems.append("el modo %s supera los topes: %s" % (cfg["mode"], ", ".join(r["phase"] for r in over)))
    try:
        load_strategies()
    except IdeaArenaError as e:
        problems.append(str(e))
    confirmed, pending = hard_restrictions(read_text(CONSTRAINTS_PATH))
    notes.append("restricciones duras confirmadas: %s" % (", ".join(confirmed) or "ninguna"))
    if pending:
        notes.append("restricciones [A CONFIRMAR] (el juez las trata como blandas): %s" % ", ".join(pending))
    print("idea-arena doctor")
    for n in notes:
        print("  %s" % n)
    if pend:
        print("placeholders por completar (%d):" % sum(len(h) for _, h in pend))
        for path, hits in pend:
            print("  %s" % _slash(os.path.relpath(path, ROOT)))
            for n, t in hits:
                print("    línea %d: %s" % (n, _clip(t, 100)))
    else:
        print("sin placeholders pendientes")
    if problems:
        print("problemas:")
        for p in problems:
            print("  %s" % p)
        return 1
    print("configuración consistente")
    return 0


def cmd_audit(args):
    d, st, cfg = load_run(args)
    now = git_status_lines()
    if now is None:
        print("git no está disponible acá: no puedo auditar")
        return 1
    base = set(st.get("git_baseline") or [])
    outside = [line for line in now if not _status_path(line).startswith("runs/") and line not in base]
    E.sweep_dashes(d)
    if outside:
        print("ATENCIÓN: cambios fuera de runs/ desde que empezó %s:" % d)
        for line in outside:
            print("  %s" % line)
        return 1
    print("ok: desde que empezó %s no cambió nada fuera de runs/ (según git status)" % d)
    return 0


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--run", help="la carpeta del run (por defecto la de runs/LATEST)")
    p = argparse.ArgumentParser(prog="idea_arena.py", description="El pipeline de /idea-arena.")
    sub = p.add_subparsers(dest="cmd")
    sub.required = True

    for name, fn, hlp in (("plan", cmd_plan, "dry-run: fases, llamadas y topes, sin escribir nada"),
                          ("init", cmd_init, "crear un run en runs/<YYYYMMDD-HHMM>")):
        s = sub.add_parser(name, help=hlp)
        s.add_argument("--pilot", action="store_true", help="3 sectores, unas 10 ideas, bracket de 8")
        s.add_argument("--seed", type=int)
        s.add_argument("--config", help="otro config.json (por defecto el del skill)")
        s.add_argument("--json", action="store_true")
        if name == "init":
            s.add_argument("--dry-run", action="store_true", help="solo imprimir el plan")
        s.set_defaults(func=fn, dry_run=False)

    s = sub.add_parser("next", parents=[common], help="qué hacer ahora")
    s.set_defaults(func=cmd_next)
    for name, fn, hlp in (("prompts", cmd_prompts, "escribir los briefs de una fase y listar los trabajos"),
                          ("check", cmd_check, "listar los trabajos sin salida")):
        s = sub.add_parser(name, parents=[common], help=hlp)
        s.add_argument("phase", choices=AGENT_PHASES)
        s.set_defaults(func=fn)
    s = sub.add_parser("step", parents=[common], help="correr el paso de Python pendiente")
    s.set_defaults(func=cmd_step)
    s = sub.add_parser("palabras", parents=[common], help="esquema, costo y palabras de una idea, como los cuenta el filtro")
    s.add_argument("path", help="el JSON de una idea, o el archivo de un generador")
    s.set_defaults(func=cmd_palabras)
    s = sub.add_parser("status", parents=[common], help="estado del run")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_status)
    s = sub.add_parser("record", parents=[common], help="decidir un cruce a mano")
    s.add_argument("match_id")
    s.add_argument("idea_id")
    s.add_argument("--reason")
    s.set_defaults(func=cmd_record)
    s = sub.add_parser("deepen", parents=[common], help="profundizar una idea")
    s.add_argument("idea_id")
    s.set_defaults(func=cmd_deepen)
    s = sub.add_parser("calibrate", help="crear un run de calibración del juez")
    s.add_argument("--calibration-dir")
    s.add_argument("--config")
    s.add_argument("--seed", type=int)
    s.add_argument("--dry-run", action="store_true")
    s.set_defaults(func=cmd_calibrate)
    s = sub.add_parser("doctor", help="placeholders pendientes y chequeos de consistencia")
    s.add_argument("--config")
    s.add_argument("--calibration-dir")
    s.set_defaults(func=cmd_doctor)
    s = sub.add_parser("audit", parents=[common], help="cambios fuera de runs/ desde el init")
    s.set_defaults(func=cmd_audit)
    return p


def main(argv=None):
    global _RUN_SUFFIX
    for stream in (sys.stdout, sys.stderr):
        try:
            # UTF-8 so accents survive a Windows pipe, and agents' titles can hold any character
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    args = build_parser().parse_args(argv)
    os.chdir(ROOT)
    if getattr(args, "run", None):
        _RUN_SUFFIX = " --run %s" % rel(args.run)
    try:
        return args.func(args)
    except (IdeaArenaError, T.ArenaError) as e:
        print("error: %s" % e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
