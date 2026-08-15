import streamlit as st
from rag import ask_rag


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SupplyLens",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* ================= GENERAL ================= */

.stApp {
    background: #080b12;
    color: #f8fafc;
}

.main .block-container {
    max-width: 1180px;
    padding-top: 2.2rem;
    padding-bottom: 3rem;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}


/* ================= HEADER ================= */

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4rem;
}

.logo {
    font-size: 1.55rem;
    font-weight: 800;
    color: #f8fafc;
}

.logo-mark {
    color: #8b5cf6;
}

.tagline {
    color: #64748b;
    font-size: 0.82rem;
    margin-left: 10px;
}

.online {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 7px 13px;
    border: 1px solid #1e293b;
    border-radius: 999px;
    background: #0d111b;
    color: #94a3b8;
    font-size: 0.76rem;
}

.online-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #34d399;
    display: inline-block;
}


/* ================= HERO ================= */

.hero {
    text-align: center;
    margin-bottom: 2.5rem;
}

.hero-label {
    display: inline-block;
    padding: 7px 14px;
    border-radius: 999px;
    background: #151124;
    border: 1px solid #292044;
    color: #a78bfa;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.7px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.hero-title {
    font-size: 3.4rem;
    line-height: 1.05;
    font-weight: 800;
    letter-spacing: -2px;
    color: #f8fafc;
}

.hero-title span {
    color: #8b5cf6;
}

.hero-description {
    max-width: 700px;
    margin: 1rem auto 0 auto;
    color: #64748b;
    font-size: 1rem;
    line-height: 1.7;
}


/* ================= SEARCH ================= */

.search-wrapper {
    max-width: 850px;
    margin: 0 auto 10px auto;
    padding: 22px;
    background: #0d111b;
    border: 1px solid #1e293b;
    border-radius: 18px 18px 0 0;
}

.search-label {
    color: #94a3b8;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.8px;
}

div[data-testid="stTextInput"] {
    max-width: 850px;
    margin-left: auto;
    margin-right: auto;
}

div[data-testid="stTextInput"] input {
    background: #080b12 !important;
    border: 1px solid #263244 !important;
    border-radius: 12px !important;
    color: #f8fafc !important;
    padding: 14px !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #475569 !important;
}


/* ================= BUTTONS ================= */

.stButton > button {
    border-radius: 10px !important;
    border: 1px solid #263244 !important;
    background: #101621 !important;
    color: #cbd5e1 !important;
    font-weight: 600 !important;
    min-height: 42px !important;
}

.stButton > button:hover {
    border-color: #8b5cf6 !important;
    color: #c4b5fd !important;
    background: #151124 !important;
}


/* ================= FORM ================= */

div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}


/* ================= ANALYZE BUTTON ================= */

div[data-testid="stFormSubmitButton"] button {
    background: #8b5cf6 !important;
    border: 1px solid #8b5cf6 !important;
    color: white !important;
    border-radius: 10px !important;
    min-height: 48px !important;
    font-weight: 700 !important;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background: #7c3aed !important;
    border-color: #7c3aed !important;
}


/* ================= SUGGESTIONS ================= */

.suggestion-title {
    max-width: 850px;
    margin: 1.8rem auto 0.7rem auto;
    color: #475569;
    font-size: 0.72rem;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.8px;
}


/* ================= ANSWER ================= */

.answer-header {
    margin-top: 3.5rem;
    margin-bottom: 0.8rem;
    color: #a78bfa;
    font-size: 0.76rem;
    font-weight: 700;
    text-transform: uppercase;
}

.answer-card {
    background: #0d111b;
    border: 1px solid #1e293b;
    border-left: 3px solid #8b5cf6;
    border-radius: 18px;
    padding: 25px;
}

.answer-title {
    color: #f8fafc;
    font-size: 1.05rem;
    font-weight: 700;
}

.answer-note {
    color: #64748b;
    font-size: 0.78rem;
    margin-top: 15px;
}


