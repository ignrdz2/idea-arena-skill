"""Tests for skills/idea-arena. Standard library only.

    python -m unittest discover -s tests -v

The headline test drives a whole pilot through the real command line, with fake
sub-agents and canned URL results, in a temporary root, and checks that every file
the pipeline wrote is under runs/ and that nothing in skills/ changed.
"""
import hashlib
import http.server
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest

sys.dont_write_bytecode = True   # keep __pycache__ out of skills/idea-arena

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SKILL = os.path.join(REPO, "skills", "idea-arena")
TOOL = os.path.join(SKILL, "idea_arena.py")
sys.path.insert(0, SKILL)

import ia_evidence as E  # noqa: E402
import ia_schema as S  # noqa: E402
import ia_tournament as T  # noqa: E402
import idea_arena as IA  # noqa: E402

B = T.B
EM_DASH, EN_DASH = chr(0x2014), chr(0x2013)   # spelled as code points so this file stays clean
CFG = IA.effective_config(IA.load_json_file(IA.CONFIG_PATH), False)
PAGE = "<html><body><p>Dato verificable: el 30% de las pymes pierde horas por semana.</p></body></html>"


def ficha(fid, sector="agro", geo="UY", url=None, estado=None, **kw):
    f = {"id": fid, "sector": sector, "hallazgo": "Un hallazgo concreto: el 30% de las pymes pierde 5 horas por semana.",
         "source_url": url or "https://ejemplo.uy/%s" % fid, "source_title": "Una nota", "source_date": "2025-05",
         "source_type": "prensa", "geografia": geo, "confianza": "media", "retrieved_at": "2026-10-02T10:00:00"}
    if estado:
        f["verificacion"] = {"estado": estado}
    f.update(kw)
    return f


def idea(evid=("F-agro-001", "F-agro-002"), total=120, items=None, comps=None, **kw):
    items = items if items is not None else [{"concepto": "Servidor", "usd_anual": total, "supuesto": "una instancia chica todo el año",
                                              "fuente_precio_url": "https://precios.ejemplo.com/vm"}]
    d = {"titulo": "Idea de prueba", "problema": "Un problema concreto que les cuesta horas a los productores (F-agro-001).",
         "usuario": "Productores medianos", "solucion": "Un sistema que registra los datos del campo y avisa a tiempo.",
         "mvp": {"semestre_1": ["Registro"], "semestre_2": ["Alertas"]}, "stack": ["Python", "PostgreSQL"],
         "costo_infra": {"total_anual_usd": total, "items": items},
         "competidores": comps if comps is not None else [{"nombre": "Comp", "evidencia_ids": ["F-agro-002"], "hueco": "caro para pymes"}],
         "monetizacion": "Suscripción mensual de 20 dólares por productor.", "riesgos": ["Adopción lenta"],
         "supuestos": ["Pagarían 20 dólares por mes"], "evidencias": list(evid)}
    d.update(kw)
    return d


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def write_json(path, obj):
    write(path, json.dumps(obj, ensure_ascii=False, indent=1))


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def snapshot(top):
    out = {}
    for root, dirs, files in os.walk(top):
        dirs[:] = [x for x in dirs if x not in ("__pycache__", ".git")]
        for name in files:
            path = os.path.join(root, name)
            with open(path, "rb") as fh:
                out[os.path.relpath(path, top)] = hashlib.sha1(fh.read()).hexdigest()
    return out


def sc(v, fatal=False, motivo="", **over):
    d = {k: v for k, _ in T.CRITERIA}
    d.update(over)
    d.update(fatal=fatal, fatal_motivo=motivo)
    return d


# ---------------------------------------------------------------- formats

class Schemas(unittest.TestCase):
    def errors(self, value, name):
        return S.validate(value, S.load_schema(name))

    def test_every_schema_file_loads(self):
        for name in IA.SCHEMAS:
            self.assertIsInstance(S.load_schema(name), dict)

    def test_valid_ficha_and_idea_pass(self):
        self.assertEqual(self.errors(ficha("F-agro-001"), "ficha"), [])
        self.assertEqual(self.errors(ficha("F-agro-001", extracto="una frase", competidor="X"), "ficha"), [])
        self.assertEqual(self.errors(S.idea_body(dict(idea(), id="i001", local_id="g01-1")), "idea"), [])

    def test_bad_fichas_fail(self):
        f = ficha("F-agro-001")
        del f["hallazgo"]
        self.assertTrue(any("hallazgo" in e for e in self.errors(f, "ficha")))
        for bad in ({"source_type": "blog"}, {"source_url": "ftp://x.uy/a"}, {"source_date": "mayo 2025"},
                    {"geografia": "Uruguay"}, {"confianza": "total"}, {"id": "agro-1"}, {"retrieved_at": "ayer"},
                    {"hallazgo": "corto"}, {"inventado": True}):
            self.assertTrue(self.errors(ficha("F-agro-001", **bad), "ficha"), "should fail: %s" % bad)

    def test_bad_ideas_fail(self):
        i = idea()
        del i["mvp"]["semestre_2"]
        self.assertTrue(self.errors(i, "idea"))
        self.assertTrue(self.errors(idea(total=-1), "idea"))
        self.assertTrue(self.errors(idea(comps=[{"nombre": "X", "evidencia_ids": [], "hueco": "ninguno"}]), "idea"))
        self.assertTrue(self.errors(idea(meta={"estrategia": "dolor"}), "idea"))
        self.assertTrue(self.errors(idea(evid=()), "idea"))


# ---------------------------------------------------------------- the hard filter

