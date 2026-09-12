from pathlib import Path

from ollama import chat
from sentence_transformers import SentenceTransformer, util


EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
LLM_MODEL_NAME = "gemma3:4b"


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


def find_relevant_documents(question, documents, model, limit=1):
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


def generate_answer(question, relevant_documents):
    context = "\n\n".join(
        [
            f"Source: {document['source']}\n{document['content']}"
            for document in relevant_documents
        ]
    )

    response = chat(
        model=LLM_MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a support knowledge assistant. "
                    "Answer the user's question using only the provided context. "
                    "Give a concise and helpful answer. "
                    "Mention the source filename you used. "
                    "Only say that the answer is unavailable if the context is empty "
                    "or does not contain any relevant information."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ],
        options={"temperature": 0},
    )

    return response.message.content


def main():
    project_folder = Path(__file__).parent
    documents_folder = project_folder / "documents"
    documents = load_documents(documents_folder)

    print("Loading the semantic search model...")
    embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    question = input("\nAsk a question about the knowledge base: ")

    if not question.strip():
        print("Please enter a question.")
        return

    relevant_documents = find_relevant_documents(
        question,
        documents,
        embedding_model,
    )

    print("\n--- Relevant Sources ---")

    for document in relevant_documents:
        print(f"- {document['source']} ({document['score']:.2f})")

    print("\n--- Generated Answer ---")
    answer = generate_answer(question, relevant_documents)
    print(answer)


if __name__ == "__main__":
    main()