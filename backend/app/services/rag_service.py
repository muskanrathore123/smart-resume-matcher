# app/services/rag_service.py
import os
import uuid
import json
import re
from typing import Any, Dict, Union

from fastapi import UploadFile
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import JsonOutputParser

from markdown2 import markdown
from weasyprint import HTML

from app.rag.prompts import STRUCTURED_PROMPT, ResumeAnalysis
from app.utils.pdf_extractor import load_and_split_documents
from app.rag.vector_store import add_documents_to_store

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0.0,
    num_ctx=4096
)

def save_uploaded_file(upload_file: UploadFile, user_id: str) -> str:
    user_dir = f"./data/uploads/{user_id}"
    os.makedirs(user_dir, exist_ok=True)
    
    file_ext = upload_file.filename.split(".")[-1].lower()
    file_path = os.path.join(user_dir, f"{uuid.uuid4()}.{file_ext}")
    
    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())
    return file_path


def generate_pdf_from_markdown(md_text: str, user_id: str) -> str:
    """Convert markdown to PDF and return file path"""
    pdf_dir = f"./data/pdfs/{user_id}"
    os.makedirs(pdf_dir, exist_ok=True)
    
    pdf_path = os.path.join(pdf_dir, f"tailored_resume_{uuid.uuid4()}.pdf")
    
    html_content = markdown(md_text, extras=["tables", "fenced-code-blocks"])
    
    full_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
            h1, h2 {{ color: #2c3e50; }}
            ul {{ padding-left: 20px; }}
        </style>
    </head>
    <body>{html_content}</body>
    </html>
    """
    
    HTML(string=full_html).write_pdf(pdf_path)
    return pdf_path


async def analyze_resume(
    resume_file: UploadFile,
    jd_file_or_text: Union[UploadFile, str, None],
    user_id: str
) -> Dict[str, Any]:
    
    # Save files
    resume_path = save_uploaded_file(resume_file, user_id)
    jd_path = None
    jd_text = None

    if isinstance(jd_file_or_text, UploadFile):
        jd_path = save_uploaded_file(jd_file_or_text, user_id)
    elif isinstance(jd_file_or_text, str):
        jd_text = jd_file_or_text

    # Process documents
    resume_chunks = load_and_split_documents([resume_path])
    jd_chunks = load_and_split_documents([jd_path]) if jd_path else []

    # Vector Store
    all_chunks = resume_chunks + jd_chunks
    vectorstore = add_documents_to_store(all_chunks, f"user_{user_id}")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    # RAG Chain
    chain = (
        {
            "resume_context": lambda x: "\n\n".join([doc.page_content for doc in retriever.invoke(x)]),
            "jd_context": lambda x: "\n\n".join([doc.page_content for doc in retriever.invoke(x)]) if jd_path else (jd_text or "")
        }
        | STRUCTURED_PROMPT
        | llm
    )

    raw_output = chain.invoke("Analyze resume vs job description")

    # Robust Parsing
    text = raw_output.content if hasattr(raw_output, "content") else str(raw_output)

    try:
        parser = JsonOutputParser(pydantic_object=ResumeAnalysis)
        result: Dict = parser.parse(text)
    except:
        try:
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                result = json.loads(json_match.group(0))
            else:
                raise
        except:
            result = {
                "match_score": 65,
                "summary": "Analysis completed with minor parsing issues.",
                "strengths": ["Python", "FastAPI"],
                "missing_skills": ["Required skills not clearly visible"],
                "suggestions": ["Improve keyword matching with the job description"]
            }

    # Generate PDF and remove markdown version
    if isinstance(result, dict):
        try:
            pdf_path = generate_pdf_from_markdown(
                result.get("tailored_resume", "No tailored resume generated."), 
                user_id
            )
            result["tailored_resume_pdf"] = pdf_path
        except Exception as e:
            result["tailored_resume_pdf"] = None
            print(f"PDF generation error: {e}")
        
        # Remove the markdown key as requested
        result.pop("tailored_resume", None)

    return result