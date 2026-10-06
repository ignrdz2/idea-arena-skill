"""ia_tournament.py: the idea tournament, built on /arena's bracket.

The single-elimination mechanics (pairing, byes, eliminating the losers, carrying the
revised version into the next match, crowning) come from skills/arena/bracket.py,
imported read-only. This module adds what an idea tournament needs on top:

- personas: every match has one attacking persona, the same for both ideas, and the
  persona changes every round, so an idea that plays r rounds faces min(r, P) of them;
- presentation order: the judge sees "Idea X" and "Idea Y", never the ids. X is the
  idea that has been shown first fewer times; on a tie it alternates match by match;
- decide(): six criteria with the rubric's weights, and the fatal rule: an idea with a
  verified fatal flaw cannot beat one without. Fatal comes from the judge (only with a
  valid category) or from Python's hard check of the revised idea.

Python 3.8+, standard library only.
"""
import importlib.util
import math
import os
import re
import sys

sys.dont_write_bytecode = True   # never leave __pycache__ inside skills/arena

HERE = os.path.dirname(os.path.abspath(__file__))
ARENA_BRACKET = os.path.join(os.path.dirname(HERE), "arena", "bracket.py")


def _load_bracket():
    if not os.path.isfile(ARENA_BRACKET):
        raise ImportError("idea-arena needs /arena's bracket.py at %s. Keep skills/arena next to "
                          "skills/idea-arena." % ARENA_BRACKET)
    spec = importlib.util.spec_from_file_location("arena_bracket", ARENA_BRACKET)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


B = _load_bracket()
ArenaError = B.ArenaError

# Mirrors the tables in rubric.md and constraints.md. tests/test_idea_arena.py checks they agree.
CRITERIA = (
    ("demanda", 25),
    ("viabilidad", 25),
    ("diferenciacion", 20),
    ("business_case", 15),
    ("encaje", 10),
    ("academico", 5),
)
TIE_ORDER = ("demanda", "viabilidad")
SOLUTION_SUFFIX = ".solution.md"


# ---------------------------------------------------------------- verdicts

def _num(v):
    if isinstance(v, bool):
        return None
    try:
        return max(0.0, min(10.0, float(v)))
    except (TypeError, ValueError):
        return None


def weighted_total(scores):
    """0 to 100 from six 0 to 10 scores. None if any is missing."""
    if not isinstance(scores, dict):
        return None
    total = 0.0
    for key, weight in CRITERIA:
        v = _num(scores.get(key))
        if v is None:
            return None
        total += v * weight
    return round(total / 10.0, 2)


def truthy(v):
    if isinstance(v, str):
        return v.strip().lower() in ("true", "yes", "si", "sí", "1")
    return bool(v)


_HARD_RE = re.compile(r"^\s*restricci[oó]n_dura\s*:\s*(R\d+)\b", re.I)
_CLAIM_RE = re.compile(r"^\s*afirmaci[oó]n_sin_evidencia\s*:\s*(.+)", re.I | re.S)


def valid_fatal_reason(reason, hard_ids=None):
    """A fatal flaw counts only as a confirmed hard restriction or an unsupported claim, quoted."""
    if not isinstance(reason, str):
        return False
    m = _HARD_RE.match(reason)
    if m:
        return hard_ids is None or m.group(1).upper() in hard_ids
    m = _CLAIM_RE.match(reason)
    return bool(m) and len(m.group(1).strip()) >= 8


def normalize_verdict(v, x_id, y_id):
    """A judge's X/Y verdict, re-keyed by idea id."""
    if not isinstance(v, dict):
        raise ArenaError("el veredicto no es un objeto JSON")
    label = {"X": x_id, "Y": y_id}
    raw = v.get("scores") if isinstance(v.get("scores"), dict) else {}
    scores = {}
    for k, s in raw.items():
        iid = label.get(str(k).strip().upper())
        if iid and isinstance(s, dict):
            d = {key: s.get(key) for key, _ in CRITERIA}
            d["fatal_claims"] = [(truthy(s.get("fatal")), str(s.get("fatal_motivo") or ""))]
            scores[iid] = d
    pick = str(v.get("winner") or "").strip().upper()
    hx, hy = re.search(r"\bX\b", pick) is not None, re.search(r"\bY\b", pick) is not None
    st = v.get("standing") if isinstance(v.get("standing"), dict) else {}
    standing = {label[str(k).strip().upper()]: [str(x) for x in val] for k, val in st.items()
                if str(k).strip().upper() in label and isinstance(val, list)}
    survived = [str(x) for x in v.get("survived")] if isinstance(v.get("survived"), list) else []
    return {"scores": scores, "pick": x_id if hx and not hy else y_id if hy and not hx else None,
            "standing": standing, "survived": survived[:10], "reasons": [str(v.get("reason") or "")[:400]]}


