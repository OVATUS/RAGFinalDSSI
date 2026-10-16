"""✏️ ส่วนที่ 1: Chunking — แบ่งตามหัวข้อ markdown แล้วตัดย่อย"""
import re

from student import settings

_SIZE = int(getattr(settings, "CHUNK_SIZE", 900))
_OVERLAP = int(getattr(settings, "CHUNK_OVERLAP", 120))
_MIN_CHUNK = 150

_HEAD = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_FENCE = re.compile(r"^\s*(```|~~~)")


def _sections(text: str):
    """แยกเอกสารเป็น [(titles, blocks)] โดย block คือย่อหน้า / ตาราง / code block ที่ไม่ควรตัดกลาง"""
    sections = []
    stack = []  # (level, title)
    blocks = []
    buf = []
    kind = "text"
    in_code = False

    def flush():
        nonlocal buf
        if buf:
            b = "\n".join(buf).strip("\n")
            if b.strip():
                blocks.append(b)
        buf = []

    def close_section():
        nonlocal blocks
        flush()
        if blocks:
            sections.append((tuple(t for _, t in stack), blocks))
        blocks = []

    for line in text.replace("\r\n", "\n").split("\n"):
        if _FENCE.match(line):
            if not in_code:
                flush()
                in_code = True
                buf = [line]
            else:
                buf.append(line)
                in_code = False
                flush()
                kind = "text"
            continue
        if in_code:
            buf.append(line)
            continue
        m = _HEAD.match(line)
        if m:
            close_section()
            level = len(m.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, m.group(2).strip()))
            continue
        if not line.strip():
            flush()
            continue
        new_kind = "table" if line.lstrip().startswith("|") else "text"
        if buf and kind != new_kind:
            flush()
        kind = new_kind
        buf.append(line)
    close_section()
    return sections


def _split_long(text: str, limit: int) -> list[str]:
    """ตัด block ที่ยาวเกิน limit โดยตัดตามบรรทัด/ประโยค และซ้อนกันเล็กน้อย"""
    overlap = min(_OVERLAP, limit // 3)
    if "\n" in text:
        units, sep = text.split("\n"), "\n"
    else:
        units = [u for u in re.split(r"(?<=[.!?。])\s+|\s{2,}", text) if u]
        sep = " "
    flat = []
    for u in units:
        while len(u) > limit:  # ภาษาไทยที่ไม่มีช่องว่าง
            flat.append(u[:limit])
            u = u[limit:]
        flat.append(u)

    pieces, cur, size = [], [], 0
    for u in flat:
        add = len(u) + len(sep)
        if cur and size + add > limit:
            pieces.append(sep.join(cur))
            tail, t = [], 0
            for x in reversed(cur):
                if t + len(x) + len(sep) > overlap:
                    break
                tail.insert(0, x)
                t += len(x) + len(sep)
            cur, size = tail, t
        cur.append(u)
        size += add
    if cur:
        pieces.append(sep.join(cur))
    return [p for p in pieces if p.strip()]


def _pack(titles, blocks) -> list[str]:
    header = " > ".join(titles)
    limit = max(300, _SIZE - len(header) - 1)
    out, cur = [], ""
    for b in blocks:
        pieces = [b] if len(b) <= limit else _split_long(b, limit)
        for p in pieces:
            if cur and len(cur) + 2 + len(p) > limit:
                out.append(cur)
                cur = p
            else:
                cur = f"{cur}\n\n{p}" if cur else p
    if cur:
        out.append(cur)
    return [f"{header}\n{c}" if header else c for c in out]


def split(doc_id: str, text: str) -> list[str]:
    chunks: list[str] = []
    for titles, blocks in _sections(text):
        chunks.extend(_pack(titles, blocks))

    # รวม chunk ที่สั้นเกินไปเข้ากับชิ้นถัดไป
    merged, carry = [], ""
    for c in chunks:
        if carry:
            if len(carry) + len(c) + 2 <= _SIZE * 1.3:
                c = carry + "\n\n" + c
            else:
                merged.append(carry)
            carry = ""
        if len(c) < _MIN_CHUNK:
            carry = c
        else:
            merged.append(c)
    if carry:
        merged.append(carry)

    merged = [c.strip() for c in merged if c.strip()]
    if not merged and text.strip():
        merged = _pack((), [text.strip()])
    return merged