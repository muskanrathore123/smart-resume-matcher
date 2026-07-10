# database configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# we need to connect base with main.py
Base = declarative_base()
#Using check_same_thread=False allows FastAPI to use the same SQLite database in different threads.
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# here we create db provider when we have requirement so we get the  session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()