def merge_verdicts(nvs, a, b):
    """Merge the verdicts of one match judged in both orders: mean scores, every fatal claim,
    every standing attack. The judge's pick survives only if both judges agree."""
    if len(nvs) == 1:
        return nvs[0]
    scores = {}
    for iid in (a, b):
        per = [nv["scores"].get(iid) for nv in nvs if nv["scores"].get(iid)]
        if not per:
            continue
        d = {}
        for key, _ in CRITERIA:
            vals = [_num(p.get(key)) for p in per if _num(p.get(key)) is not None]
            d[key] = round(sum(vals) / len(vals), 2) if vals else None
        d["fatal_claims"] = [c for p in per for c in p["fatal_claims"]]
        scores[iid] = d
    picks = set(nv["pick"] for nv in nvs)
    standing = {}
    for nv in nvs:
        for iid, lst in nv["standing"].items():
            standing.setdefault(iid, [])
            standing[iid] += [x for x in lst if x not in standing[iid]]
    survived = []
    for nv in nvs:
        survived += [x for x in nv["survived"] if x not in survived]
    return {"scores": scores, "pick": picks.pop() if len(picks) == 1 else None, "standing": standing,
            "survived": survived[:10], "reasons": [r for nv in nvs for r in nv["reasons"]]}


def decide(nv, a, b, hard_ids=None, det_fatal=None):
    """Apply the rubric's arithmetic to a normalized verdict.

    An idea with a verified fatal flaw cannot beat one without. Otherwise the higher
    weighted total wins. On an exact tie: fewer standing attacks, then higher demand
    evidence, then higher feasibility, then the judge's own pick.
    Returns (winner, {id: total}, {id: fatal}, [notes])."""
    det_fatal = det_fatal or {}
    notes = []
    sa, sb = nv["scores"].get(a), nv["scores"].get(b)
    totals = {a: weighted_total(sa), b: weighted_total(sb)}
    fatal = {}
    for iid, s in ((a, sa), (b, sb)):
        judged = False
        for claimed, motivo in (s or {}).get("fatal_claims", []):
            if not claimed:
                continue
            if valid_fatal_reason(motivo, hard_ids):
                judged = True
            else:
                notes.append("fatal de %s ignorado: el motivo no es una categoría válida (%s)" % (iid, motivo or "vacío"))
        det = list(det_fatal.get(iid) or [])
        if det:
            notes.append("fatal determinístico de %s: %s" % (iid, ", ".join(det)))
        fatal[iid] = judged or bool(det)
    ta, tb = totals[a], totals[b]
    if fatal[a] != fatal[b]:
        winner = b if fatal[a] else a
        loser = a if winner == b else b
        if totals[loser] is not None and totals[winner] is not None and totals[loser] > totals[winner]:
            notes.append("%s sumó más puntos pero tiene un fallo fatal" % loser)
    elif ta is None or tb is None:
        if not nv["pick"]:
            raise ArenaError("el veredicto no tiene puntajes completos ni un ganador claro")
        winner = nv["pick"]
        notes.append("puntajes incompletos: se usó la elección del juez")
    elif ta != tb:
        winner = a if ta > tb else b
    else:
        st = nv["standing"]
        na = len(st[a]) if a in st else None
        nb = len(st[b]) if b in st else None
        winner = None
        if na is not None and nb is not None and na != nb:
            winner = a if na < nb else b
        else:
            for key in TIE_ORDER:
                ca, cb = _num(sa.get(key)), _num(sb.get(key))
                if ca != cb:
                    winner = a if ca > cb else b
                    break
        if winner is None:
            if not nv["pick"]:
                raise ArenaError("empate exacto y el juez no eligió ganador")
            winner = nv["pick"]
    if nv["pick"] and nv["pick"] != winner:
        notes.append("el juez eligió %s pero las reglas dan %s: mandan las reglas" % (nv["pick"], winner))
    return winner, totals, fatal, notes


