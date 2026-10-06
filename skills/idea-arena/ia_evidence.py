"""ia_evidence.py: URL checks, text clean-up and near-duplicate detection for /idea-arena.

Nothing in here calls a model. The URL check is plain HTTP with urllib: it is how the
pipeline enforces "only URLs that really open count".

Python 3.8+, standard library only.
"""
import html
import http.client
import http.cookiejar
import json
import os
import re
import socket
import ssl
import time
import unicodedata
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

EM_DASH, EN_DASH = chr(0x2014), chr(0x2013)   # spelled as code points so this file stays clean

OK, BLOCKED, DEAD = "ok", "bloqueada", "muerta"
DEAD_CODES = (404, 410)   # the only answers that say the page is not there; any other error is a server refusing a script
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/126.0 Safari/537.36 idea-arena-url-check")
MAX_BYTES = 3 * 1024 * 1024
TEST_FETCH_ENV = "IDEA_ARENA_TEST_FETCH"   # tests only: a JSON file of canned URL results


# ---------------------------------------------------------------- text

def sanitize_text(text):
    """Swap the two dash characters the repo's tests forbid for a plain hyphen."""
    return text.replace(EM_DASH, "-").replace(EN_DASH, "-")


def sanitize_obj(obj):
    if isinstance(obj, str):
        return sanitize_text(obj)
    if isinstance(obj, list):
        return [sanitize_obj(x) for x in obj]
    if isinstance(obj, dict):
        return {(sanitize_text(k) if isinstance(k, str) else k): sanitize_obj(v) for k, v in obj.items()}
    return obj


def sweep_dashes(top):
    """Rewrite every UTF-8 text file under top that holds a forbidden dash. Returns the paths changed.
    Line endings are kept exactly as the writer left them."""
    changed = []
    for root, dirs, files in os.walk(top):
        dirs.sort()
        for name in sorted(files):
            path = os.path.join(root, name)
            try:
                with open(path, encoding="utf-8", newline="") as fh:
                    text = fh.read()
            except (UnicodeDecodeError, OSError):
                continue
            if EM_DASH in text or EN_DASH in text:
                with open(path, "w", encoding="utf-8", newline="") as fh:
                    fh.write(sanitize_text(text))
                changed.append(path)
    return changed


def fold(text):
    """Lower case, no accents, single spaces."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", text.lower()).strip()


def _alnum(text):
    return re.sub(r"[^a-z0-9]+", " ", fold(text)).strip()


_TAG_RE = re.compile(r"<(script|style|noscript)\b.*?</\1\s*>|<[^>]+>", re.S | re.I)


def html_to_text(raw):
    return html.unescape(_TAG_RE.sub(" ", raw))


def excerpt_found(excerpt, page_text):
    """True when the excerpt appears in the page, ignoring case, accents, punctuation and spacing."""
    e = _alnum(excerpt)
    return bool(e) and e in _alnum(html_to_text(page_text))


# ---------------------------------------------------------------- urls

_URL_RE = re.compile(r"^https?://[^\s/$.?#][^\s]*$", re.I)


def is_url(s):
    return isinstance(s, str) and bool(_URL_RE.match(s.strip()))


def fetch_url(url, timeout=15):
    """(status, http_code, text). status is ok, bloqueada or muerta.

    muerta means the page cannot exist as cited: 404 or 410, a domain that does not
    resolve, a refused connection. bloqueada means a server answered but would not let a
    script read the page: any other 4xx (400 and 403 included), 5xx, a redirect loop, a
    timeout, a broken certificate. Cookies are kept across redirects, because some sites
    (Google's docs among them) redirect to themselves until the client stores one."""
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-UY,es;q=0.9,en;q=0.5",
    })
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    try:
        with opener.open(req, timeout=timeout) as resp:
            code = resp.getcode()
            body = resp.read(MAX_BYTES)
            ctype = (resp.headers.get("Content-Type") or "").lower()
            charset = resp.headers.get_content_charset() or "utf-8"
            text = "" if "pdf" in ctype else body.decode(charset, errors="replace")
            return OK, code, text
    except urllib.error.HTTPError as e:
        e.close()
        return (DEAD if e.code in DEAD_CODES else BLOCKED), e.code, None
    except urllib.error.URLError as e:
        reason = e.reason
        if isinstance(reason, (socket.gaierror, ConnectionRefusedError)):
            return DEAD, None, None
        return BLOCKED, None, None
    except ValueError:
        return DEAD, None, None
    except (socket.timeout, ssl.SSLError, ConnectionError, http.client.HTTPException, OSError):
        return BLOCKED, None, None


