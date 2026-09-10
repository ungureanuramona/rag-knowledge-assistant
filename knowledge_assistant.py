import re
from pathlib import Path


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "about",
    "does",
    "for",
    "how",
    "i",
    "in",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "what",
    "why",
    "with",
}


def tokenize(text):
    words = re.findall(r"\b\w+\b", text.lower())
    return {word for word in words if word not in STOP_WORDS}


def load_documents(documents_folder):
    documents = []

    for file_path in documents_folder.glob("*.txt"):
        documents.append(
            {
                "source": file_path.name,
                "content": file_path.read_text(encoding="utf-8"),
            }
        )

    return documents


def find_relevant_documents(question, documents, limit=2):
    question_words = tokenize(question)
    scored_documents = []

    for document in documents:
        document_words = tokenize(document["content"])
        score = len(question_words.intersection(document_words))

        if score > 0:
            scored_documents.append(
                {
                    "source": document["source"],
                    "content": document["content"],
                    "score": score,
                }
            )

    scored_documents.sort(key=lambda document: document["score"], reverse=True)

    return scored_documents[:limit]


def main():
    project_folder = Path(__file__).parent
    documents_folder = project_folder / "documents"
    documents = load_documents(documents_folder)

    question = input("Ask a question about the knowledge base: ")

    if not question.strip():
        print("Please enter a question.")
        return

    results = find_relevant_documents(question, documents)

    if not results:
        print("\nNo relevant documents found.")
        return

    print("\n--- Relevant Sources ---")

    for result in results:
        print(f"\nSource: {result['source']}")
        print(f"Relevance score: {result['score']}")
        print(result["content"])


if __name__ == "__main__":
    main()