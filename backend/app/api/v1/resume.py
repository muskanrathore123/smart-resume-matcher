# Resume upload & parsing
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.resume import Resume
from app.services.document_service import extract_text_from_pdf

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    # user_id: int = Depends(get_current_user)  # Add later
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only PDF files allowed")

    text = await extract_text_from_pdf(file)

    resume = Resume(
        filename=file.filename,
        raw_text=text,
        # user_id=user_id,
        parsed_skills="[]"  # TODO: extract skills later
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {"id": resume.id, "filename": resume.filename, "message": "Resume uploaded successfully"}