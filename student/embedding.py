"""✏️ ส่วนที่ 2: Embedding — เติม prefix ตามที่ nomic-embed-text ถูกฝึกมา"""
from core.ollama_client import embed
from student import settings

_BATCH = 16


def embed_documents(texts: list[str]) -> list[list[float]]:
    prefix = getattr(settings, "DOC_PREFIX", "search_document: ")
    out: list[list[float]] = []
    for i in range(0, len(texts), _BATCH):
        batch = [prefix + t for t in texts[i:i + _BATCH]]
        out.extend(embed(batch))
    return out


def embed_query(text: str) -> list[float]:
    prefix = getattr(settings, "QUERY_PREFIX", "search_query: ")
    return embed([prefix + text])[0]