class HardFilter(unittest.TestCase):
    def setUp(self):
        self.fichas = {
            "F-agro-001": ficha("F-agro-001", estado="ok"), "F-agro-002": ficha("F-agro-002", estado="ok"),
            "F-agro-003": ficha("F-agro-003", estado="bloqueada"), "F-agro-004": ficha("F-agro-004", estado="bloqueada"),
            "F-us-001": ficha("F-us-001", geo="US", estado="ok"), "F-us-002": ficha("F-us-002", geo="US", estado="ok"),
        }
        self.prices = {"https://precios.ejemplo.com/vm": {"estado": "ok"}, "https://muerta.ejemplo.com/p": {"estado": "muerta"}}

    def codes(self, i, words=None):
        return [c for c, _ in S.hard_check(i, self.fichas, self.prices, CFG, page_words=words)]

    def test_a_good_idea_passes(self):
        self.assertEqual(self.codes(idea(), words=500), [])

    def test_cost_over_the_cap(self):
        self.assertIn("costo_tope", self.codes(idea(total=301)))
        self.assertEqual(self.codes(idea(total=300)), [], "the cap itself is allowed")

    def test_cost_items_must_add_up(self):
        items = [{"concepto": "VM", "usd_anual": 150, "supuesto": "una instancia", "fuente_precio_url": "https://precios.ejemplo.com/vm"}]
        self.assertIn("costo_suma", self.codes(idea(total=100, items=items)))

    def test_a_price_without_a_verified_source_is_an_estimate_that_does_not_drop_the_idea(self):
        def item(**kw):
            return dict({"concepto": "API de un modelo", "usd_anual": 100, "supuesto": "estimado por encima, sin página de precios"}, **kw)
        for it in (item(fuente_precio_url="https://muerta.ejemplo.com/p"), item(fuente_precio_url="https://nueva.ejemplo.com/p"),
                   item(), item(fuente_precio_url=""), item(fuente_precio_url=None)):
            problems = S.hard_check(idea(total=100, items=[it]), self.fichas, self.prices, CFG, page_words=500)
            self.assertEqual([c for c, _ in problems], ["costo_estimado"], it)
            self.assertEqual(S.blocking(problems), [], it)
            self.assertEqual(S.fatal_codes(problems), [], "an estimate is never fatal")
        no_source = idea(total=100, items=[item(fuente_precio_url="")])
        self.assertEqual(S.validate(S.idea_body(no_source), S.load_schema("idea")), [], "an empty source is dropped, not a schema error")
        page, _ = S.render_page(dict(no_source, id="i001"), self.fichas, CFG, S.hard_check(no_source, self.fichas, self.prices, CFG))
        self.assertIn("| estimación |", page)
        self.assertIn("Aviso (costo_estimado)", page)
        self.assertIn("Sin problemas", page)
        over = idea(total=301, items=[item(usd_anual=301)])
        self.assertEqual([c for c, _ in S.blocking(S.hard_check(over, self.fichas, self.prices, CFG))], ["costo_tope"],
                         "an estimate still counts against the cap")

    def test_evidence_ids_must_exist(self):
        self.assertIn("evidencia_inexistente", self.codes(idea(evid=("F-agro-001", "F-agro-999"))))
        self.assertIn("evidencia_inexistente", self.codes(idea(comps=[{"nombre": "X", "evidencia_ids": ["F-x-001"], "hueco": "caro para pymes"}])))

    def test_minimum_local_and_verified_evidence(self):
        self.assertIn("evidencia_minima", self.codes(idea(evid=("F-agro-001",), comps=[])))
        self.assertIn("evidencia_local", self.codes(idea(evid=("F-us-001", "F-us-002"), comps=[])))
        only_blocked = idea(evid=("F-agro-003", "F-agro-004"), comps=[{"nombre": "X", "evidencia_ids": ["F-agro-003"], "hueco": "caro para pymes"}])
        self.assertIn("evidencia_solo_bloqueada", self.codes(only_blocked))
        self.assertNotIn("evidencia_solo_bloqueada", self.codes(idea(evid=("F-agro-001", "F-agro-003"))))

    def test_competitors_need_a_card_and_the_page_has_a_word_limit(self):
        self.assertIn("competidor_sin_ficha", self.codes(idea(evid=("F-agro-001", "F-agro-002", "F-x-1"),
                                                              comps=[{"nombre": "X", "evidencia_ids": ["F-x-1"], "hueco": "caro para pymes"}])))
        self.assertIn("palabras", self.codes(idea(), words=CFG["filter"]["idea_max_words"] + 1))

    def test_schema_breaks_stop_the_check(self):
        broken = idea()
        del broken["usuario"]
        self.assertEqual(set(self.codes(broken)), {"esquema"})

    def test_which_failures_are_fatal(self):
        problems = [("costo_tope", ""), ("palabras", ""), ("evidencia_inexistente", "")]
        self.assertEqual(S.fatal_codes(problems), ["costo_tope", "evidencia_inexistente"])

    def test_the_page_shows_no_meta_and_lists_the_evidence(self):
        i = dict(idea(), id="i001", meta={"estrategia": "invertir", "generador": "g07"})
        page, words = S.render_page(i, self.fichas, CFG)
        self.assertIn("## Evidencias citadas", page)
        self.assertIn("F-agro-002", page)
        self.assertNotIn("invertir", page)
        self.assertNotIn("g07", page)
        self.assertLess(words, CFG["filter"]["idea_max_words"])
        body = page.split("\n---\n")[0]
        self.assertEqual(words, len(body.split()))


# ---------------------------------------------------------------- evidence

class Evidence(unittest.TestCase):
    def results(self, **states):
        return {"https://ejemplo.uy/%s" % k.replace("_", "-"): dict(v, checked_at="t") for k, v in states.items()}

    def test_dead_urls_are_discarded_and_blocked_ones_flagged(self):
        fs = [ficha("F-agro-001"), ficha("F-agro-002"), ficha("F-agro-003"), ficha("F-agro-004")]
        res = {"https://ejemplo.uy/F-agro-001": {"estado": "ok", "texto": PAGE},
               "https://ejemplo.uy/F-agro-002": {"estado": "bloqueada", "http": 403},
               "https://ejemplo.uy/F-agro-003": {"estado": "muerta", "http": 404}}
        acc, dis = S.process_fichas(fs, "F-agro-", res, CFG)
        self.assertEqual([f["id"] for f in acc], ["F-agro-001", "F-agro-002"])
        self.assertEqual(acc[1]["verificacion"]["estado"], "bloqueada")
        self.assertEqual({d["id"]: d["motivo"] for d in dis}, {"F-agro-003": "url_muerta", "F-agro-004": "url_sin_verificar"})
        strict = dict(CFG, evidence=dict(CFG["evidence"], on_blocked="discard"))
        acc, dis = S.process_fichas(fs[:2], "F-agro-", res, strict)
        self.assertEqual([f["id"] for f in acc], ["F-agro-001"])
        self.assertEqual(dis[0]["motivo"], "url_bloqueada")

    def test_excerpts_are_checked_against_the_page(self):
        res = {"https://ejemplo.uy/F-agro-001": {"estado": "ok", "texto": PAGE},
               "https://ejemplo.uy/F-agro-002": {"estado": "ok", "texto": PAGE}}
        fs = [ficha("F-agro-001", extracto="EL 30 % de las PYMES pierde horas"),
              ficha("F-agro-002", extracto="una frase que no aparece", confianza="alta")]
        acc, _ = S.process_fichas(fs, "F-agro-", res, CFG)
        self.assertEqual(acc[0]["verificacion"]["extracto"], "encontrado")
        self.assertEqual(acc[1]["verificacion"]["extracto"], "no_encontrado")
        self.assertEqual(acc[1]["confianza"], "baja")

    def test_prefix_and_repeats(self):
        res = {"https://ejemplo.uy/a": {"estado": "ok"}, "https://ejemplo.uy/b": {"estado": "ok"}}
        fs = [ficha("F-agro-001", url="https://ejemplo.uy/a"), ficha("F-salud-001", url="https://ejemplo.uy/b"),
              ficha("F-agro-001", url="https://ejemplo.uy/b"), ficha("F-agro-002", url="https://ejemplo.uy/a")]
        acc, dis = S.process_fichas(fs, "F-agro-", res, CFG)
        self.assertEqual([f["id"] for f in acc], ["F-agro-001"])
        self.assertEqual([d["motivo"] for d in dis], ["prefijo", "id_repetido", "url_repetida"])

    def test_check_urls_with_a_fake_fetcher(self):
        calls = []

        def fetch(url, timeout=None):
            calls.append(url)
            return ("ok", 200, PAGE) if "bien" in url else ("muerta", 404, None)
        res = E.check_urls(["https://bien.uy/1", "https://mal.uy/2", "https://bien.uy/1"], fetcher=fetch)
        self.assertEqual(sorted(calls), ["https://bien.uy/1", "https://mal.uy/2"], "each URL once")
        self.assertEqual(res["https://bien.uy/1"]["estado"], "ok")
        self.assertEqual(res["https://mal.uy/2"]["estado"], "muerta")

    def test_fetch_url_keeps_cookies_and_only_404_and_410_are_dead(self):
        class Handler(http.server.BaseHTTPRequestHandler):
            def reply(self, code, body=b"", **headers):
                self.send_response(code)
                for k, v in dict(headers, **{"Content-Length": str(len(body))}).items():
                    self.send_header(k.replace("_", "-"), v)
                self.end_headers()
                self.wfile.write(body)

            def do_GET(self):
                if self.path == "/cookie":   # like Google's docs: set a cookie and send the client back to the same URL
                    if "visto=1" in (self.headers.get("Cookie") or ""):
                        self.reply(200, PAGE.encode("utf-8"), Content_Type="text/html; charset=utf-8")
                    else:
                        self.reply(302, Set_Cookie="visto=1; Path=/", Location="/cookie")
                elif self.path == "/bucle":
                    self.reply(302, Location="/bucle")
                else:
                    self.reply(int(self.path.strip("/")))

            def log_message(self, *args):
                pass

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            base = "http://127.0.0.1:%d" % server.server_address[1]
            self.assertEqual(E.fetch_url(base + "/cookie", timeout=5)[:2], ("ok", 200))
            self.assertEqual(E.fetch_url(base + "/bucle", timeout=5)[0], "bloqueada", "a redirect loop is a refusal, not a missing page")
            for code, estado in ((400, "bloqueada"), (403, "bloqueada"), (404, "muerta"), (410, "muerta"), (503, "bloqueada")):
                self.assertEqual(E.fetch_url("%s/%d" % (base, code), timeout=5)[:2], (estado, code))
        finally:
            server.shutdown()
            server.server_close()

    def test_dashes_are_sanitized(self):
        self.assertEqual(E.sanitize_text("a %s b %s c" % (EM_DASH, EN_DASH)), "a - b - c")
        self.assertEqual(E.sanitize_obj({"k": ["x%sy" % EM_DASH]}), {"k": ["x-y"]})
        tmp = tempfile.mkdtemp()
        try:
            os.makedirs(os.path.join(tmp, "a"))
            with open(os.path.join(tmp, "a", "f.json"), "w", encoding="utf-8", newline="") as fh:
                fh.write('{"t": "uno %s dos"}\r\n' % EM_DASH)
            write(os.path.join(tmp, "g.md"), "sin rayas")
            changed = E.sweep_dashes(tmp)
            self.assertEqual([os.path.basename(p) for p in changed], ["f.json"])
            with open(os.path.join(tmp, "a", "f.json"), encoding="utf-8", newline="") as fh:
                self.assertEqual(fh.read(), '{"t": "uno - dos"}\r\n', "line endings untouched")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class Dedup(unittest.TestCase):
    def test_near_duplicates_cluster_and_distinct_ideas_do_not(self):
        a = E.idea_text(idea(titulo="Turnos para clínicas veterinarias", problema="Las clínicas veterinarias pierden turnos "
                             "porque los clientes no confirman por teléfono ni por WhatsApp a tiempo.", usuario="Clínicas veterinarias chicas"))
        b = E.idea_text(idea(titulo="Turnos para clínicas veterinarias del interior", problema="Las clínicas veterinarias pierden "
                             "turnos porque los clientes no confirman por teléfono ni por WhatsApp a tiempo.", usuario="Clínicas veterinarias chicas"))
        c = E.idea_text(idea(titulo="Conciliación bancaria para estudios contables", problema="Los estudios contables concilian "
                             "extractos bancarios a mano cada fin de mes y cometen errores.", usuario="Estudios contables",
                             solucion="Un conciliador automático de extractos y comprobantes fiscales."))
        self.assertGreater(E.similarity(a, b), 0.6)
        self.assertLess(E.similarity(a, c), 0.3)
        groups, links = E.clusters({"i1": a, "i2": b, "i3": c}, 0.5)
        self.assertEqual(groups, [["i1", "i2"], ["i3"]])
        groups, _ = E.clusters({"i1": a, "i2": b, "i3": c}, 0.99, extra_groups=[["i1", "i3"]])
        self.assertEqual(groups, [["i1", "i3"], ["i2"]], "the agent's groups are merged in")