/* ================= KNOWLEDGE BASE ================= */

.info-title {
    color: #f8fafc;
    font-size: 1.1rem;
    font-weight: 700;
    margin-top: 3rem;
    margin-bottom: 1rem;
}

.info-card {
    background: #0d111b;
    border: 1px solid #1e293b;
    border-radius: 15px;
    padding: 18px;
    min-height: 125px;
}

.info-icon {
    font-size: 1.2rem;
    margin-bottom: 8px;
}

.info-card-title {
    color: #e2e8f0;
    font-weight: 700;
    font-size: 0.88rem;
}

.info-card-text {
    color: #64748b;
    font-size: 0.78rem;
    line-height: 1.5;
    margin-top: 5px;
}


/* ================= PIPELINE ================= */

.pipeline-title {
    color: #f8fafc;
    font-size: 1.1rem;
    font-weight: 700;
    margin-top: 3rem;
    margin-bottom: 12px;
}

.pipeline-box {
    background: #0d111b;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 28px 22px;
    margin-bottom: 25px;
    overflow-x: auto;
}

.pipeline-flow {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    min-width: 850px;
}

.pipeline-step {
    background: #111827;
    border: 1px solid #263244;
    border-radius: 10px;
    padding: 12px 18px;
    text-align: center;
    color: #94a3b8;
    font-size: 0.78rem;
    font-weight: 600;
    white-space: nowrap;
    min-width: 82px;
}

.pipeline-arrow {
    color: #8b5cf6;
    font-size: 1.4rem;
    font-weight: 600;
    flex-shrink: 0;
}


/* ================= FOOTER ================= */

