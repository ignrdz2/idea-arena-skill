"""ia_schema.py: formats, the hard filter and the one-page view for /idea-arena.

- validate(): a small JSON Schema subset (type, enum, required, properties,
  additionalProperties, items, min/maxItems, min/maxLength, minimum/maximum, pattern,
  format uri and date-time). The schemas live in schemas/ and double as the format
  spec the sub-agents read.
- process_fichas(): schema, id prefix and URL status for evidence cards.
- hard_check(): the deterministic checks that drop an idea before the tournament and
  make a revised idea fatal during it.
- render_page(): the one-page markdown every attacker, defender and judge reads. It
  never shows the idea's meta (strategy, generator).

Python 3.8+, standard library only.
"""
import datetime
import json
import os
import re

import ia_evidence as E

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(HERE, "schemas")

# Failing any of these in a revised idea is a verified fatal flaw: a hard restriction
# broken (R1 budget) or a claim without evidence behind it.
FATAL_CODES = ("costo_tope", "costo_suma", "evidencia_inexistente", "evidencia_minima",
               "evidencia_local", "evidencia_solo_bloqueada", "competidor_sin_ficha")

# Warnings: shown on the page for the judge, but they never drop an idea. A price without a
# verified source is an estimate; the budget cap still applies to it.
WARNING_CODES = ("costo_estimado",)

_cache = {}


def load_schema(name, schema_dir=None):
    path = os.path.join(schema_dir or SCHEMA_DIR, "%s.schema.json" % name)
    if path not in _cache:
        with open(path, encoding="utf-8") as fh:
            _cache[path] = json.load(fh)
    return _cache[path]


# ---------------------------------------------------------------- the validator

_DATE_TIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?$")
_TYPES = {
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "array": lambda v: isinstance(v, list),
    "object": lambda v: isinstance(v, dict),
    "null": lambda v: v is None,
}


def _short(v):
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
    return s if len(s) <= 60 else s[:57] + "..."


def validate(value, schema, path="$"):
    """Every way value breaks schema, as readable strings. An empty list means valid."""
    errors = []
    if "enum" in schema and value not in schema["enum"]:
        return ["%s: '%s' no es uno de %s" % (path, _short(value), ", ".join(map(str, schema["enum"])))]
    t = schema.get("type")
    if t:
        types = t if isinstance(t, list) else [t]
        if not any(_TYPES[x](value) for x in types):
            return ["%s: se esperaba %s" % (path, " o ".join(types))]
    if isinstance(value, str):
        if "minLength" in schema and len(value.strip()) < schema["minLength"]:
            errors.append("%s: demasiado corto (mínimo %d caracteres)" % (path, schema["minLength"]))
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append("%s: demasiado largo (máximo %d caracteres)" % (path, schema["maxLength"]))
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append("%s: '%s' no tiene el formato esperado" % (path, _short(value)))
        fmt = schema.get("format")
        if fmt == "uri" and not E.is_url(value):
            errors.append("%s: '%s' no es una URL http(s)" % (path, _short(value)))
        if fmt == "date-time" and not _DATE_TIME_RE.match(value):
            errors.append("%s: '%s' no es una fecha y hora ISO 8601" % (path, _short(value)))
    if _TYPES["number"](value):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append("%s: menor que %s" % (path, schema["minimum"]))
        if "maximum" in schema and value > schema["maximum"]:
            errors.append("%s: mayor que %s" % (path, schema["maximum"]))
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append("%s: hacen falta al menos %d elementos" % (path, schema["minItems"]))
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append("%s: como mucho %d elementos" % (path, schema["maxItems"]))
        if "items" in schema:
            for i, item in enumerate(value):
                errors.extend(validate(item, schema["items"], "%s[%d]" % (path, i)))
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append("%s: falta el campo '%s'" % (path, key))
        if schema.get("additionalProperties") is False:
            for key in sorted(value):
                if key not in props:
                    errors.append("%s: campo no permitido '%s'" % (path, key))
        for key, sub in props.items():
            if key in value:
                errors.extend(validate(value[key], sub, "%s.%s" % (path, key)))
    return errors


