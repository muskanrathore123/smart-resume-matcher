from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.models.user import User
from app.api.v1.auth import router as auth_router
from app.api.v1.rag import router as rag_router
from fastapi.staticfiles import StaticFiles
import os

# when system server start our system first try to connect with db. All tables that created inside the local they create into db
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Resume Matcher API")

'''
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
# Mount static files
os.makedirs("./data/pdfs", exist_ok=True)
app.mount("/data", StaticFiles(directory="data"), name="data")

# Include routers
app.include_router(auth_router)
app.include_router(rag_router)


@app.get("/")
def root():
    return {"message": "Smart Resume Matcher Backend is running!"}
