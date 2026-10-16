"""✏️ ส่วนที่ 3: Retrieval — ค้นหา chunk ที่เกี่ยวข้องกับคำถาม

ค่าตั้งต้นตอนยังไม่ทำ: ไม่คืน chunk ใดเลย LLM จึงไม่เห็นเอกสาร
"""
from core.types import Chunk
from core.utils import cosine, cosine_many  # noqa: F401 — ตัวช่วยคำนวณความคล้ายของ vector
from student import settings  # noqa: F401 — TOP_K, QUERY_WITH_OPTIONS, HYBRID_WEIGHT, MIN_SCORE


def make_query(question: str, options: list[str]) -> str:
    """สร้างข้อความที่จะใช้ค้นหา

    รับ:  question  คำถาม (หรือ requirement ของโจทย์เขียนโค้ด ซึ่งกรณีนี้ options จะเป็น list ว่าง)
          options   ข้อความของตัวเลือก ก–จ (ไม่มีตัวอักษร key นำหน้า)
    คืน:  สตริงคำค้น (ห้ามว่าง)

    แนวทาง: ลองรวมคำถามกับตัวเลือกเข้าด้วยกัน เพราะคำตอบมักอยู่ในย่อหน้าที่มีคำของตัวเลือก
    """
    # TODO HERE: Retrieval
    pass


def search(chunks: list[Chunk], query_text: str, query_vector: list[float] | None, k: int) -> list[tuple[Chunk, float]]:
    """เลือก chunk ที่เกี่ยวข้องที่สุด k ชิ้น

    รับ:  chunks        chunk ทั้งหมดของเอกสารชุดนี้ (chunk.text, chunk.vector, chunk.doc_id)
          query_text    คำค้น (จาก make_query)
          query_vector  vector ของคำค้น (จาก embedding.embed_query) หรือ None ถ้ายังไม่ได้ทำ embedding
          k             จำนวนที่ระบบแนะนำ (5) จะใช้ settings.TOP_K ของตัวเองแทนก็ได้
    คืน:  list ของ (chunk, score) เรียงจากเกี่ยวข้องมากไปน้อย

    แนวทาง:
      - วิธีพื้นฐาน: scores = cosine_many(query_vector, [c.vector for c in chunks]) แล้วเลือก k ตัวที่คะแนนสูงสุด
      - วิธีที่ดีขึ้น: hybrid search คือรวมคะแนน vector กับคะแนนการจับคำ (keyword / BM25) ช่วยมากกับชื่อเฉพาะและตัวเลข
      - ระวังกรณีที่ chunk.vector หรือ query_vector เป็น None
    """
    # TODO HERE: Retrieval
    pass
