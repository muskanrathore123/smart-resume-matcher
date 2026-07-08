from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from app.core.security import get_current_user  # your auth
from app.services.rag_service import analyze_resume

router = APIRouter(prefix="/api", tags=["rag"])

@router.post("/analyze")
async def analyze(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(None),
    jd_text: str = Form(None),
    # current_user = Depends(get_current_user)
):
    if not resume.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Resume must be a PDF")

    result = await analyze_resume(
        resume_file=resume,
        jd_file_or_text=jd_text or job_description,
        user_id="test_user"

        # user_id=str(current_user.id)

    )
    
    return result