class Diversity(unittest.TestCase):
    STRATEGIES = [{"id": s} for s in ("dolor", "capacidad", "segmento", "localizar", "invertir")]

    def sectors(self, n):
        return [{"id": "s%02d" % k} for k in range(n)]

    def test_each_generator_works_its_own_sectors(self):
        for agents, n_sectors, per_gen in ((5, 3, 1), (10, 10, 1), (5, 10, 2), (3, 3, 1)):
            gens = IA.assign_generators(self.STRATEGIES, self.sectors(n_sectors), {"agents": agents, "ideas_per_agent": 2}, 7)
            self.assertEqual(len(gens), agents)
            self.assertTrue(all(len(g["focus"]) == per_gen for g in gens), (agents, n_sectors, gens))
            covered = [s for g in gens for s in g["focus"]]
            self.assertEqual(sorted(set(covered)), sorted(s["id"] for s in self.sectors(n_sectors)), "every sector has a generator")
            if agents <= n_sectors:
                self.assertEqual(len(covered), len(set(covered)), "no two generators share a sector when there are enough")
            self.assertEqual([g["strategy"] for g in gens[:5]], [s["id"] for s in self.STRATEGIES][:min(5, agents)])

    def test_shared_evidence_marks_a_theme_and_themes_take_turns(self):
        cites = {"i1": ["F-a-1", "F-a-2", "F-a-3"], "i2": ["F-a-1", "F-a-2", "F-a-3", "F-a-4"],
                 "i3": ["F-a-5", "F-a-6"], "i4": ["F-a-1", "F-a-6"]}
        self.assertEqual(E.overlap(cites["i1"], cites["i2"]), 0.75)
        groups, _ = E.clusters(cites, 0.6, sim=E.overlap)
        self.assertEqual(groups, [["i1", "i2"], ["i3"], ["i4"]])
        theme_of = {iid: k for k, g in enumerate(groups) for iid in g}
        self.assertEqual(IA.theme_first(["i1", "i2", "i3", "i4"], theme_of), ["i1", "i3", "i4", "i2"],
                         "the second idea of a theme waits until every theme has one in")

    def test_the_theme_comes_from_the_cards_behind_the_problem(self):
        i = idea(evid=("F-agro-001", "F-agro-002", "F-agro-0010"), problema="Pierden horas (F-agro-001, F-agro-0010).",
                 comps=[{"nombre": "Comp", "evidencia_ids": ["F-agro-003"], "hueco": "caro"}])
        self.assertEqual(S.problem_ids(i), ["F-agro-001", "F-agro-0010"], "competitors and context are left out")
        self.assertEqual(S.problem_ids(idea(problema="Un problema sin citas.")), ["F-agro-001", "F-agro-002"],
                         "with no ids in the problem, every cited card counts")


# ---------------------------------------------------------------- the fatal rule

