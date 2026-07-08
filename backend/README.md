<!-- In config.py -->
In which i have created a class "Setting" in which i configure DATABASE_URL, ACCESS_TOKEN_EXPIRE_MINTUES and other things

<!-- In database.py -->
I completed the database configuration. Here we define database provider if we have requirement so we get the  session from there. 
we need to connect database with main.py. 

<!-- main.py -->
# Base.metadata.create_all(bind=engine)
when system server start our system first try to connect with db. All tables that created inside the local they create into db

<!-- user.py -->
In user.py file i have created the User model and  added it into main.py

# Note: everything that we create inside the application we need to define inside the main.py because python run the whole application by using main.py

<!--  "email": "muskan123@gmail.com",
    "password": "sdfghjkl@123", -->

 
# If you want to use Llama 3 locally, install Ollama.
- install: sudo snap install ollama
- version: ollama --version
- start ollama server : ollama serve

# Download llama 3 model
- ollama pull llama3
- ollama list

# Test the model
ollama run llama3

# pdf_extractor.py
This code is part of the document ingestion stage of a RAG (Retrieval-Augmented Generation) pipeline. Its job is to:

- Read PDF files.
- Extract their text.
- Split the text into smaller chunks.
- Return those chunks so they can later be converted into embeddings and stored in a vector database

# vector_store.py
This code creates and manages a Chroma vector database for a RAG (Retrieval-Augmented Generation) application. Its purpose is to convert documents into embeddings, store them in a vector database, and later retrieve similar documents based on user queries.



# Smart Resume Matcher - Project Setup Guide

## Project Overview

Smart Resume Matcher is an AI-powered application that compares a candidate's resume with a job description using Retrieval-Augmented Generation (RAG).

Tech Stack:
- FastAPI
- LangChain
- ChromaDB
- Ollama
- Llama 3.2
- Nomic Embed Text
- PyMuPDF
- SQLite
- JWT Authentication

---

# 1. Prerequisites

Install the following software before running the project.

## Python

Recommended Version

```
Python 3.12+
```

Verify

```bash
python3 --version
```

---

## Git

Install Git.

Verify

```bash
git --version
```

---

## VS Code

Recommended Extensions

- Python
- Pylance
- Black Formatter
- Thunder Client (optional)
- Docker (optional)

---

# 2. Clone Repository

```bash
git clone <repository-url>

cd smart-resume-matcher/backend
```

---

# 3. Create Virtual Environment

Linux / macOS

```bash
python3 -m venv venv
```

Activate

```bash
source venv/bin/activate
```

Windows

```cmd
python -m venv venv

venv\Scripts\activate
```

---

# 4. Install Python Packages

Install all dependencies

```bash
pip install -r requirements.txt
```

If requirements.txt does not exist

```bash
pip install fastapi
pip install uvicorn
pip install python-multipart
pip install langchain
pip install langchain-core
pip install langchain-community
pip install langchain-chroma
pip install langchain-ollama
pip install chromadb
pip install pymupdf
pip install pydantic
pip install python-jose
pip install passlib[bcrypt]
pip install bcrypt
```

Generate requirements later

```bash
pip freeze > requirements.txt
```

---

# 5. Install Ollama

Download from

https://ollama.com/download

Verify

```bash
ollama --version
```

---

# 6. Start Ollama

```bash
ollama serve
```

---

# 7. Download Required Models

LLM

```bash
ollama pull llama3.2:3b
```

Embedding Model

```bash
ollama pull nomic-embed-text
```

Verify

```bash
ollama list
```

Expected Output

```
NAME

llama3.2:3b

nomic-embed-text
```

---

# 8. Project Folder Structure

```
backend/

│

├── app/

│ ├── api/

│ ├── core/

│ ├── rag/

│ ├── services/

│ ├── utils/

│

├── chroma_db/

├── data/

│ └── uploads/

├── requirements.txt

├── .env

└── main.py
```

---

# 9. Environment Variables

Create a .env file

Example

```env
SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

# 10. Run FastAPI

```bash
uvicorn app.main:app --reload
```

Expected

```
INFO: Application startup complete.
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

# 11. API Testing

POST

```
http://127.0.0.1:8000/api/analyze
```

Body → form-data

Resume

```
Key

resume

Type

File
```

Job Description

Either

```
jd_text

Type

Text
```

or

```
job_description

Type

File
```

Authorization

```
Bearer Token
```

(if authentication is enabled)

---

# 12. How RAG Works

User uploads

Resume

↓

Resume saved

↓

Extract PDF text

↓

Split into chunks

↓

Generate embeddings using

nomic-embed-text

↓

Store in ChromaDB

↓

User asks for analysis

↓

Retriever fetches relevant chunks

↓

Prompt + Resume + JD

↓

Llama 3.2

↓

JSON Response

---

# 13. Models Used

LLM

```
llama3.2:3b
```

Purpose

Resume analysis

Embedding Model

```
nomic-embed-text
```

Purpose

Generate vector embeddings

---

# 14. Python Packages Used

Backend

- FastAPI
- Uvicorn
- python-multipart

Authentication

- python-jose
- passlib
- bcrypt

RAG

- langchain
- langchain-core
- langchain-community
- langchain-chroma
- langchain-ollama

Vector Database

- chromadb

PDF

- pymupdf

Validation

- pydantic

---

# 15. Database

Current

SQLite

Used For

- Users
- Authentication

Vector Database

ChromaDB

Stores

- Resume chunks
- Job description chunks
- Embeddings
- Metadata

---

# 16. Generated Folders

Created Automatically

```
backend/chroma_db/
```

```
backend/data/uploads/
```

Do NOT commit these folders.

---

# 17. .gitignore

```gitignore
venv/

__pycache__/

*.pyc

.env

backend/chroma_db/

backend/data/uploads/

*.sqlite3

*.db

.vscode/
```

---

# 18. Common Errors

### Model not found

```
model "nomic-embed-text" not found
```

Solution

```bash
ollama pull nomic-embed-text
```

---

### Ollama Connection Error

```
Connection refused
```

Start Ollama

```bash
ollama serve
```

---

### 401 Unauthorized

Add Bearer Token.

---

### Resume must be PDF

Upload only PDF.

---

### ChromaDB Error

Delete

```
backend/chroma_db
```

Restart application.

---

### PDF Extraction Error

Install

```bash
pip install pymupdf
```

---

# 19. Updating Dependencies

Whenever new packages are installed

```bash
pip freeze > requirements.txt
```

Commit

```
requirements.txt
```

---

# 20. Files to Commit

Commit

```
app/

requirements.txt

README.md

.gitignore

.env.example
```

Do NOT Commit

```
venv/

backend/chroma_db/

backend/data/uploads/

*.db

*.sqlite3

__pycache__/
```

---

# 21. Setup on New Machine

Clone project

↓

Create virtual environment

↓

Activate environment

↓

Install requirements

↓

Install Ollama

↓

Pull models

↓

Create .env

↓

Start Ollama

↓

Run FastAPI

↓

Open Swagger

↓

Test API

Project Ready.