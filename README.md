# RAG Knowledge Assistant

A Python knowledge retrieval application that searches through support documentation and returns the most relevant source files.

## Current Functionality

- Loads text documents from a local knowledge base
- Searches documents using keyword overlap
- Removes common stop words to improve relevance
- Returns the most relevant source document
- Shows a relevance score for each result

## Run Locally

```bash
.\.venv\Scripts\python.exe knowledge_assistant.py
```

## Example Question

```text
Why does the API return a 401 response?
```

## Example Result

```text
Source: api_integration_guide.txt
Relevance score: 3
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
└── README.md
```

## Built With

- Python 3.13
- Git
- GitHub