# ---------------------------------------------------------------- the bracket

def new_tournament(ideas, seed, tdir, persona_order, personas_per_match=1, both_orders=False):
    """ideas: [(id, primary sector, page path, json path)]. Pairs round 1 through bracket.py.
    The sector goes where /arena keeps the reasoning mode, so pairing prefers to cross sectors."""
    agents = {}
    for iid, sector, page, ij in ideas:
        agents[iid] = {"card": {"reasoning": {"id": sector, "name": sector}},
                       "solution": page, "idea_json": ij, "alive": True,
                       "eliminated_in": None, "eliminated_by": None, "byes": 0,
                       "shown_first": 0, "shown_second": 0, "personas": []}
    state = {"version": 1, "seed": seed, "dir": tdir, "has_baseline": False, "final": None,
             "agents": agents, "agents_n": len(agents), "rounds": [], "champion": None,
             "persona_order": list(persona_order), "personas_per_match": max(1, int(personas_per_match)),
             "judge_both_orders": bool(both_orders)}
    rd = B.open_round(state, sorted(agents))
    if rd:
        annotate_round(state, rd)
    return state


def round_personas(state, n):
    order = state["persona_order"]
    k = min(state["personas_per_match"], len(order))
    start = ((n - 1) * k) % len(order)
    return [order[(start + j) % len(order)] for j in range(k)]


def annotate_round(state, rd):
    """Give every match of a freshly opened round its personas and its presentation order."""
    agents = state["agents"]
    personas = round_personas(state, rd["n"])
    for idx, m in enumerate(rd["matches"]):
        a, b = m["a"], m["b"]
        ba = agents[a]["shown_first"] - agents[a]["shown_second"]
        bb = agents[b]["shown_first"] - agents[b]["shown_second"]
        if ba != bb:
            first = a if ba < bb else b
        else:
            first = a if idx % 2 == 0 else b
        second = b if first == a else a
        m["first"], m["second"] = first, second
        agents[first]["shown_first"] += 1
        agents[second]["shown_second"] += 1
        m["personas"] = list(personas)
        for iid in (a, b):
            agents[iid]["personas"].extend(personas)
    return rd


def advance_round(state):
    """bracket.py's advance, then point every idea at its latest JSON and annotate the new round."""
    survivors = B.advance(state)
    for ag in state["agents"].values():
        ag["solution"] = ag["solution"].replace("\\", "/")
        if ag["solution"].endswith(SOLUTION_SUFFIX):
            ag["idea_json"] = ag["solution"][:-len(SOLUTION_SUFFIX)] + ".idea.json"
    rd = B.current_round(state)
    if rd:
        annotate_round(state, rd)
    return survivors


def _p(*parts):
    return os.path.join(*parts).replace("\\", "/")


def rdir(state, n):
    return _p(state["dir"], "r%d" % n)


def attack_json(state, n, mid, iid, persona):
    return _p(rdir(state, n), "%s.%s.ataque.%s.json" % (mid, iid, persona))


def attacks_md(state, n, mid, iid):
    return _p(rdir(state, n), "%s.%s.ataques.md" % (mid, iid))


def defense_json(state, n, mid, iid):
    return _p(rdir(state, n), "%s.%s.defensa.json" % (mid, iid))


def defense_md(state, n, mid, iid):
    return _p(rdir(state, n), "%s.%s.defensa.md" % (mid, iid))


def revised_json(state, n, mid, iid):
    return _p(rdir(state, n), "%s.%s.idea.json" % (mid, iid))


def solution_md(state, n, mid, iid):
    """Exactly where bracket.py's advance looks for a revised solution."""
    return B.revised_out(state["dir"], n, mid, iid).replace("\\", "/")


def verdict_json(state, n, mid, swapped=False):
    return _p(rdir(state, n), "%s.veredicto%s.json" % (mid, ".invertido" if swapped else ""))