class FatalRule(unittest.TestCase):
    HARD = {"R1", "R2", "R3", "R4", "R5", "R6", "R7"}

    def decide(self, x, y, det=None, standing=None, winner="X", hard=HARD):
        v = {"scores": {"X": x, "Y": y}, "winner": winner}
        if standing:
            v["standing"] = standing
        nv = T.normalize_verdict(v, "i001", "i002")
        return T.decide(nv, "i001", "i002", hard, det)

    def test_weights_match_rubric_and_constraints(self):
        for name in ("rubric.md", "constraints.md"):
            with open(os.path.join(SKILL, name), encoding="utf-8") as fh:
                rows = re.findall(r"^\| (\w+) \| (\d+) \|", fh.read(), re.M)
            self.assertEqual([(k, int(w)) for k, w in rows], list(T.CRITERIA), name)
        self.assertEqual(sum(w for _, w in T.CRITERIA), 100)

    def test_total(self):
        self.assertEqual(T.weighted_total(sc(10)), 100.0)
        self.assertEqual(T.weighted_total(sc(8, demanda=6, academico=0)), 71.0)   # (150 + 200 + 160 + 120 + 80 + 0) / 10
        self.assertIsNone(T.weighted_total({"demanda": 9}))

    def test_a_fatal_idea_cannot_beat_a_clean_one(self):
        w, totals, fatal, notes = self.decide(sc(10, True, "restriccion_dura:R1: cuesta USD 900"), sc(3))
        self.assertEqual(w, "i002")
        self.assertEqual(fatal, {"i001": True, "i002": False})
        self.assertGreater(totals["i001"], totals["i002"])
        self.assertTrue(any("fallo fatal" in n for n in notes))
        w, _, _, _ = self.decide(sc(10, True, "afirmacion_sin_evidencia: 'nadie en Uruguay lo hace'"), sc(3))
        self.assertEqual(w, "i002")

    def test_fatal_needs_a_valid_category(self):
        for motivo in ("me pareció flojo", "", "restriccion_dura:R9: no existe", "afirmacion_sin_evidencia: x"):
            w, _, fatal, notes = self.decide(sc(10, True, motivo), sc(3))
            self.assertEqual(w, "i001", motivo)
            self.assertFalse(fatal["i001"])
            self.assertTrue(any("ignorado" in n for n in notes))

    def test_a_soft_restriction_is_not_fatal(self):
        w, _, fatal, _ = self.decide(sc(10, True, "restriccion_dura:R7: datos"), sc(3), hard={"R1"})
        self.assertEqual(w, "i001")

    def test_the_deterministic_check_overrides_the_judge(self):
        w, _, fatal, notes = self.decide(sc(10), sc(3), det={"i001": ["costo_tope"]})
        self.assertEqual(w, "i002")
        self.assertTrue(fatal["i001"])
        self.assertTrue(any("determinístico" in n for n in notes))

    def test_both_fatal_then_totals_decide(self):
        w, _, fatal, _ = self.decide(sc(4, True, "restriccion_dura:R2: no entra"), sc(6), det={"i002": ["costo_tope"]})
        self.assertEqual(w, "i002")
        self.assertEqual(fatal, {"i001": True, "i002": True})

    def test_ties(self):
        self.assertEqual(self.decide(sc(7), sc(7), standing={"X": ["a", "b"], "Y": ["c"]})[0], "i002")
        self.assertEqual(self.decide(sc(7, demanda=8, viabilidad=6), sc(7, demanda=6, viabilidad=8), winner="Y")[0], "i001",
                         "equal totals: demand breaks the tie before the judge's pick")
        self.assertEqual(self.decide(sc(7), sc(7), winner="Y")[0], "i002")
        with self.assertRaises(T.ArenaError):
            self.decide(sc(7), sc(7), winner="")

    def test_the_scores_beat_the_judges_pick(self):
        w, _, _, notes = self.decide(sc(4), sc(8), winner="X")
        self.assertEqual(w, "i002")
        self.assertTrue(any("mandan las reglas" in n for n in notes))

    def test_both_orders_are_merged(self):
        one = T.normalize_verdict({"scores": {"X": sc(8), "Y": sc(6)}, "winner": "X"}, "i001", "i002")
        two = T.normalize_verdict({"scores": {"X": sc(7), "Y": sc(6, True, "restriccion_dura:R1: caro")}, "winner": "X"}, "i002", "i001")
        nv = T.merge_verdicts([one, two], "i001", "i002")
        self.assertEqual(nv["scores"]["i001"]["demanda"], 7.0)
        self.assertIsNone(nv["pick"], "the two judges picked different ideas")
        w, _, fatal, _ = T.decide(nv, "i001", "i002", self.HARD)
        self.assertTrue(fatal["i001"], "a fatal claim from either order counts")
        self.assertEqual(w, "i002")


# ---------------------------------------------------------------- the tournament

def ideas_for(n):
    return [("i%03d" % i, "s%d" % (i % 4), "p/%d.md" % i, "p/%d.json" % i) for i in range(1, n + 1)]


def play(ts, rng):
    while not ts["champion"]:
        rd = B.current_round(ts)
        for m in rd["matches"]:
            B.record(ts, m["id"], rng.choice([m["a"], m["b"]]))
        T.advance_round(ts)
    return ts


class JudgeOrder(unittest.TestCase):
    def test_round_one_alternates_match_by_match(self):
        ts = T.new_tournament(ideas_for(16), 3, "t", ["cliente", "competidor", "inversor", "tutor"])
        for idx, m in enumerate(ts["rounds"][0]["matches"]):
            self.assertEqual(m["first"], m["a"] if idx % 2 == 0 else m["b"])
            self.assertEqual({m["first"], m["second"]}, {m["a"], m["b"]})

    def test_the_idea_shown_first_more_often_never_goes_first_again(self):
        worst = 0
        for n in range(2, 17):
            for seed in range(40):
                ts = play(T.new_tournament(ideas_for(n), seed, "t", ["a", "b", "c", "d"]), random.Random(seed))
                balance = {k: 0 for k in ts["agents"]}
                for rd in ts["rounds"]:
                    for m in rd["matches"]:
                        self.assertLessEqual(balance[m["first"]], balance[m["second"]], "n=%d seed=%d %s" % (n, seed, m["id"]))
                    for m in rd["matches"]:
                        balance[m["first"]] += 1
                        balance[m["second"]] -= 1
                worst = max([worst] + [abs(v) for v in balance.values()])
        self.assertLessEqual(worst, 3, "measured bound for up to 16 ideas (4 rounds)")

    def test_both_orders_add_a_swapped_judge(self):
        ts = T.new_tournament(ideas_for(4), 1, "t", ["a"], both_orders=True)
        jobs = T.tournament_jobs(ts, "judge")
        self.assertEqual(len(jobs), 4)
        for a, b in zip(jobs[::2], jobs[1::2]):
            self.assertEqual((a["x"], a["y"]), (b["y"], b["x"]))
            self.assertNotEqual(a["outputs"], b["outputs"])

    def test_personas_rotate_and_both_sides_get_the_same(self):
        order = ["cliente", "competidor", "inversor", "tutor"]
        ts = play(T.new_tournament(ideas_for(16), 9, "t", order), random.Random(9))
        for rd in ts["rounds"]:
            for m in rd["matches"]:
                self.assertEqual(m["personas"], [order[rd["n"] - 1]])
        self.assertEqual(sorted(ts["agents"][ts["champion"]]["personas"]), sorted(order), "the champion faced all four")