# ---------------------------------------------------------------- evidence cards

def _age_years(source_date, today):
    m = re.match(r"^(\d{4})", source_date or "")
    return None if not m else today.year - int(m.group(1))


def process_fichas(fichas, prefix, url_results, cfg, seen_ids=(), today=None):
    """Check evidence cards against the schema, their id prefix and the URL results.

    url_results is {url: {"estado", "http", "checked_at", "texto"?}}. Returns
    (accepted, discarded). An accepted card gets a "verificacion" block; a discarded
    one keeps its reason. Dead URLs are always discarded; blocked ones follow
    evidence.on_blocked ("keep_flagged" or "discard")."""
    ecfg = cfg["evidence"]
    today = today or datetime.date.today()
    schema = load_schema("ficha")
    seen = set(seen_ids)
    seen_urls = set()
    accepted, discarded = [], []
    for f in fichas if isinstance(fichas, list) else []:
        if not isinstance(f, dict):
            discarded.append({"id": None, "motivo": "no es un objeto JSON"})
            continue
        f = dict(f)
        f.pop("verificacion", None)
        f = E.sanitize_obj(f)

        def drop(reason, **extra):
            d = {"id": f.get("id"), "source_url": f.get("source_url"), "motivo": reason}
            d.update(extra)
            discarded.append(d)

        errs = validate(f, schema)
        if errs:
            drop("esquema", errores=errs[:5])
            continue
        if not f["id"].startswith(prefix):
            drop("prefijo", errores=["el id tiene que empezar con %s" % prefix])
            continue
        if f["id"] in seen:
            drop("id_repetido")
            continue
        if f["source_url"] in seen_urls:
            drop("url_repetida")
            continue
        res = url_results.get(f["source_url"]) or {}
        estado = res.get("estado", "sin_verificar")
        if estado == E.DEAD:
            drop("url_muerta", http=res.get("http"))
            continue
        if estado == E.BLOCKED and ecfg.get("on_blocked", "keep_flagged") == "discard":
            drop("url_bloqueada", http=res.get("http"))
            continue
        if estado not in (E.OK, E.BLOCKED):
            drop("url_sin_verificar")
            continue
        ver = {"estado": estado, "http": res.get("http"), "checked_at": res.get("checked_at")}
        if f.get("extracto"):
            text = res.get("texto")
            if estado == E.OK and text:
                if E.excerpt_found(f["extracto"], text):
                    ver["extracto"] = "encontrado"
                elif ecfg.get("excerpt_check", "warn") == "discard":
                    drop("extracto_no_encontrado")
                    continue
                else:
                    ver["extracto"] = "no_encontrado"
                    f["confianza"] = "baja"
            else:
                ver["extracto"] = "no_verificable"
        else:
            ver["extracto"] = "sin_extracto"
        age = _age_years(f["source_date"], today)
        max_age = cfg.get("research", {}).get("max_source_age_years")
        if age is not None and max_age and age > max_age:
            ver["aviso"] = "fuente de hace %d años" % age
        f["verificacion"] = ver
        seen.add(f["id"])
        seen_urls.add(f["source_url"])
        accepted.append(f)
    return accepted, discarded


def ficha_estado(ficha):
    return ((ficha or {}).get("verificacion") or {}).get("estado")


# ---------------------------------------------------------------- ideas

def idea_body(idea):
    """The idea without the fields Python adds or the generator's local id. A cost item whose
    price source is empty loses the field: it is an estimate, which the schema allows."""
    body = {k: v for k, v in idea.items() if k not in ("id", "meta", "local_id")}
    cost = body.get("costo_infra")
    if isinstance(cost, dict) and isinstance(cost.get("items"), list):
        body["costo_infra"] = dict(cost, items=[
            {k: v for k, v in it.items() if not (k == "fuente_precio_url" and (v is None or str(v).strip() == ""))}
            if isinstance(it, dict) else it for it in cost["items"]])
    return body