def tournament_jobs(state, phase):
    """Every sub-agent job of the open round for attack, defend or judge. Decided matches are skipped."""
    rd = B.current_round(state)
    if rd is None:
        return []
    n, jobs = rd["n"], []
    for m in rd["matches"]:
        if m["winner"]:
            continue
        mid, pair = m["id"], (m["first"], m["second"])
        if phase == "attack":
            for iid in pair:
                for p in m["personas"]:
                    jobs.append({"id": "%s.%s.ataque.%s" % (mid, iid, p), "kind": "attack", "round": n,
                                 "match": mid, "idea": iid, "persona": p,
                                 "outputs": [attack_json(state, n, mid, iid, p)]})
        elif phase == "defend":
            for iid in pair:
                jobs.append({"id": "%s.%s.defensa" % (mid, iid), "kind": "defend", "round": n,
                             "match": mid, "idea": iid,
                             "outputs": [defense_json(state, n, mid, iid), revised_json(state, n, mid, iid)]})
        elif phase == "judge":
            jobs.append({"id": "%s.juez" % mid, "kind": "judge", "round": n, "match": mid,
                         "x": m["first"], "y": m["second"], "outputs": [verdict_json(state, n, mid)]})
            if state["judge_both_orders"]:
                jobs.append({"id": "%s.juez-invertido" % mid, "kind": "judge", "round": n, "match": mid,
                             "x": m["second"], "y": m["first"], "outputs": [verdict_json(state, n, mid, True)]})
    return jobs


def calls_per_match(personas_per_match=1, both_orders=False):
    return 2 * personas_per_match + 2 + (2 if both_orders else 1)


def tournament_plan(n, personas_per_match=1, both_orders=False, wave=10):
    """Per round: alive, matches, bye, calls and waves. With one persona and one judge it is
    exactly /arena's round plan."""
    k, j = personas_per_match, 2 if both_orders else 1
    rows = []
    for rnd, alive in enumerate(B.bracket_sizes(n)[:-1], start=1):
        m = alive // 2
        waves = math.ceil(2 * k * m / wave) + math.ceil(2 * m / wave) + math.ceil(j * m / wave)
        rows.append({"round": rnd, "alive": alive, "matches": m, "bye": alive % 2,
                     "calls": m * calls_per_match(k, both_orders), "waves": waves})
    return rows


def ranking(state):
    """Every idea, best first: the champion, then by the round it fell in (later is better).
    Within a round, an idea whose last match ended with a verified fatal flaw goes below the
    rest, then the total it scored in the match it lost decides."""
    last = {}
    for rd in state["rounds"]:
        for m in rd["matches"]:
            for iid in (m["a"], m["b"]):
                last[iid] = m
    rows = []
    for iid, ag in state["agents"].items():
        m = last.get(iid) or {}
        lost_score = (m.get("scores") or {}).get(iid) if ag["eliminated_in"] else None
        reached = len(state["rounds"]) + 1 if iid == state["champion"] else (ag["eliminated_in"] or 0)
        rows.append({"id": iid, "champion": iid == state["champion"], "reached_round": reached,
                     "eliminated_in": ag["eliminated_in"], "eliminated_by": ag["eliminated_by"],
                     "lost_score": lost_score, "fatal": bool((m.get("fatal") or {}).get(iid))})
    rows.sort(key=lambda r: (-r["reached_round"], r["fatal"],
                             -(r["lost_score"] if r["lost_score"] is not None else -1), r["id"]))
    for i, r in enumerate(rows, start=1):
        r["rank"] = i
    return rows


def trail(state, iid):
    """Every match an idea played, in order, with what the judges said."""
    rows = []
    for rd in state["rounds"]:
        if rd["bye"] == iid:
            rows.append({"round": rd["n"], "bye": True})
        for m in rd["matches"]:
            if iid not in (m["a"], m["b"]):
                continue
            opp = m["b"] if m["a"] == iid else m["a"]
            sc = m.get("scores") or {}
            rows.append({"round": rd["n"], "bye": False, "match": m["id"], "opponent": opp,
                         "personas": m.get("personas", []), "score": sc.get(iid), "opponent_score": sc.get(opp),
                         "won": m["winner"] == iid if m["winner"] else None, "reason": m.get("reason"),
                         "fatal": (m.get("fatal") or {}).get(iid), "standing": (m.get("standing") or {}).get(iid, []),
                         "survived": m.get("survived") if m["winner"] == iid else [], "notes": m.get("notes", [])})
    return rows