.footer {
    text-align: center;
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid #151c29;
    color: #475569;
    font-size: 0.72rem;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.html("""
<div class="topbar">

    <div>
        <span class="logo">
            <span class="logo-mark">◆</span> SupplyLens
        </span>

        <span class="tagline">
            Document Intelligence
        </span>
    </div>

    <div class="online">
        <span class="online-dot"></span>
        SYSTEM ONLINE
    </div>

</div>
""")


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="hero">

    <div class="hero-label">
        AI-powered supply chain intelligence
    </div>

    <div class="hero-title">
        Ask your documents.<br>
        <span>Get grounded answers.</span>
    </div>

    <div class="hero-description">
        Search across Meridian Components' procurement and
        supply-chain documents using Retrieval-Augmented Generation.
    </div>

</div>
""")


# ============================================================
# SEARCH LABEL
# ============================================================

st.html("""
<div class="search-wrapper">
    <div class="search-label">
        ASK SUPPLYLENS
    </div>
</div>
""")


# ============================================================
# SEARCH FORM
# ============================================================

with st.form("search_form"):

    question = st.text_input(
        "Question",
        placeholder="Ask about suppliers, procurement, penalties, spend, quality...",
        label_visibility="collapsed"
    )

    ask = st.form_submit_button(
        "◆  Analyze documents",
        use_container_width=True
    )


# ============================================================
# TRY ASKING
# ============================================================

st.html("""
<div class="suggestion-title">
    TRY ASKING
</div>
""")


q1, q2, q3 = st.columns(3)


with q1:

    if st.button(
        "PO approval authority",
        use_container_width=True
    ):

        st.session_state.selected_question = (
            "Who approves a purchase order worth ₹1.4 crore?"
        )

        st.rerun()


with q2:

    if st.button(
        "Highest supplier spend",
        use_container_width=True
    ):

        st.session_state.selected_question = (
            "Which supplier has the highest Q1 spend?"
        )

        st.rerun()


with q3:

    if st.button(
        "Kaveri Metals penalty",
        use_container_width=True
    ):

        st.session_state.selected_question = (
            "What penalty applies to Kaveri Metals for 1,150 PPM defects?"
        )

        st.rerun()


# ============================================================
# HANDLE SELECTED SUGGESTION
# ============================================================

if "selected_question" in st.session_state:

    selected_question = st.session_state.selected_question

    del st.session_state.selected_question

    st.session_state.pending_question = selected_question

    st.rerun()


# ============================================================
# PROCESS PENDING QUESTION
# ============================================================

if "pending_question" in st.session_state:

    pending_question = st.session_state.pending_question

    del st.session_state.pending_question

    st.html("""
    <div class="answer-header">
        ◆ AI ANALYSIS
    </div>
    """)

    with st.spinner("Searching the knowledge base..."):

        try:

            answer = ask_rag(pending_question)

            st.html("""
            <div class="answer-card">

                <div class="answer-title">
                    SupplyLens Response
                </div>

            </div>
            """)

            st.markdown(answer)

            st.html("""
            <div class="answer-note">
                Answer generated from retrieved company documents.
            </div>
            """)

        except Exception as e:

            st.error("Unable to process the question.")
            st.exception(e)


# ============================================================
# RAG ANSWER FROM MANUAL QUESTION
# ============================================================

if ask:

    if not question.strip():

        st.warning("Please enter a question first.")

    else:

        st.html("""
        <div class="answer-header">
            ◆ AI ANALYSIS
        </div>
        """)

        with st.spinner("Searching the knowledge base..."):

            try:

                answer = ask_rag(question)

                st.html("""
                <div class="answer-card">

                    <div class="answer-title">
                        SupplyLens Response
                    </div>

                </div>
                """)

                st.markdown(answer)

                st.html("""
                <div class="answer-note">
                    Answer generated from retrieved company documents.
                </div>
                """)

            except Exception as e:

                st.error("Unable to process the question.")
                st.exception(e)


# ============================================================
# KNOWLEDGE BASE
# ============================================================

st.html("""
<div class="info-title">
    Knowledge Base
</div>
""")


c1, c2, c3 = st.columns(3)


with c1:

    st.html("""
    <div class="info-card">

        <div class="info-icon">
            ▣
        </div>

        <div class="info-card-title">
            Procurement Handbook
        </div>

        <div class="info-card-text">
            Procurement rules, approval authority,
            supplier classification and payment terms.
        </div>

    </div>
    """)


with c2:

    st.html("""
    <div class="info-card">

        <div class="info-icon">
            ▥
        </div>

        <div class="info-card-title">
            Q1 Supply Chain Review
        </div>

        <div class="info-card-text">
            Supplier scorecards, spend, delivery,
            defects and quality performance.
        </div>

    </div>
    """)


with c3:

    st.html("""
    <div class="info-card">

        <div class="info-icon">
            ◉
        </div>

        <div class="info-card-title">
            26 Indexed Chunks
        </div>

        <div class="info-card-text">
            Relevant document passages are retrieved
            from the ChromaDB knowledge base.
        </div>

    </div>
    """)


# ============================================================
# RAG PIPELINE
# ============================================================

st.html("""
<div class="pipeline-title">
    How SupplyLens works
</div>

<div class="pipeline-box">

    <div class="pipeline-flow">

        <div class="pipeline-step">
            PDF
        </div>

        <div class="pipeline-arrow">
            →
        </div>

        <div class="pipeline-step">
            Chunking
        </div>

        <div class="pipeline-arrow">
            →
        </div>

        <div class="pipeline-step">
            Embeddings
        </div>

        <div class="pipeline-arrow">
            →
        </div>

        <div class="pipeline-step">
            ChromaDB
        </div>

        <div class="pipeline-arrow">
            →
        </div>

        <div class="pipeline-step">
            Retrieval
        </div>

        <div class="pipeline-arrow">
            →
        </div>

        <div class="pipeline-step">
            Groq
        </div>

        <div class="pipeline-arrow">
            →
        </div>

        <div class="pipeline-step">
            Answer
        </div>

    </div>

</div>
""")


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">
    SupplyLens · Retrieval-Augmented Generation ·
    ChromaDB · Sentence Transformers · Groq
</div>
""")