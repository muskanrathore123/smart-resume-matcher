from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String, nullable=False)
    raw_text = Column(Text)
    parsed_skills = Column(Text)   # JSON string of skills
    created_at = Column(DateTime(timezone=True), server_default=func.now())