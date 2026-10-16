"""✏️ ส่วนที่ 3: Retrieval — hybrid search (vector + BM25 แบบ n-gram)"""
import math
import re
from collections import Counter

from core.types import Chunk
from core.utils import cosine, cosine_many  # noqa: F401
from student import settings

_K1, _B = 1.5, 0.75
_TOKEN = re.compile(r"[a-z0-9_]+|[\u0E00-\u0E7F]+")


def _tokens(text: str) -> list[str]:
    toks: list[str] = []
    for m in _TOKEN.finditer(text.lower()):
        s = m.group()
        if "\u0e00" <= s[0] <= "\u0e7f":
            # ภาษาไทยไม่มีช่องว่างคั่นคำ ใช้ bigram + trigram
            if len(s) < 2:
                toks.append(s)
            for n in (2, 3):
                toks.extend(s[i:i + n] for i in range(len(s) - n + 1))
        else:
            toks.append(s)
    return toks


_cache: dict = {}


def _index(chunks: list[Chunk]):
    key = tuple(hash(c.text) for c in chunks)
    if _cache.get("key") == key:
        return _cache["idx"]
    docs = [Counter(_tokens(c.text)) for c in chunks]
    lens = [sum(d.values()) for d in docs]
    avg = (sum(lens) / len(lens)) or 1.0
    df: Counter = Counter()
    for d in docs:
        df.update(d.keys())
    idx = (docs, lens, avg, df)
    _cache["key"], _cache["idx"] = key, idx
    return idx


def _bm25(chunks: list[Chunk], query: str) -> list[float]:
    docs, lens, avg, df = _index(chunks)
    n_docs = len(docs)
    scores = [0.0] * n_docs
    for tok in set(_tokens(query)):
        n = df.get(tok, 0)
        if not n:
            continue
        idf = math.log(1 + (n_docs - n + 0.5) / (n + 0.5))
        for i, d in enumerate(docs):
            f = d.get(tok, 0)
            if f:
                scores[i] += idf * f * (_K1 + 1) / (f + _K1 * (1 - _B + _B * lens[i] / avg))
    return scores


def _norm(xs: list[float]) -> list[float]:
    if not xs:
        return xs
    lo, hi = min(xs), max(xs)
    if hi - lo < 1e-12:
        return [0.0] * len(xs)
    return [(x - lo) / (hi - lo) for x in xs]


def make_query(question: str, options: list[str]) -> str:
    q = (question or "").strip()
    if options and getattr(settings, "QUERY_WITH_OPTIONS", True):
        q = q + "\n" + "\n".join(o.strip() for o in options if o and o.strip())
    return q.strip() or "."


def search(chunks: list[Chunk], query_text: str, query_vector: list[float] | None, k: int) -> list[tuple[Chunk, float]]:
    if not chunks:
        return []
    top_k = int(getattr(settings, "TOP_K", k) or k)
    w = float(getattr(settings, "HYBRID_WEIGHT", 0.5))

    kw = _bm25(chunks, query_text)

    vec = None
    if query_vector is not None and all(c.vector is not None for c in chunks):
        try:
            vec = [float(x) for x in cosine_many(query_vector, [c.vector for c in chunks])]
        except Exception:
            vec = None

    if vec is None:
        final = _norm(kw)
    elif max(kw) <= 0:
        final = _norm(vec)
    else:
        final = [(1 - w) * a + w * b for a, b in zip(_norm(vec), _norm(kw))]

    order = sorted(range(len(chunks)), key=lambda i: final[i], reverse=True)[:top_k]
    return [(chunks[i], float(final[i])) for i in order]