def _test_fetcher():
    path = os.environ.get(TEST_FETCH_ENV)
    if not path:
        return None
    with open(path, encoding="utf-8") as fh:
        table = json.load(fh)
    default = table.get("*", {"status": DEAD})

    def fetch(url, timeout=None):
        r = table.get(url, default)
        return r.get("status", DEAD), r.get("code"), r.get("text")
    return fetch


def check_urls(urls, fetcher=None, timeout=15, workers=8):
    """{url: {"estado", "http", "texto"}} for every distinct URL. A bare timeout is retried once."""
    real = fetcher is None
    fetcher = fetcher or _test_fetcher() or fetch_url

    def one(u):
        st, code, text = fetcher(u, timeout)
        if real and st == BLOCKED and code is None:
            time.sleep(1)
            st, code, text = fetcher(u, timeout)
        return u, st, code, text

    uniq = sorted(set(u for u in urls if u))
    if not uniq:
        return {}
    with ThreadPoolExecutor(max_workers=max(1, min(workers, len(uniq)))) as ex:
        done = list(ex.map(one, uniq))
    return {u: {"estado": st, "http": code, "texto": text} for u, st, code, text in done}


# ---------------------------------------------------------------- near duplicates

STOPWORDS = frozenset("""
a al algo algun alguna algunas algunos ante antes aqui asi aun bajo bien cada como con contra
cual cuales cuando de del desde donde dos el ella ellas ellos en entre era es esa esas ese eso
esos esta estas este esto estos fue han hace hacia hasta hay la las le les lo los mas me mi muy
no nos o otra otras otro otros para pero poco por porque que quien se segun ser si sin sino sobre
son su sus tambien tan tanto te tiene tienen todo todos tu un una uno unos y ya
""".split())


def tokens(text):
    return [t for t in re.findall(r"[a-z0-9]+", fold(text)) if len(t) > 2 and t not in STOPWORDS]


def _jaccard(a, b):
    if not a and not b:
        return 0.0
    return len(a & b) / float(len(a | b))


def similarity(text_a, text_b):
    """0 to 1: the mean of word and word-pair Jaccard overlap."""
    ta, tb = tokens(text_a), tokens(text_b)
    uni = _jaccard(set(ta), set(tb))
    bi = _jaccard(set(zip(ta, ta[1:])), set(zip(tb, tb[1:])))
    return round((uni + bi) / 2.0, 4)


def overlap(ids_a, ids_b):
    """0 to 1: Jaccard overlap of two lists of evidence ids. Ideas whose problems rest on mostly
    the same cards attack the same problem, even when their products differ."""
    return round(_jaccard(set(ids_a), set(ids_b)), 4)


def idea_text(idea):
    return " ".join(str(idea.get(k) or "") for k in ("titulo", "usuario", "problema", "solucion"))


def clusters(texts, threshold, extra_groups=(), sim=similarity):
    """Group ids whose texts are at least threshold similar, plus any extra groups, transitively.
    texts is {id: text}, or {id: whatever sim takes}. Returns (sorted groups, [(a, b, similarity)]
    for the linked pairs)."""
    ids = sorted(texts)
    parent = {i: i for i in ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def join(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    links = []
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            s = sim(texts[a], texts[b])
            if s >= threshold:
                links.append((a, b, s))
                join(a, b)
    for g in extra_groups:
        g = [x for x in g if x in parent]
        for x in g[1:]:
            join(g[0], x)
    groups = {}
    for i in ids:
        groups.setdefault(find(i), []).append(i)
    return sorted(sorted(g) for g in groups.values()), links