def cited_ids(idea):
    """Every evidence id the idea cites, in order of first appearance, competitors included."""
    out = []
    for x in list(idea.get("evidencias") or []) + [e for c in (idea.get("competidores") or [])
                                                   if isinstance(c, dict) for e in (c.get("evidencia_ids") or [])]:
        if isinstance(x, str) and x not in out:
            out.append(x)
    return out


def problem_ids(idea):
    """The cited evidence ids that the problem statement names: the cards behind the pain itself,
    not the competitors or the context. Every cited id when the problem names none."""
    text = idea.get("problema") or ""
    named = [c for c in cited_ids(idea) if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(c), text)]
    return named or cited_ids(idea)


def is_local(geo, cfg):
    return str(geo).split("-")[0] in set(cfg["evidence"]["local_geographies"])


def hard_check(idea, fichas, url_status, cfg, page_words=None):
    """[(code, message)] for every hard rule the idea breaks, warnings included: the idea
    passes when blocking() of this list is empty.
    fichas is {id: card}; url_status is {url: {"estado": ...}} for the price sources."""
    errs = validate(idea_body(idea), load_schema("idea"))
    if errs:
        return [("esquema", e) for e in errs[:8]]
    fcfg = cfg["filter"]
    problems = []
    cap = float(cfg["infra_budget_usd"])
    cost = idea["costo_infra"]
    total = float(cost["total_anual_usd"])
    summed = sum(float(it["usd_anual"]) for it in cost["items"])
    if total > cap + 1e-9:
        problems.append(("costo_tope", "el costo de infraestructura (USD %g por año) supera el tope de USD %g" % (total, cap)))
    if abs(summed - total) > 1.0:
        problems.append(("costo_suma", "los ítems de costo suman USD %g pero el total dice USD %g" % (summed, total)))
    for it in cost["items"]:
        url = it.get("fuente_precio_url")
        st = (url_status.get(url) or {}).get("estado") if url else None
        if not url:
            problems.append(("costo_estimado", "el precio de '%s' es una estimación sin fuente" % it["concepto"]))
        elif st == E.DEAD:
            problems.append(("costo_estimado", "el precio de '%s' queda como estimación: su fuente no existe (%s)"
                             % (it["concepto"], url)))
        elif st not in (E.OK, E.BLOCKED):
            problems.append(("costo_estimado", "el precio de '%s' queda como estimación: su fuente no se pudo verificar"
                             % it["concepto"]))
    cited = cited_ids(idea)
    missing = [c for c in cited if c not in fichas]
    if missing:
        problems.append(("evidencia_inexistente", "cita fichas que no existen o fueron descartadas: %s" % ", ".join(missing)))
    valid = [c for c in cited if c in fichas]
    if len(valid) < fcfg["min_evidence_per_idea"]:
        problems.append(("evidencia_minima", "cita %d ficha(s) válidas; el mínimo es %d" % (len(valid), fcfg["min_evidence_per_idea"])))
    local = [c for c in valid if is_local(fichas[c].get("geografia"), cfg)]
    if len(local) < fcfg["min_local_evidence"]:
        problems.append(("evidencia_local", "hace falta al menos %d ficha(s) de Uruguay o LATAM" % fcfg["min_local_evidence"]))
    if valid and not any(ficha_estado(fichas[c]) == E.OK for c in valid):
        problems.append(("evidencia_solo_bloqueada", "toda su evidencia viene de URLs bloqueadas: ninguna se pudo abrir"))
    for comp in idea["competidores"]:
        if not any(e in fichas for e in comp["evidencia_ids"]):
            problems.append(("competidor_sin_ficha", "el competidor '%s' no tiene ninguna ficha válida" % comp["nombre"]))
    if page_words is not None and page_words > fcfg["idea_max_words"]:
        problems.append(("palabras", "la página tiene %d palabras; el máximo es %d" % (page_words, fcfg["idea_max_words"])))
    return problems


def blocking(problems):
    """The problems that drop an idea: everything but the warnings."""
    return [(code, msg) for code, msg in problems if code not in WARNING_CODES]


