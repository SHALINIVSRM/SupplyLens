# SupplyLens

### AI-Powered Supply Chain Document Intelligence using RAG

SupplyLens is a Retrieval-Augmented Generation (RAG) application that allows users to ask questions about procurement and supply-chain documents and receive grounded answers based on the information contained in those documents.

The system retrieves relevant passages from the indexed documents using semantic search and then uses Groq's LLM to generate a concise answer based only on the retrieved context.

---

## 🚀 Features

- 📄 PDF document processing
- ✂️ Document chunking
- 🧠 Semantic embeddings using Sentence Transformers
- 🔎 Similarity-based document retrieval
- 🗄️ ChromaDB vector database
- 🤖 Groq LLM for answer generation
- 🛡️ Grounded responses to reduce hallucination
- 💬 Interactive Streamlit interface
- ⚡ Suggested questions for quick testing
- 📊 Visual RAG pipeline
- 🔐 API key stored using environment variables

---

## 🏗️ RAG Architecture

```text
PDF Documents
      ↓
Text Extraction
      ↓
Chunking
      ↓
Sentence Transformers
      ↓
ChromaDB
      ↓
Semantic Retrieval
      ↓
Relevant Context
      ↓
Groq LLM
      ↓
Grounded Answer


## 🎥 Demo

Watch the SupplyLens RAG application in action:

[▶️ View SupplyLens Demo](demo/SupplyLens%20demo.mp4)