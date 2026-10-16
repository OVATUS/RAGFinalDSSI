"""✏️ ส่วนที่ 1: Chunking — แบ่งเอกสารเป็นชิ้น (chunk)

เอกสารที่ได้รับเป็น markdown เช่น lecture note หรือ case study ที่มีหัวข้อ (#, ##), ตาราง และ code block
ชิ้นที่แบ่งแล้วจะถูกนำไปทำ embedding และใช้ค้นหาตอนตอบคำถาม
แบ่งดี = ค้นเจอเนื้อหาที่ตรงคำถามและครบถ้วน

ค่าตั้งต้นตอนยังไม่ทำ: ไม่แบ่งเลย ทั้งเอกสารเป็น chunk เดียว
ค่าที่ปรับได้ (CHUNK_SIZE, CHUNK_OVERLAP, ...) อยู่ใน student/settings.py
"""
from student import settings  # noqa: F401


def split(doc_id: str, text: str) -> list[str]:
    """แบ่งเอกสาร 1 ชิ้นเป็น list ของข้อความ

    รับ:  doc_id  ชื่อเอกสาร เช่น "session04_01_prompt_fundamentals"
          text    เนื้อหาทั้งหมดของเอกสาร (markdown)
    คืน:  list[str] ข้อความของแต่ละ chunk (ห้ามว่าง)

    แนวทาง:
      - แยกตามหัวข้อ markdown (บรรทัดที่ขึ้นต้นด้วย #) แล้วใส่ชื่อหัวข้อไว้ต้น chunk ด้วย
      - หัวข้อที่ยาวเกินไปให้ตัดย่อยเป็นช่วง ๆ (เช่น 600–1,000 ตัวอักษร) และซ้อนกันเล็กน้อย (overlap)
      - พยายามอย่าตัดกลางตาราง กลาง code block หรือกลางประโยค
    ตัวอย่าง:
      split("doc1", "# A\\nเนื้อหา A\\n# B\\nเนื้อหา B") -> ["A\\nเนื้อหา A", "B\\nเนื้อหา B"]
    """
    # TODO HERE: Chunking
    pass
