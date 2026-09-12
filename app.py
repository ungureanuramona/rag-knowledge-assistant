from pathlib import Path

import streamlit as st
from sentence_transformers import SentenceTransformer

from knowledge_assistant import (
    EMBEDDING_MODEL_NAME,
    find_relevant_documents,
    generate_answer,
    load_documents,
)


@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(EMBEDDING_MODEL_NAME)


@st.cache_data
def load_knowledge_base():
    project_folder = Path(__file__).parent
    documents_folder = project_folder / "documents"
    return load_documents(documents_folder)


st.set_page_config(
    page_title="RAG Knowledge Assistant",
    page_icon="📚",
)

st.title("📚 RAG Knowledge Assistant")
st.write("Ask a question about the support knowledge base.")

documents = load_knowledge_base()
embedding_model = load_embedding_model()

question = st.text_input(
    "Your question",
    placeholder="For example: What should I do when I get a 401 error?",
)

if st.button("Ask question"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching the knowledge base and generating an answer..."):
            relevant_documents = find_relevant_documents(
                question,
                documents,
                embedding_model,
            )
            answer = generate_answer(question, relevant_documents)

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Relevant source")
        for document in relevant_documents:
            st.write(f"**{document['source']}** — similarity: {document['score']:.2f}")

            with st.expander("View source content"):
                st.text(document["content"])