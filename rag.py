import os
import time

import chromadb
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from your .env file")


CHROMA_PATH = "chroma_db"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

GROQ_MODEL = "llama-3.1-8b-instant"

# Keep this moderate so Groq does not hit the free-tier limit
TOP_K = 4

# Keep retrieved text small
MAX_CHARS_PER_CHUNK = 1400

MAX_CONTEXT_CHARS = 4500

MAX_OUTPUT_TOKENS = 250


# ============================================================
# EMBEDDING MODEL
# ============================================================

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)


# ============================================================
# CHROMADB
# ============================================================

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


# ============================================================
# GET COLLECTION
# ============================================================

collections = chroma_client.list_collections()

if not collections:
    raise ValueError(
        "No ChromaDB collection found. "
        "Please run your indexing script first."
    )


# Try to find SupplyLens collection first
collection = None

for c in collections:

    try:
        name = c.name
    except:
        name = str(c)

    if name.lower() == "supplylens":
        collection = chroma_client.get_collection(name=name)
        break


# If collection is not called supplylens,
# automatically use the first available collection
if collection is None:

    try:
        first_name = collections[0].name
    except:
        first_name = str(collections[0])

    collection = chroma_client.get_collection(
        name=first_name
    )


# ============================================================
# GROQ
# ============================================================

groq_client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# RETRIEVE DOCUMENTS
# ============================================================

def retrieve_documents(question):

    query_embedding = embedding_model.encode(
        question
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )

    documents = results.get(
        "documents",
        [[]]
    )

    if not documents:
        return []

    return documents[0]


# ============================================================
# PREPARE CONTEXT
# ============================================================

def prepare_context(documents):

    context_parts = []

    total_chars = 0

    for i, document in enumerate(documents):

        if not document:
            continue

        # Clean whitespace
        document = " ".join(
            document.split()
        )

        # Limit each chunk
        document = document[
            :MAX_CHARS_PER_CHUNK
        ]

        # Remaining context space
        remaining = (
            MAX_CONTEXT_CHARS
            - total_chars
        )

        if remaining <= 0:
            break

        document = document[
            :remaining
        ]

        context_parts.append(
            f"DOCUMENT PASSAGE {i + 1}:\n"
            f"{document}"
        )

        total_chars += len(document)

    return "\n\n".join(
        context_parts
    )


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(question, context):

    system_prompt = """
You are SupplyLens, a document intelligence assistant
for Meridian Components.

You must answer ONLY using the document passages provided.

STRICT RULES:

1. Never invent information.

2. Never guess an answer.

3. If the document passages do not contain enough
   information to answer the question, say:

   "I could not find sufficient information in the
   provided documents."

4. For numerical questions, use only numbers that
   actually appear in the passages.

5. For supplier-spend questions, compare the actual
   supplier values. Do not use a total or weighted
   average as a supplier's spend.

6. For approval-authority questions, carefully check
   the purchase-order value against the exact approval
   range stated in the document.

7. Do not assume that a rule for one monetary range
   applies to another range.

8. If the evidence is incomplete, say so instead of
   making an inference.

9. Give a short, clear answer.

10. Mention the relevant clause, supplier, amount,
    threshold, or policy when available.

11. Do not use outside knowledge.
"""

    user_prompt = f"""
DOCUMENT PASSAGES:

{context}

QUESTION:

{question}

Answer using ONLY the document passages above.
"""

    # ========================================================
    # GROQ REQUEST
    # ========================================================

    for attempt in range(2):

        try:

            response = groq_client.chat.completions.create(

                model=GROQ_MODEL,

                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],

                temperature=0,

                max_tokens=MAX_OUTPUT_TOKENS
            )

            return response.choices[0].message.content


        except Exception as e:

            error_text = str(e)

            # ------------------------------------------------
            # GROQ RATE LIMIT
            # ------------------------------------------------

            if "429" in error_text:

                if attempt == 0:

                    time.sleep(20)

                    continue

                return (
                    "Groq rate limit reached. "
                    "Please wait about 20 seconds and try again."
                )

            # ------------------------------------------------
            # OTHER ERROR
            # ------------------------------------------------

            return (
                "Unable to generate an answer right now. "
                "Please try again."
            )

    return (
        "Unable to generate an answer right now."
    )


# ============================================================
# MAIN RAG FUNCTION
# ============================================================

def ask_rag(question):

    question = question.strip()

    if not question:

        return "Please enter a question."


    # --------------------------------------------------------
    # 1. RETRIEVE
    # --------------------------------------------------------

    documents = retrieve_documents(
        question
    )


    if not documents:

        return (
            "I could not find sufficient information "
            "in the provided documents."
        )


    # --------------------------------------------------------
    # 2. CREATE CONTEXT
    # --------------------------------------------------------

    context = prepare_context(
        documents
    )


    if not context:

        return (
            "I could not find sufficient information "
            "in the provided documents."
        )


    # --------------------------------------------------------
    # 3. GENERATE ANSWER
    # --------------------------------------------------------

    return generate_answer(
        question,
        context
    )