def fatal_codes(problems):
    return sorted(set(code for code, _ in problems if code in FATAL_CODES))


# ---------------------------------------------------------------- the one-page view

def cell(text):
    return re.sub(r"\s+", " ", str(text)).replace("|", "/").strip()


def _usd(x):
    return ("%.2f" % float(x)).rstrip("0").rstrip(".")


def render_page(idea, fichas, cfg, problems=None):
    """(markdown, words in the page body). The evidence table and the automatic check at
    the bottom are built by Python from the verified cards and do not count as words."""
    L = ["# %s" % idea["titulo"], "",
         "**Problema.** %s" % idea["problema"], "",
         "**Usuario.** %s" % idea["usuario"], "",
         "**Solución.** %s" % idea["solucion"], "",
         "## Alcance del MVP", "", "**Semestre 1 (2027)**"]
    L += ["- %s" % x for x in idea["mvp"]["semestre_1"]]
    L += ["", "**Semestre 2 (2027)**"]
    L += ["- %s" % x for x in idea["mvp"]["semestre_2"]]
    L += ["", "## Stack propuesto", "", ", ".join(idea["stack"]), "",
          "## Costo de infraestructura (anual)", "",
          "| Concepto | USD/año | Supuesto | Fuente de precio |", "| --- | --- | --- | --- |"]
    for it in idea["costo_infra"]["items"]:
        L.append("| %s | %s | %s | %s |" % (cell(it["concepto"]), _usd(it["usd_anual"]), cell(it["supuesto"]),
                                          cell(it.get("fuente_precio_url") or "estimación")))
    L += ["", "**Total: USD %s por año** (tope USD %s, objetivo cómodo USD %s)."
          % (_usd(idea["costo_infra"]["total_anual_usd"]), _usd(cfg["infra_budget_usd"]),
             _usd(cfg.get("infra_budget_target_usd", cfg["infra_budget_usd"]))), "",
          "## Competidores", ""]
    if idea["competidores"]:
        L += ["- **%s**: %s (evidencia: %s)" % (c["nombre"], c["hueco"], ", ".join(c["evidencia_ids"]))
              for c in idea["competidores"]]
    else:
        L.append("- Ninguno respaldado por fichas.")
    L += ["", "## Monetización", "", idea["monetizacion"], "", "## Riesgos", ""]
    L += ["- %s" % r for r in idea["riesgos"]]
    L += ["", "## Supuestos declarados (sin evidencia)", ""]
    L += ["- %s" % s for s in idea["supuestos"]] or ["- Ninguno."]
    body = "\n".join(L)
    words = len(re.findall(r"\S+", body))

    T = ["", "---", "", "## Evidencias citadas", "",
         "Armada por Python a partir de las fichas verificadas, no por quien escribió la idea.", "",
         "| ID | Hallazgo | Fuente | Fecha | Geografía | Verificación |", "| --- | --- | --- | --- | --- | --- |"]
    for cid in cited_ids(idea):
        f = fichas.get(cid)
        if not f:
            T.append("| %s | NO EXISTE en las fichas verificadas | | | | |" % cell(cid))
            continue
        ver = f.get("verificacion") or {}
        T.append("| %s | %s | %s (%s) | %s | %s | %s |" % (
            cell(cid), cell(f["hallazgo"]), cell(f["source_title"]), cell(f["source_url"]),
            cell(f["source_date"]), cell(f["geografia"]), cell(ver.get("estado", "?"))))
    T += ["", "## Chequeo automático", ""]
    hard = blocking(problems or [])
    T += ["- %s: %s" % (code, msg) for code, msg in hard]
    if not hard:
        T.append("- Sin problemas: costo dentro del tope, citas existentes y evidencia local.")
    T += ["- Aviso (%s): %s. No descarta la idea: queda a juicio de quien la evalúe si la estimación es razonable."
          % (code, msg) for code, msg in problems or [] if code in WARNING_CODES]
    T.append("- Página: %d palabras (máximo %d)." % (words, cfg["filter"]["idea_max_words"]))
    return body + "\n" + "\n".join(T) + "\n", words
