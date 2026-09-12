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
st.caption("Ask questions about the support knowledge base.")

if "messages" not in st.session_state:
    st.session_state.messages = []

documents = load_knowledge_base()
embedding_model = load_embedding_model()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant":
            st.write("**Relevant source:**")

            for document in message["sources"]:
                st.write(
                    f"- {document['source']} "
                    f"(similarity: {document['score']:.2f})"
                )

                with st.expander(f"View {document['source']}"):
                    st.text(document["content"])

question = st.chat_input("Ask a support question")

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the knowledge base and generating an answer..."):
            relevant_documents = find_relevant_documents(
                question,
                documents,
                embedding_model,
            )
            answer = generate_answer(question, relevant_documents)

        st.write(answer)
        st.write("**Relevant source:**")

        for document in relevant_documents:
            st.write(
                f"- {document['source']} "
                f"(similarity: {document['score']:.2f})"
            )

            with st.expander(f"View {document['source']}"):
                st.text(document["content"])

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": relevant_documents,
        }
    )