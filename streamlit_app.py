import streamlit as st
from rag import ask_rag

st.set_page_config(
    page_title="SupplyLens RAG",
    page_icon="📦",
    layout="wide"
)

st.title("📦 SupplyLens RAG")
st.write("Ask questions about Meridian's Supply Chain Review and Procurement Policy.")

question = st.text_input(
    "Enter your question:",
    placeholder="e.g. Who approves a purchase order worth ₹1.4 crore?"
)

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching documents and generating answer..."):
            answer = ask_rag(question)

        st.subheader("Answer")
        st.write(answer)