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

# Stronger prompt with strict context-only rule
STRUCTURED_PROMPT = ChatPromptTemplate.from_template("""
You are an expert recruiter. Analyze the resume **strictly based on the provided context only**.

**Rules:**
- Use ONLY information present in the Resume and Job Description below.
- Always generate a **full tailored resume** in clean Markdown format.
- Improve the original resume by highlighting transferable skills and adding keywords from the JD.
- Even if the match is low, create an improved version of the resume.
- Do NOT use your own knowledge or make assumptions.
- Return ONLY valid JSON. No explanations, no markdown, no extra text.

**Resume Context:**
<resume_context>
{resume_context}
</resume_context>

**Job Description Context:**
<jd_context>
{jd_context}
</jd_context>

Respond with this exact JSON format:

{{
  "match_score": 82,
  "summary": "Good technical fit with gaps in cloud technologies.",
  "strengths": ["Python", "FastAPI", "REST APIs", "PostgreSQL"],
  "missing_skills": ["Advanced AWS", "ChromaDB"],
  "suggestions": ["Add AWS project examples", "Mention Docker Compose experience"],
  "tailored_resume": "Full markdown resume here..."
}}

Be concise, factual, and strictly follow the context.
""")