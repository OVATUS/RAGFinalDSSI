"""✏️ ส่วนที่ 4: Prompt — บอก LLM ว่าจะให้ทำอะไร"""
import re

from student import settings

_MAX_CTX = getattr(settings, "MAX_CONTEXT_CHARS", 6000)

_NEG_PATTERN = re.compile(r"(ไม่|ยกเว้น|ผิด|นอกจาก|ข้อใดเท็จ|เท็จ|not|except|incorrect|false)", re.IGNORECASE)


def _format_context(hits, max_chars: int = _MAX_CTX) -> str:
    """รวมเนื้อหาของ chunk เป็นข้อความอ้างอิง เรียงตามความเกี่ยวข้อง และจำกัดความยาว"""
    if not hits:
        return ""
    parts = []
    used = 0
    for i, hit in enumerate(hits, 1):
        chunk = hit[0] if isinstance(hit, (tuple, list)) else hit
        text = getattr(chunk, "text", str(chunk)).strip()
        doc_id = getattr(chunk, "doc_id", "")
        block = f"[{i}] ({doc_id})\n{text}" if doc_id else f"[{i}]\n{text}"
        if used + len(block) > max_chars:
            remain = max_chars - used
            if remain > 200:
                parts.append(block[:remain])
            break
        parts.append(block)
        used += len(block) + 2
    return "\n\n".join(parts)


def build_mc_prompt(question: str, options: list[tuple[str, str]], hits) -> list[dict]:
    context = _format_context(hits)
    keys = [k for k, _ in options]
    opts_text = "\n".join(f"{k}. {t}" for k, t in options)
    is_negative = bool(_NEG_PATTERN.search(question))

    system = (
        "คุณคือผู้เชี่ยวชาญที่ตอบข้อสอบปรนัยด้านการเขียนโปรแกรมและโครงสร้างข้อมูล\n"
        "กติกา:\n"
        "1. ถ้ามี 'เอกสารอ้างอิง' ให้ยึดเอกสารเป็นหลักในการตอบ แม้ขัดกับความรู้ทั่วไปของคุณ "
        "เพราะเอกสารอาจมีนิยามหรือตัวเลขเฉพาะ\n"
        "2. ถ้าเอกสารไม่ครอบคลุมคำถาม ให้ใช้ความรู้ของคุณตอบ\n"
        "3. ตรวจทุกตัวเลือกเทียบกับเอกสารทีละข้อ แล้วเลือกตัวเลือกที่ดีที่สุดเพียงข้อเดียว\n"
        f"4. ฟิลด์ answer ต้องเป็นหนึ่งใน: {', '.join(keys)} เท่านั้น\n"
        "5. ฟิลด์ reason เขียนเหตุผลสั้น ๆ (1-3 ประโยค) ก่อนสรุปคำตอบ"
    )

    user_parts = []
    if context:
        user_parts.append(f"เอกสารอ้างอิง:\n{context}")
    else:
        user_parts.append("เอกสารอ้างอิง: (ไม่มี ให้ใช้ความรู้ของคุณ)")
    user_parts.append(f"คำถาม:\n{question.strip()}")
    user_parts.append(f"ตัวเลือก:\n{opts_text}")
    if is_negative:
        user_parts.append(
            "⚠️ คำถามนี้เป็นเชิงปฏิเสธ (ถามหาข้อที่ 'ไม่ใช่' / 'ผิด' / 'ยกเว้น') "
            "ให้หาตัวเลือกที่ขัดกับเอกสารหรือไม่เป็นจริง อย่าเลือกข้อที่ถูกต้อง"
        )
    user_parts.append("ตอบเป็น JSON: เหตุผลสั้น ๆ แล้วตามด้วยตัวเลือกที่เลือก")

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": "\n\n".join(user_parts)},
    ]


def build_code_prompt(requirement: str, signature: str | None, entry_point: str | None, hits) -> list[dict]:
    context = _format_context(hits)

    system = (
        "You are an expert Python programmer. You write correct, simple, efficient code "
        "that passes hidden unit tests.\n"
        "Rules:\n"
        "- Use the EXACT function name and signature given. Do not rename or change parameters.\n"
        "- Use only the Python standard library.\n"
        "- The function must RETURN its result. Never print, never call input().\n"
        "- Do not write example usage, tests, or `if __name__ == '__main__'`.\n"
        "- Put any needed imports at the top of the code block.\n"
        "- Read the requirement carefully. If it forbids certain functions or techniques "
        "(e.g. max, sorted, eval, recursion), you MUST NOT use them, or you score zero.\n"
        "- Handle edge cases (empty input, zero, negatives, duplicates) mentioned or implied.\n"
        "- Before answering, mentally check your code against every example in the requirement.\n"
        "- Reply with ONE ```python code block containing the complete function, and nothing else."
    )

    user_parts = []
    if context:
        user_parts.append(f"เอกสารอ้างอิง:\n{context}")
    user_parts.append(f"โจทย์:\n{requirement.strip()}")
    if signature:
        user_parts.append(f"ต้องใช้ signature นี้เป๊ะ ๆ:\n{signature.strip()}")
    if entry_point:
        user_parts.append(f"ชื่อฟังก์ชัน: {entry_point}")
    user_parts.append("ตอบเป็น ```python code block เดียว ที่มีฟังก์ชันสมบูรณ์")

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": "\n\n".join(user_parts)},
    ]