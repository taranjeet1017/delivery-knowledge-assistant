import json
from datetime import datetime

import numpy as np
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(".env")
client = OpenAI()

st.set_page_config(
    page_title="Delivery Knowledge Assistant",
    page_icon="📘"
)

st.markdown("""
<style>
    .stApp {
        background-color: #F7F9FC;
    }

    h1, h2, h3 {
        color: #17324D;
    }

    [data-testid="stSidebar"] {
        background-color: #EEF4F7;
    }

    .stButton > button {
        background-color: #1F6F78;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }

    .stButton > button:hover {
        background-color: #185B63;
        color: white;
    }

    [data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #D8E2E8;
        padding: 12px;
        border-radius: 10px;
    }

    [data-testid="stExpander"] {
        background-color: white;
        border: 1px solid #D8E2E8;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)python run_eval.py

st.title("Delivery Knowledge Assistant")
st.caption("Grounded AI assistant for the Nexus modernization project")
st.info(
    "Portfolio demonstration using fully synthetic project data. "
    "No real client or confidential information is included."
)
if st.button("Clear conversation"):
    st.session_state.messages = []
    st.session_state.last_question = None
    st.rerun()


with open("index.json", "r", encoding="utf-8") as f:
    records = json.load(f)

with st.sidebar:
    st.header("Project Knowledge")

    unique_sources = sorted(
        set(record["source"] for record in records)
    )

    st.metric(
        "Indexed documents",
        len(unique_sources)
    )

    st.metric(
        "Knowledge chunks",
        len(records)
    )

    st.divider()

    st.markdown("### Try asking")

    st.markdown("""
- What is the latest working UAT start date?
- What is preventing UAT from starting?
- What changed in Phase 2?
- What are the current project risks?
- What is the total project budget?
""")

    st.divider()

    with st.expander("How this assistant works"):
        st.markdown("""
1. Project documents are converted into searchable text chunks.
2. OpenAI embeddings identify the most relevant project evidence.
3. Retrieval considers both semantic relevance and document chronology.
4. The AI answers only from the retrieved project context.
5. Supporting evidence can be inspected below each answer.
""")

    st.divider()

    with st.expander(
        f"View indexed sources ({len(unique_sources)})"
    ):
        for source in unique_sources:
            st.write(f"• {source}")

if "last_question" not in st.session_state:
    st.session_state.last_question = None
if "messages" not in st.session_state:
    st.session_state.messages = []


def similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )

def contextualize_question(question):

    follow_up_terms = [
        "it", "this", "that", "they", "them",
        "those", "these", "its", "their"
    ]

    words = question.lower().split()

    is_follow_up = any(
        term in words
        for term in follow_up_terms
    )

    if not st.session_state.last_question or not is_follow_up:
        return question

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=f"""
Rewrite the follow-up question as a standalone project question.

Previous question:
{st.session_state.last_question}

Follow-up question:
{question}

Resolve references such as "it", "this", "that", "they",
"them", "those", or "these" using the previous question.

Return only the rewritten question.
"""
    )

    return response.output_text.strip()

def retrieve(question, top_k=5):

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    query_embedding = response.data[0].embedding

    results = []

    all_dates = [
        datetime.fromisoformat(record["source_date"])
        for record in records
    ]

    oldest_date = min(all_dates)
    newest_date = max(all_dates)
    date_range = max(
        (newest_date - oldest_date).days,
        1
    )

    chronology_terms = [
        "latest",
        "current",
        "now",
        "changed",
        "change",
        "status",
        "still",
        "prevent",
        "blocking",
        "blocker"
    ]

    chronology_sensitive = any(
        term in question.lower()
        for term in chronology_terms
    )

    for record in records:

        semantic_score = similarity(
            query_embedding,
            record["embedding"]
        )

        adjusted_score = semantic_score

        if chronology_sensitive:

            record_date = datetime.fromisoformat(
                record["source_date"]
            )

            freshness = (
                (record_date - oldest_date).days
                / date_range
            )

            # Recency helps, but semantic relevance
            # remains the primary factor.
            adjusted_score += 0.02 * freshness

        results.append(
            (adjusted_score, record)
        )

    results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    # Prefer evidence from different documents
    # instead of several similar chunks from one file.
    selected = []
    source_counts = {}

    for score, record in results:

        source = record["source"]

        if source_counts.get(source, 0) < 2:
            selected.append((score, record))
            source_counts[source] = source_counts.get(source, 0) + 1

        if len(selected) == top_k:
            break

    return selected


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant" and message.get("sources"):

            with st.expander("View supporting project sources"):

                for source in message["sources"]:

                    st.markdown(
                        f"**{source['source']}**  \n"
                        f"Source date: {source['source_date']} | "
                        f"Chunk: {source['chunk']}"
                    )

                    st.caption(
                        f"Retrieval relevance: {source['score']:.3f}"
                    )

                    preview = source["text"][:800]

                    if len(source["text"]) > 800:
                        preview += "..."

                    st.write(preview)
                    st.divider()
                    
question = st.chat_input(
    "Ask a question about the Nexus project..."
)


if question:

    st.chat_message("user").write(question)
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    search_question = question

    search_question = contextualize_question(question)

    matches = retrieve(search_question)

    context_parts = []

    for score, record in matches:

        context_parts.append(
            f"""
SOURCE: {record['source']}
SOURCE DATE: {record['source_date']}
CHUNK: {record['chunk']}

{record['text']}
"""
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are an enterprise project delivery knowledge assistant.

Answer the user's question using ONLY the project information
provided below.

Important rules:

1. Do not invent information.

2. When multiple documents describe the same date, status,
   dependency, risk, or decision, use the most recently dated
   source as the current position.

3. Do not carry forward an older open dependency, assumption,
   or status unless a newer document confirms that it is still
   applicable.

4. Use older documents only to explain how the position changed
   over time.

5. Clearly distinguish an original baseline from a revised
   or current position.

6. Do not create a separate Sources section or list filenames
   in the answer. The application displays the retrieved
   supporting evidence separately.

7. If the answer cannot be determined from the sources,
   say so clearly.
8. Answer only what the user asked. Do not state that a fact is
   missing or unavailable unless the user specifically asked for
   that fact or it is necessary to answer the question.

PROJECT INFORMATION:

{context}

USER QUESTION:

{search_question}
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    st.chat_message("assistant").write(
        response.output_text
    )
    st.session_state.messages.append({
        "role": "assistant",
        "content": response.output_text,
        "sources": [
        {
            "source": record["source"],
            "source_date": record["source_date"],
            "chunk": record["chunk"],
            "score": score,
            "text": record["text"]
        }
        for score, record in matches
        ]
    })

    st.session_state.last_question = question

    with st.expander("View supporting project sources"):

        for score, record in matches:

            st.markdown(
                f"**{record['source']}**  \n"
                f"Source date: {record['source_date']} | "
                f"Chunk: {record['chunk']}"
            )

            st.caption(
                f"Retrieval relevance: {score:.3f}"
            )

            preview = record["text"][:800]

            if len(record["text"]) > 800:
                preview += "..."

            st.write(preview)

            st.divider()
