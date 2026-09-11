# RAG Knowledge Assistant

A Python knowledge retrieval application that uses semantic search to find relevant support documentation.

## Current Functionality

- Loads text documents from a local knowledge base
- Uses a local Sentence Transformers embedding model
- Searches documents by semantic similarity
- Returns the most relevant source documents
- Shows a similarity score for each result
- Uses the retrieval component of a Retrieval-Augmented Generation (RAG) workflow

## Run Locally

```bash
.\.venv\Scripts\python.exe knowledge_assistant.py
```

The semantic model downloads automatically the first time you run the application.

## Example Question

```text
How do I fix an invalid API credential?
```

## Example Result

```text
Source: api_integration_guide.txt
Similarity score: 0.43
```

## Project Structure

```text
rag-knowledge-assistant/
├── documents/
│   ├── api_integration_guide.txt
│   ├── authentication_guide.txt
│   └── reporting_guide.txt
├── .gitignore
├── knowledge_assistant.py
├── README.md
└── requirements.txt
```

## Built With

- Python 3.13
- Sentence Transformers
- Git
- GitHub