# RAG Knowledge Assistant

A local Python application that answers support questions using a small knowledge base of documents.

The application finds the most relevant document with semantic search, then uses a local LLM to generate an answer grounded in that source.

## Features

- Loads `.txt` knowledge-base documents
- Uses semantic search with Sentence Transformers
- Shows the most relevant source document and similarity score
- Generates answers with a local Ollama model (`gemma3:4b`)
- Includes source grounding in generated answers
- Provides a browser interface with Streamlit
- Uses fictional support documentation only

## Example

```text
Question: What should I do when I get a 401 error from the Orders API?

Answer:
The API key is missing or invalid. Source: api_integration_guide.txt
```

## Project Structure

```text
rag-knowledge-assistant/
├── documents/
│   ├── api_integration_guide.txt
│   ├── authentication_guide.txt
│   └── reporting_guide.txt
├── app.py
├── knowledge_assistant.py
└── requirements.txt
```

## Run Locally

### 1. Create and install the Python environment

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 2. Start Ollama with Docker

Docker Desktop must be running.

```powershell
docker start ollama
```

If the container does not exist yet:

```powershell
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### 3. Download the local model

```powershell
docker exec -it ollama ollama pull gemma3:4b
```

### 4. Run the browser interface

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open `http://localhost:8501` if the browser does not open automatically.

## Tech Stack

- Python
- Streamlit
- Sentence Transformers
- Ollama
- Gemma 3 4B
- Docker
- Git and GitHub