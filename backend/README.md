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