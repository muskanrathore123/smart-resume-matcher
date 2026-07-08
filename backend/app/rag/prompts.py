# app/rag/prompts.py
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List

class ResumeAnalysis(BaseModel):
    match_score: int = Field(..., ge=0, le=100)
    summary: str
    strengths: List[str]
    missing_skills: List[str]
    suggestions: List[str]
    tailored_resume: str

# Much stronger prompt
STRUCTURED_PROMPT = ChatPromptTemplate.from_template("""
You are an expert recruiter. Analyze the resume vs job description and **return ONLY valid JSON**, nothing else.

**Resume:**
{resume_context}

**Job Description:**
{jd_context}

Respond with this exact JSON format (no explanation, no markdown, no extra text):

{{
  "match_score": 82,
  "summary": "Good technical fit with gaps in cloud technologies.",
  "strengths": ["Python", "FastAPI", "REST APIs", "PostgreSQL"],
  "missing_skills": ["Advanced AWS", "ChromaDB"],
  "suggestions": ["Add AWS project examples", "Mention Docker Compose experience"],
  "tailored_resume": "Full markdown resume here..."
}}

Be concise and accurate.
""")