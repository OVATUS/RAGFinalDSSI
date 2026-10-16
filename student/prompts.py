"""✏️ ส่วนที่ 4: Prompt — บอก LLM ว่าจะให้ทำอะไร

คืนค่าเป็น list ของ message แบบ chat:
    [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
(หรือคืนเป็นสตริงก็ได้ ระบบจะถือว่าเป็นข้อความของ user)

hits คือผลจาก retrieval.search เป็น list ของ (chunk, score) อ่านเนื้อหาได้จาก chunk.text และ chunk.doc_id

ค่าตั้งต้นตอนยังไม่ทำ: ไม่เรียก LLM เลย ข้อสอบปรนัยตอบ "ก" ทุกข้อ และโจทย์โค้ดได้ฟังก์ชันว่างที่ raise NotImplementedError
(ทำส่วนนี้ก่อน เพราะถ้ายังไม่ทำ ส่วนอื่นจะไม่มีผลต่อคะแนนเลย)
"""
from student import settings  # noqa: F401 — MAX_CONTEXT_CHARS


def build_mc_prompt(question: str, options: list[tuple[str, str]], hits) -> list[dict]:
    """prompt สำหรับข้อสอบปรนัย

    รับ:  question  คำถาม
          options   list ของ (key, text) เช่น [("ก", "O(1)"), ("ข", "O(log n)"), ...]
          hits      chunk ที่ค้นได้ (list ของ (chunk, score)) อาจเป็น list ว่าง
    คืน:  list ของ message

    หมายเหตุ: core บังคับให้ LLM ตอบเป็น JSON {"reason": "...", "answer": "<key>"} ให้อยู่แล้ว
    แนวทาง:
      - ใส่เนื้อหาของ hits เป็น "เอกสารอ้างอิง" แล้วสั่งให้ยึดเอกสารเป็นหลัก แม้จะขัดกับความรู้ทั่วไป
      - แสดงตัวเลือกพร้อม key (ก. ... ข. ...)
      - ระวังคำถามเชิงปฏิเสธ เช่น "ข้อใด**ไม่**ถูกต้อง"
    """
    # TODO HERE: Prompt
    pass


def build_code_prompt(requirement: str, signature: str | None, entry_point: str | None, hits) -> list[dict]:
    """prompt สำหรับโจทย์เขียนโปรแกรม

    รับ:  requirement  โจทย์ (ภาษาไทย)
          signature    บรรทัด def ที่ต้องใช้ เช่น "def is_prime(n: int) -> bool:"
          entry_point  ชื่อฟังก์ชัน เช่น "is_prime"
          hits         chunk ที่ค้นได้ (มีเฉพาะโจทย์ที่อ้างถึงเอกสาร ส่วนใหญ่จะเป็น list ว่าง)
    คืน:  list ของ message

    หมายเหตุ: core ดึงโค้ดจาก ```python ... ``` ในคำตอบให้ และถ้า compile ไม่ผ่านจะขอให้ LLM แก้ให้อีก 1 รอบ
    แนวทาง:
      - สั่งให้ใช้ชื่อฟังก์ชันและ signature ตามที่ให้มาเป๊ะ ๆ และใช้เฉพาะ Python standard library
      - ห้าม print หรือรับ input เอง ให้ return ค่า
      - อ่านโจทย์ให้ดี บางข้อ "ห้ามใช้" ฟังก์ชันบางตัว (เช่น max, sorted, eval) ถ้าใช้จะได้ 0 ทั้งข้อ
      - ให้ตอบเป็น code block เดียว
    """
    # TODO HERE: Prompt
    pass
