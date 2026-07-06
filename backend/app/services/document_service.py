import PyPDF2
import io
from fastapi import UploadFile

async def extract_text_from_pdf(file: UploadFile) -> str:
    content = await file.read()
    pdf = PyPDF2.PdfReader(io.BytesIO(content))
    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""
    return text.strip()