class BracketContract(unittest.TestCase):
    def test_same_sizes_calls_and_waves_as_arena(self):
        for n in (2, 3, 7, 8, 13, 16, 31, 64):
            rows = T.tournament_plan(n)
            arena = B.plan_totals(n)
            self.assertEqual(sum(r["calls"] for r in rows), arena["calls"] - n, "n=%d (arena adds the spawn)" % n)
            self.assertEqual(sum(r["waves"] for r in rows), arena["waves"] - -(-n // 10))
            ts = play(T.new_tournament(ideas_for(n), n, "t", ["a", "b"]), random.Random(n))
            self.assertEqual([len(rd["alive"]) for rd in ts["rounds"]] + [1], B.bracket_sizes(n))
            self.assertEqual(len(B.alive_ids(ts)), 1)
            self.assertTrue(all(a["byes"] <= 1 for a in ts["agents"].values()))

    def test_advance_carries_the_revised_idea(self):
        tmp = tempfile.mkdtemp()
        try:
            ts = T.new_tournament(ideas_for(4), 2, os.path.join(tmp, "t").replace("\\", "/"), ["a"])
            rd = B.current_round(ts)
            for m in rd["matches"]:
                for iid in (m["a"], m["b"]):
                    write(T.solution_md(ts, 1, m["id"], iid), "revised")
                B.record(ts, m["id"], m["a"])
            T.advance_round(ts)
            for m in rd["matches"]:
                ag = ts["agents"][m["a"]]
                self.assertEqual(ag["solution"], T.solution_md(ts, 1, m["id"], m["a"]))
                self.assertEqual(ag["idea_json"], T.revised_json(ts, 1, m["id"], m["a"]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_a_fatal_loser_ranks_below_the_clean_ones(self):
        ts = T.new_tournament(ideas_for(4), 6, "t", ["a"])
        rd = B.current_round(ts)
        m1, m2 = rd["matches"]
        B.record(ts, m1["id"], m1["a"], scores={m1["a"]: 40, m1["b"]: 95})
        m1["fatal"] = {m1["a"]: False, m1["b"]: True}
        B.record(ts, m2["id"], m2["a"], scores={m2["a"]: 60, m2["b"]: 50})
        T.advance_round(ts)
        rd = B.current_round(ts)
        B.record(ts, rd["matches"][0]["id"], rd["matches"][0]["a"])
        T.advance_round(ts)
        rows = T.ranking(ts)
        self.assertEqual([r["id"] for r in rows[2:]], [m2["b"], m1["b"]])
        self.assertTrue(rows[3]["fatal"])

    def test_ranking(self):
        ts = play(T.new_tournament(ideas_for(8), 4, "t", ["a"]), random.Random(4))
        rows = T.ranking(ts)
        self.assertEqual(rows[0]["id"], ts["champion"])
        self.assertEqual(rows[1]["eliminated_in"], 3, "the finalist is second")
        self.assertEqual(sorted(r["rank"] for r in rows), list(range(1, 9)))
        self.assertEqual([r["reached_round"] for r in rows], sorted((r["reached_round"] for r in rows), reverse=True))


class Calibration(unittest.TestCase):
    def test_ranking_file(self):
        names = ["idea_A", "idea_B", "idea_C"]
        self.assertEqual(IA.parse_ranking("1. idea_B\n2) `idea_C`\n3. idea_A extra\n", names), ["idea_B", "idea_C", "idea_A"])
        with self.assertRaises(IA.IdeaArenaError):
            IA.parse_ranking("1. idea_A\n2. idea_A\n", names)

    def test_metrics(self):
        user = ["A", "B", "C"]

        def r(x, y, w, tx=60, ty=50):
            return {"x": x, "y": y, "winner": w, "totals": {x: tx, y: ty}, "criteria": {x: sc(6), y: sc(5)}}
        results = [r("A", "B", "A"), r("B", "A", "A", 40, 70), r("A", "C", "A"), r("C", "A", "A", 40, 70),
                   r("B", "C", "C", 40, 60), r("C", "B", "C")]
        met = IA.calibration_metrics(user, results)
        self.assertEqual((met["acuerdo"], met["total_pares"], met["consistencia"]), (2, 3, 3))
        self.assertEqual(met["orden_juez"], ["A", "C", "B"])
        self.assertEqual(met["kendall_tau"], round(1 / 3.0, 3))
        self.assertEqual(met["x_gana"], 0.5)
        self.assertEqual(IA.kendall_tau(["A", "B", "C"], ["C", "B", "A"]), -1.0)


class Inputs(unittest.TestCase):
    def test_hard_restrictions(self):
        text = "## 1. Restricciones duras\n\n- **R1** (a): uno.\n- **R2** (b): dos\n  sigue [A CONFIRMAR].\n- **R3** (c): tres.\n\n## 2. Otra\n- **R9** no.\n"
        self.assertEqual(IA.hard_restrictions(text), (["R1", "R3"], ["R2"]))
        confirmed, pending = IA.hard_restrictions(read(IA.CONSTRAINTS_PATH))
        self.assertEqual(confirmed, ["R1", "R2", "R3", "R4", "R5", "R6", "R7"])
        self.assertEqual(pending, [])

    def test_the_project_shim_matches_the_skill(self):
        def front(path):
            return read(path).split("---")[1]
        self.assertEqual(front(os.path.join(REPO, ".claude", "skills", "idea-arena", "SKILL.md")), front(os.path.join(SKILL, "SKILL.md")))

    def test_every_brief_and_template_exists(self):
        for name in list(IA.BRIEF_OF.values()) + ["_comunes"] + ["06_profundizar_%s" % a for a in CFG["deepen"]["aspects"]]:
            self.assertTrue(os.path.isfile(os.path.join(IA.BRIEFS_DIR, name + ".md")), name)
        self.assertTrue(os.path.isfile(os.path.join(IA.TEMPLATES_DIR, "guion_entrevista.md")))

    def test_runs_is_versioned(self):
        with open(os.path.join(REPO, ".gitignore"), encoding="utf-8") as fh:
            self.assertNotIn("runs", fh.read())
        try:
            r = subprocess.run(["git", "check-ignore", "-q", "runs/20990101-0000/state.json"], cwd=REPO,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError:
            self.skipTest("git is not available")
        self.assertEqual(r.returncode, 1, "runs/ must not be ignored by git")

    def test_writes_outside_runs_are_refused(self):
        with self.assertRaises(IA.IdeaArenaError):
            IA.guard(os.path.join(REPO, "skills", "idea-arena", "x.txt"))
        with self.assertRaises(IA.IdeaArenaError):
            IA.guard(os.path.join(os.getcwd(), "runs", "..", "x.txt"))
        IA.guard(os.path.join(os.getcwd(), "runs", "20990101-0000", "x.txt"))   # allowed, and writes nothing


# ---------------------------------------------------------------- the command line

class CliCase(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="idea-arena-test-")
        self.fetch = os.path.join(tempfile.mkdtemp(prefix="idea-arena-fetch-"), "fetch.json")
        table = {"*": {"status": "ok", "code": 200, "text": PAGE}}
        for s in CFG["sectors"]:
            table["https://muerta.ejemplo.uy/%s" % s["id"]] = {"status": "muerta", "code": 404}
            table["https://bloqueada.ejemplo.uy/%s" % s["id"]] = {"status": "bloqueada", "code": 403}
        write_json(self.fetch, table)

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)
        shutil.rmtree(os.path.dirname(self.fetch), ignore_errors=True)

    def cli(self, *args):
        env = dict(os.environ, IDEA_ARENA_ROOT=self.root, IDEA_ARENA_TEST_FETCH=self.fetch,
                   PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, TOOL] + [str(a) for a in args], cwd=self.root, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return r.returncode, r.stdout.decode("utf-8"), r.stderr.decode("utf-8")

    def ok(self, *args):
        code, out, err = self.cli(*args)
        self.assertEqual(code, 0, "idea_arena.py %s failed:\n%s%s" % (" ".join(map(str, args)), out, err))
        return out


class DryRunAndCaps(CliCase):
    def test_dry_run_prints_the_plan_and_writes_nothing(self):
        out = self.ok("init", "--pilot", "--dry-run", "--seed", 1)
        self.assertIn("hasta 53", out)
        self.assertIn("Dry-run", out)
        out = self.ok("plan", "--seed", 1)
        self.assertIn("hasta 114", out)
        plan = json.loads(self.ok("plan", "--json", "--seed", 1))
        self.assertEqual((plan["calls"], plan["waves"], plan["candidates"]), (114, 19, 16))
        self.assertEqual([r["calls"] for r in plan["rows"] if r["kind"] == "agentes"], [10, 10, 10, 1, 75, 8])
        self.assertEqual(os.listdir(self.root), [], "a dry run writes nothing")

    def test_init_refuses_a_plan_over_the_caps(self):
        cfg = IA.load_json_file(IA.CONFIG_PATH)
        cfg["limits"]["research"] = 2
        path = os.path.join(os.path.dirname(self.fetch), "config.json")
        write_json(path, cfg)
        code, out, err = self.cli("init", "--config", path, "--seed", 1)
        self.assertEqual(code, 2)
        self.assertIn("supera los topes", err)
        self.assertEqual(os.listdir(self.root), [])
        code, out, _ = self.cli("plan", "--config", path, "--seed", 1)
        self.assertIn("EXCEDE", out)

    def test_calibration_refuses_placeholders(self):
        # its own calibration dir, so the result does not depend on whether you filled in the repo's
        cdir = os.path.join(os.path.dirname(self.fetch), "calibration")
        for name in ("idea_A", "idea_B"):
            write(os.path.join(cdir, "ideas", name + ".md"), "# %s\n\n**Problema.** Uno real.\n" % name)
        write(os.path.join(cdir, "ideas", "idea_C.md"), "# idea_C\n\n**Problema.** <<COMPLETAR: el problema>>\n")
        write(os.path.join(cdir, "my_ranking.md"), "# Mi ranking\n\n1. idea_A\n2. idea_B\n3. idea_C\n")
        code, _, err = self.cli("calibrate", "--calibration-dir", cdir)
        self.assertEqual(code, 2)
        self.assertIn("placeholders", err)
        self.assertIn("idea_C.md:3", err)
        self.assertEqual(os.listdir(self.root), [])


class WordCheck(CliCase):
    def test_palabras_counts_like_the_filter_and_says_how_much_to_cut(self):
        self.ok("init", "--pilot", "--seed", 1)
        path = os.path.join(os.path.dirname(self.fetch), "ideas.json")
        long = idea(supuestos=[("dato " * 55).strip()] * 12)
        write_json(path, {"generador": "g01", "ideas": [dict(idea(), local_id="g01-1"), dict(long, local_id="g01-2")]})
        code, out, _ = self.cli("palabras", path)
        self.assertEqual(code, 1, out)
        _, words = S.render_page(S.idea_body(idea()), {}, CFG)
        self.assertIn("OK   g01-1: %d palabras (máximo 700)" % words, out)
        self.assertRegex(out, r"MAL  g01-2: \d+ palabras \(máximo 700\): recortá \d+")
        write_json(path, idea(total=500, items=[dict(idea()["costo_infra"]["items"][0], usd_anual=500)]))
        code, out, _ = self.cli("palabras", path)
        self.assertEqual(code, 1)
        self.assertIn("supera el tope", out, "the budget cap is checked too")
        write_json(path, idea())
        self.assertIn("OK", self.ok("palabras", path))


class FakeAgents(object):
    """Write the files real sub-agents would, including a few bad ones on purpose."""
    VOCAB = ("turnos clínicas stock depósitos cosecha riego facturas cobranzas reclamos aduana flota choferes "
             "rutas pacientes recetas aulas docentes notas contratos expedientes trámites reservas hoteles "
             "excursiones medidores consumo residuos reciclaje seguros siniestros créditos pagos").split()

    def __init__(self, case, rng):
        self.case, self.rng = case, rng
        self.fatal_ideas = set()
        self.dup_text = None

    def text(self, n):
        return " ".join(self.rng.choice(self.VOCAB) for _ in range(n))

    def run(self, d, st, ts, job):
        getattr(self, job["kind"])(d, st, ts, job)

    def research(self, d, st, ts, job):
        sid = job["sector"]["id"]
        fs = []
        for k in range(1, 6):
            f = ficha("F-%s-%03d" % (sid, k), sector=sid, geo="US" if k == 5 else "UY",
                      url="https://ejemplo.uy/%s/%d" % (sid, k), hallazgo="Dato %s del sector, %d%% de las empresas." % (EM_DASH, 10 * k))
            if k == 1:
                f["extracto"] = "el 30% de las pymes"
            if k == 2:
                f["extracto"] = "una frase que no aparece en la página"
            fs.append(f)
        fs.append(ficha("F-%s-006" % sid, sector=sid, url="https://muerta.ejemplo.uy/%s" % sid))
        fs.append(ficha("F-%s-007" % sid, sector=sid, url="https://bloqueada.ejemplo.uy/%s" % sid))
        fs.append(ficha("F-otro-008", sector=sid, url="https://ejemplo.uy/%s/otro" % sid))
        write_json(job["outputs"][0], {"sector": sid, "fichas": fs})

    def generate(self, d, st, ts, job):
        g = job["gen"]
        ideas = []
        for k in range(1, g["ideas"] + 1):
            s = g["focus"][(k - 1) % len(g["focus"])]
            i = idea(evid=("F-%s-001" % s, "F-%s-003" % s, "F-%s-004" % s),
                     comps=[{"nombre": "Competidor %s" % s, "evidencia_ids": ["F-%s-004" % s], "hueco": "no atiende pymes"}],
                     titulo="Idea sobre %s" % self.text(3), problema="Problema: %s (F-%s-001)." % (self.text(12), s),
                     usuario="Usuarios %s" % self.text(4), solucion="Solución que %s." % self.text(12), local_id="%s-%d" % (g["id"], k))
            if g["id"] == "g01" and k == 2:
                i["costo_infra"] = {"total_anual_usd": 500, "items": [dict(i["costo_infra"]["items"][0], usd_anual=500)]}
            if g["id"] == "g02" and k == 2:
                del i["riesgos"]
            if g["id"] in ("g03", "g04") and k == 1:
                if self.dup_text is None:
                    self.dup_text = {key: i[key] for key in ("titulo", "problema", "usuario", "solucion")}
                i.update(self.dup_text)
            ideas.append(i)
        write_json(job["outputs"][0], {"generador": g["id"], "ideas": ideas})

    def scope(self, d, st, ts, job):
        first = next(iid for iid in st["scope_batches"][0]
                     if IA.read_json(IA.j(d, "ideas", iid + ".json"))["titulo"] != self.dup_text["titulo"])
        ev = [{"id": iid, "veredicto": "inviable" if iid == first else "viable", "horas_estimadas": 900,
               "motivo": "Estimación hecha componente por componente."} for iid in job["batch"]]
        write_json(job["outputs"][0], {"evaluaciones": ev})

    def dedup(self, d, st, ts, job):
        lex = IA.read_json(IA.j(d, "filter", "dedup_lexico.json"))["grupos"]
        grouped = set(x for g in lex for x in g)
        groups = lex + [[iid] for iid in st["candidates"] if iid not in grouped]
        write_json(job["outputs"][0], {"grupos": groups, "motivos": ["por similitud"]})

    def attack(self, d, st, ts, job):
        prefix = IA.ficha_prefix("attack", job["match"], job["idea"], job["persona"])
        some = sorted(IA.load_fichas(d))[0]
        data = {"idea": job["idea"], "persona": job["persona"], "ataques": [
            {"n": 1, "severidad": "MAJOR", "titulo": "Demanda floja", "donde": "Problema",
             "problema": "La ficha citada no muestra disposición a pagar.", "tipo": "evidencia", "evidencia": [some]},
            {"n": 2, "severidad": "MINOR", "titulo": "Cita inventada", "donde": "Competidores",
             "problema": "Se apoya en una ficha que no existe.", "tipo": "evidencia", "evidencia": ["F-agro-999"]},
            {"n": 3, "severidad": "FATAL", "titulo": "Ya existe", "donde": "Diferenciación",
             "problema": "Un competidor local ya hace esto mismo.", "tipo": "evidencia", "evidencia": [prefix + "001"]}],
            "nuevas_fichas": [ficha(prefix + "001", sector="transversal", url="https://competidor.ejemplo.com/%s/%s" % (job["match"], job["idea"])),
                              ficha("F-mal-prefijo-001", sector="transversal")]}
        write_json(job["outputs"][0], data)

    def defend(self, d, st, ts, job):
        iid = job["idea"]
        cur = IA.read_json(ts["agents"][iid]["idea_json"])
        rev = S.idea_body(cur)
        rev["solucion"] = cur["solucion"] + " Revisada en %s." % job["match"]
        m = next(mm for mm in B.current_round(ts)["matches"] if mm["id"] == job["match"])
        if job["round"] == 1 and m["id"].endswith("m01") and iid == m["first"]:
            rev["costo_infra"] = {"total_anual_usd": 400, "items": [dict(rev["costo_infra"]["items"][0], usd_anual=400)]}
            self.fatal_ideas.add(iid)
        write_json(job["outputs"][0], {"idea": iid, "respuestas": [
            {"ataque": 1, "decision": "CONCEDE", "detalle": "Agregamos el supuesto de pago."},
            {"ataque": 2, "decision": "REBUT", "detalle": "Esa ficha no es nuestra."},
            {"ataque": 3, "decision": "PARCIAL", "detalle": "El competidor existe, pero no atiende pymes."}], "nuevas_fichas": []})
        write_json(job["outputs"][1], rev)

    def judge(self, d, st, ts, job):
        def s(iid):
            return sc(10) if iid in self.fatal_ideas else sc(self.rng.randint(3, 9))
        write_json(job["outputs"][0], {"match": job["match"], "scores": {"X": s(job["x"]), "Y": s(job["y"])},
                                       "winner": "X", "reason": "una diferencia", "survived": ["demanda floja"],
                                       "standing": {"X": ["cita inventada"], "Y": []}})

    def questions(self, d, st, ts, job):
        n = IA.read_json(IA.j(d, "inputs", "config.json"))["shortlist"]["questions_per_idea"]
        write_json(job["outputs"][0], {"idea": job["idea"], "preguntas": [
            {"pregunta": "¿Cómo lo resolvieron la última vez? (%d)" % k, "a_quien": "encargado de compras",
             "que_valida": "el dolor"} for k in range(n)]})

    def deepen(self, d, st, ts, job):
        write(job["outputs"][0], "# %s\n\nBosquejo.\n" % job["aspect"])
        prefix = IA.ficha_prefix("deepen", iid=job["idea"], aspect=job["aspect"])
        write_json(job["outputs"][1], {"nuevas_fichas": [ficha(prefix + "001", sector="transversal",
                                                               url="https://docs.ejemplo.com/%s" % job["aspect"])]})

    def calibrate(self, d, st, ts, job):
        rank = st["calibration"]["ranking"]
        better = job["x"] if rank.index(job["x"]) < rank.index(job["y"]) else job["y"]
        lab = "X" if better == job["x"] else "Y"
        other = "Y" if lab == "X" else "X"
        write_json(job["outputs"][0], {"scores": {lab: sc(8), other: sc(5)}, "winner": lab, "reason": "r",
                                       "standing": {"X": [], "Y": []}})


class Pipeline(CliCase):
    def drive(self, agents, limit=500):
        seen = []
        strategies = IA.load_strategies()
        for _ in range(limit):
            out = self.ok("next")
            m = re.search(r"^(NEXT: (\w+)|DONE|STUCK)", out, re.M)
            self.assertIsNotNone(m, out)
            phase = "done" if m.group(1) == "DONE" else "stuck" if m.group(1) == "STUCK" else m.group(2)
            seen.append(phase)
            if phase in ("done", "stuck"):
                return seen
            if phase == "step":
                self.ok("step")
                continue
            listing = self.ok("prompts", phase)
            cwd = os.getcwd()
            os.chdir(self.root)
            try:
                d = IA.run_dir_from(type("A", (), {"run": None})())
                st = IA.read_json(IA.j(d, IA.STATE_FILE))
                ts = IA.load_tournament(d)
                jobs = IA.missing_jobs(IA.phase_jobs(d, st, phase))
                self.assertTrue(jobs, "%s listed no jobs:\n%s" % (phase, listing))
                for job in jobs:
                    self.assertIn(job["id"], listing)
                    brief = read(job["prompt"])
                    self.assertNotRegex(brief, r"\{\{\w+\}\}", "unfilled placeholder in %s" % job["id"])
                    self.assertNotIn("<!--", brief)
                    if phase in IA.TOURNAMENT_PHASES:
                        self.blind(brief, strategies, job["id"])
                        self.assertNotIn("meta.json", brief)
                    if phase == "attack":
                        self.blind(read(ts["agents"][job["idea"]]["solution"]), strategies, job["id"])
                    if phase == "judge":
                        m = next(mm for mm in B.current_round(ts)["matches"] if mm["id"] == job["match"])
                        x_line = "Idea X\n- la idea revisada: %s" % os.path.abspath(T.solution_md(ts, job["round"], m["id"], m["first"]))
                        self.assertIn(x_line, brief, "the judge reads the first idea as X")
                        self.blind(read(T.solution_md(ts, job["round"], m["id"], job["x"])), strategies, job["id"])
                    agents.run(d, st, ts, job)
            finally:
                os.chdir(cwd)
        self.fail("the pipeline did not finish: %s" % seen[-20:])

    def blind(self, text, strategies, where):
        for s in strategies:
            self.assertNotIn(s["name"], text, where)
            self.assertNotIn(s["how"], text, where)
        self.assertNotIn("estrategia", text.lower(), where)
        self.assertNotIn("local_id", text, where)
        self.assertIsNone(re.search(r"\bg\d\d-\d\b", text), where)

    def test_a_whole_pilot_writes_only_under_runs(self):
        skill_before = snapshot(SKILL)
        root_before = snapshot(self.root)
        self.ok("init", "--pilot", "--seed", 5)
        agents = FakeAgents(self, random.Random(5))
        seen = self.drive(agents)
        self.assertEqual(seen[-1], "done")
        for phase in ("research", "generate", "scope", "dedup", "attack", "defend", "judge", "questions"):
            self.assertIn(phase, seen)

        runs = os.path.join(self.root, "runs")
        d = read(os.path.join(runs, "LATEST")).strip()
        self.assertRegex(d, r"^runs/\d{8}-\d{4}$")
        run = os.path.join(self.root, d)
        st = json.loads(read(os.path.join(run, "state.json")))
        steps = st["steps"]

        # evidence: dead URLs and wrong prefixes out, blocked ones kept and flagged, excerpts checked
        fichas = {f["id"]: f for f in json.loads(read(os.path.join(run, "evidence", "fichas.json")))["fichas"]}
        self.assertEqual(steps["verify"]["aceptadas"], 3 * 6)
        self.assertEqual(steps["verify"]["motivos"], {"url_muerta": 3, "prefijo": 3})
        sid = st["sectors"][0]["id"]
        self.assertEqual(fichas["F-%s-007" % sid]["verificacion"]["estado"], "bloqueada")
        self.assertEqual(fichas["F-%s-001" % sid]["verificacion"]["extracto"], "encontrado")
        self.assertEqual(fichas["F-%s-002" % sid]["confianza"], "baja")

        # ideas and filters: one schema reject, one over budget, one inviable, one duplicate merged
        self.assertEqual(steps["ingest"]["rechazadas_esquema"], 1)
        self.assertEqual(steps["ingest"]["problemas"], {"costo_tope": 1})
        self.assertEqual(steps["scope-collect"]["veredictos"].get("inviable"), 1)
        self.assertEqual(steps["select"]["fusionadas"], 1)
        meta = json.loads(read(os.path.join(run, "ideas", "meta.json")))["ideas"]
        self.assertEqual(len(meta), 9)
        for iid in meta:
            page = read(os.path.join(run, "ideas", iid + ".md"))
            self.blind(page, IA.load_strategies(), iid)
            self.assertIn("## Evidencias citadas", page)

        # the tournament: 6 ideas, 3 rounds, a bye, the deterministic fatal flaw lost its match
        ts = json.loads(read(os.path.join(run, "tournament", "bracket.json")))
        self.assertEqual(ts["agents_n"], 6)
        self.assertEqual([len(rd["alive"]) for rd in ts["rounds"]], [6, 3, 2])
        self.assertTrue(any(rd["bye"] for rd in ts["rounds"]))
        self.assertEqual(sum(1 for a in ts["agents"].values() if a["alive"]), 1)
        self.assertEqual(len(agents.fatal_ideas), 1)
        bad = agents.fatal_ideas.pop()
        m1 = ts["rounds"][0]["matches"][0]
        self.assertEqual(m1["det_fatal"][bad], ["costo_tope"])
        self.assertNotEqual(m1["winner"], bad, "a fatal idea cannot win, even with the judge's 10s")
        self.assertNotIn(bad, st["shortlist"], "and it is never recommended")
        self.assertEqual(steps["rank"]["excluidas_por_fallo_fatal"], [bad])
        self.assertGreater(m1["scores"][bad], m1["scores"][m1["winner"]])
        attacks = read(os.path.join(run, "tournament", "r1", "%s.%s.ataques.md" % (m1["id"], m1["first"])))
        self.assertIn("reetiquetado", attacks, "an attack citing a missing card became an opinion")
        self.assertIn("F-mal-prefijo-001 (prefijo)", attacks)
        defense = read(os.path.join(run, "tournament", "r1", "%s.%s.defensa.md" % (m1["id"], m1["second"])))
        self.assertIn("ATAQUE 3: PARCIAL.", defense, "a partial answer is a valid defense")
        self.assertIn("## Temas compartidos", read(os.path.join(run, "filter", "reporte.md")))
        torneo = json.loads(read(os.path.join(run, "evidence", "fichas_torneo.json")))["fichas"]
        self.assertTrue(torneo and all(f["id"].startswith("F-ataque-") for f in torneo))

        # the shortlist
        shortlist = read(os.path.join(run, "shortlist.md"))
        top = st["shortlist"]
        self.assertEqual(len(top), 5)
        self.assertEqual(top[0], ts["champion"])
        self.assertIn("## Resumen", shortlist)
        for iid in top:
            self.assertIn("(%s)" % iid, shortlist)
            guion = read(os.path.join(run, "shortlist", "guiones", iid + ".md"))
            self.assertNotRegex(guion, r"\{\{\w+\}\}")
            self.assertIn("¿Cómo lo resolvieron la última vez?", guion)
        self.assertEqual(shortlist.count("### Preguntas para validar con el mercado"), 5)

        # deepen one idea, then the run is done again
        self.ok("deepen", ts["champion"])
        seen = self.drive(agents)
        self.assertIn("deepen", seen)
        self.assertEqual(seen[-1], "done")
        self.assertTrue(os.path.isfile(os.path.join(run, "deepen", ts["champion"], "README.md")))
        prof = json.loads(read(os.path.join(run, "evidence", "fichas_profundizar.json")))["fichas"]
        self.assertEqual(len(prof), 3)
        self.assertIn("campeona", self.ok("status"))

        # nothing outside runs/, nothing in skills/, and no forbidden dash anywhere in the run
        root_after = snapshot(self.root)
        changed = [k for k in set(root_before) | set(root_after) if root_before.get(k) != root_after.get(k)]
        self.assertTrue(changed)
        self.assertEqual([k for k in changed if not k.startswith("runs" + os.sep)], [])
        self.assertEqual(snapshot(SKILL), skill_before, "skills/idea-arena must not change")
        for k in root_after:
            with open(os.path.join(self.root, k), encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
            self.assertNotIn(EM_DASH, text, k)
            self.assertNotIn(EN_DASH, text, k)

    def test_calibration_measures_agreement_with_your_ranking(self):
        cdir = os.path.join(os.path.dirname(self.fetch), "calibration")
        for name in ("idea_A", "idea_B", "idea_C"):
            write(os.path.join(cdir, "ideas", name + ".md"), "<!-- nota para vos -->\n# %s\n\n**Problema.** Uno real.\n" % name)
        write(os.path.join(cdir, "my_ranking.md"), "# Mi ranking\n\n1. idea_C\n2. idea_A\n3. idea_B\n")
        self.assertIn("6 llamadas", self.ok("calibrate", "--calibration-dir", cdir, "--dry-run"))
        self.assertEqual(os.listdir(self.root), [])
        self.ok("calibrate", "--calibration-dir", cdir, "--seed", 2)
        seen = self.drive(FakeAgents(self, random.Random(2)))
        self.assertEqual(seen.count("calibrate"), 1)
        run = os.path.join(self.root, read(os.path.join(self.root, "runs", "LATEST")).strip())
        report = read(os.path.join(run, "calibration_report.md"))
        self.assertIn("**3 de 3**", report)
        self.assertIn("idea_C > idea_A > idea_B", report)
        self.assertNotIn("nota para vos", read(os.path.join(run, "calibration", "ideas", "idea_A.md")))
        prompts = os.listdir(os.path.join(run, "prompts", "calibrate"))
        self.assertEqual(len(prompts), 6)

    def test_unreadable_outputs_are_set_aside_then_fall_back(self):
        self.ok("init", "--pilot", "--seed", 8)
        self.ok("prompts", "research")
        run = os.path.join(self.root, read(os.path.join(self.root, "runs", "LATEST")).strip())
        raw = os.path.join(run, "evidence", "raw")
        cwd = os.getcwd()
        os.chdir(self.root)
        try:
            d = IA.run_dir_from(type("A", (), {"run": None})())
            st = IA.read_json(IA.j(d, IA.STATE_FILE))
            agents = FakeAgents(self, random.Random(8))
            jobs = IA.phase_jobs(d, st, "research")
            for job in jobs:
                agents.run(d, st, None, job)
        finally:
            os.chdir(cwd)
        target = os.path.join(raw, st["sectors"][0]["id"] + ".json")
        write(target, "el agente divagó y no escribió JSON")
        self.ok("step")
        self.assertTrue(os.path.isfile(target + ".invalido1"))
        self.assertIn("NEXT: research", self.ok("next"), "the job is missing again and gets re-run")
        write(target, "otra vez sin JSON")
        self.ok("step")
        self.assertEqual(read(target).strip(), "NO OUTPUT", "the second failure falls back")
        self.assertIn("NEXT: generate", self.ok("next"), "and the step went on without that sector")
        st = json.loads(read(os.path.join(run, "state.json")))
        self.assertEqual(st["steps"]["verify"]["por_sector"][st["sectors"][0]["id"]]["recibidas"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
