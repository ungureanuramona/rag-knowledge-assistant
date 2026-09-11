from pathlib import Path

from sentence_transformers import SentenceTransformer, util


MODEL_NAME = "all-MiniLM-L6-v2"


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


def find_relevant_documents(question, documents, model, limit=2):
    document_texts = [document["content"] for document in documents]

    question_embedding = model.encode(question, convert_to_tensor=True)
    document_embeddings = model.encode(document_texts, convert_to_tensor=True)

    similarity_scores = util.cos_sim(question_embedding, document_embeddings)[0]

    scored_documents = []

    for index, score in enumerate(similarity_scores):
        scored_documents.append(
            {
                "source": documents[index]["source"],
                "content": documents[index]["content"],
                "score": float(score),
            }
        )

    scored_documents.sort(key=lambda document: document["score"], reverse=True)

    return scored_documents[:limit]


def main():
    project_folder = Path(__file__).parent
    documents_folder = project_folder / "documents"
    documents = load_documents(documents_folder)

    print("Loading the semantic search model...")
    model = SentenceTransformer(MODEL_NAME)

    question = input("\nAsk a question about the knowledge base: ")

    if not question.strip():
        print("Please enter a question.")
        return

    results = find_relevant_documents(question, documents, model)

    print("\n--- Relevant Sources ---")

    for result in results:
        print(f"\nSource: {result['source']}")
        print(f"Similarity score: {result['score']:.2f}")
        print(result["content"])


if __name__ == "__main__":
    main()