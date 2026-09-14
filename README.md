# Delivery Knowledge Assistant

**Live Demo:** [Open the Delivery Knowledge Assistant](https://delivery-knowledge-assistant-nd8xpudpu9hugsvwrxnmdc.streamlit.app/)

An AI-powered project delivery assistant that answers questions from project documents using Retrieval-Augmented Generation (RAG).

## Demo

![Delivery Knowledge Assistant Demo](assets/delivery-knowledge-assistant-demo.png)

An AI-powered project delivery assistant that answers questions from project documents using Retrieval-Augmented Generation (RAG).


## What it demonstrates

- Enterprise document ingestion
- Semantic search using embeddings
- Grounded AI responses
- Chronology-aware retrieval
- Conversational follow-up questions
- Source transparency and evidence inspection
- Hallucination control for unsupported information

## Demo Use Case

The application uses a fully synthetic software-modernization project called **NexusCert Platform Modernization**.

A Delivery Manager can ask questions such as:

- What is the latest working UAT start date?
- What is preventing UAT from starting?
- What changed in Phase 2?
- What are the current project risks?
- Which dependencies are still open?

## Technology

- Python
- Streamlit
- OpenAI API
- OpenAI Embeddings
- NumPy
- python-docx
- openpyxl

## Solution Architecture

```mermaid
flowchart LR
    A[Project Documents] --> B[Document Extraction]
    B --> C[Text Chunking]
    C --> D[OpenAI Embeddings]
    D --> E[Vector Index]
    F[Delivery Manager Question] --> G[Semantic Retrieval]
    E --> G
    G --> H[Chronology-Aware Ranking]
    H --> I[Relevant Project Context]
    I --> J[OpenAI Response Generation]
    J --> K[Grounded Answer]
    K --> L[Supporting Source Evidence]
```

## Data Privacy

All project documents included in this repository are synthetic. No real client or confidential informat
cat > README.md <<'EOF'
# Delivery Knowledge Assistant

An AI-powered project delivery assistant that answers questions from project documents using Retrieval-Augmented Generation (RAG).

## What it demonstrates

- Enterprise document ingestion
- Semantic search using embeddings
- Grounded AI responses
- Chronology-aware retrieval
- Conversational follow-up questions
- Source transparency and evidence inspection
- Hallucination control for unsupported information

## Demo Use Case

The application uses a fully synthetic software-modernization project called **NexusCert Platform Modernization**.

A Delivery Manager can ask questions such as:

- What is the latest working UAT start date?
- What is preventing UAT from starting?
- What changed in Phase 2?
- What are the current project risks?
- Which dependencies are still open?

## Technology

- Python
- Streamlit
- OpenAI API
- OpenAI Embeddings
- NumPy
- python-docx
- openpyxl

## Data Privacy

## Key Design Decisions

- **Grounded answers rather than generic AI responses:** The assistant answers only from indexed project artefacts.
- **Chronology-aware retrieval:** When project dates, risks, dependencies or decisions evolve, newer evidence is prioritized while older information can still explain the history.
- **Transparent evidence:** Every answer can expose the supporting document excerpts used by the assistant.
- **Hallucination control:** If the source material does not contain an answer, the assistant states that rather than inventing information.
- **Conversational context:** Follow-up questions such as “What is preventing it from starting?” are rewritten into standalone questions before retrieval.
- **Privacy-safe portfolio design:** The demonstration uses completely synthetic project data rather than real client information.

## Business Value

The Delivery Knowledge Assistant demonstrates how Generative AI can reduce the effort required to understand and govern complex delivery programmes.

For a Delivery or Program Manager, it can help:

- Surface current risks, dependencies and blockers from distributed project artefacts.
- Trace how milestones, commitments and decisions changed over time.
- Reduce manual searching across status reports, meeting minutes and trackers.
- Improve leadership visibility by providing evidence-backed answers.
- Accelerate onboarding of new project or programme stakeholders.
- Support better governance while keeping the human decision-maker in control.

The solution is designed as a practical enterprise AI use case rather than a generic chatbot.

## Evaluation

A small evaluation suite is included to validate the RAG pipeline against representative Delivery Manager questions.

The current test set checks:

- Retrieval of the latest UAT date
- Explanation of milestone changes
- Identification of Phase 2 scope changes
- Identification of estimation dependencies
- Refusal to invent unsupported project budget information

**Current result: 5/5 evaluation cases passed.**

The evaluation uses expected facts rather than exact response wording so that correct answers are not penalized for harmless phrasing differences.

## MVP Scope and Future Evolution

This implementation is intentionally designed as a focused portfolio MVP. The current version uses a small synthetic project dataset and a lightweight local JSON-based embedding index.

A production enterprise implementation could evolve to include:

- **Google Drive / SharePoint integration** for automated ingestion of live project artefacts.
- **Incremental indexing** when documents are added or updated.
- **Enterprise vector storage** using a managed vector database.
- **Role-based access control** so users retrieve only information they are authorized to see.
- **Document-level security and audit logging** for enterprise governance.
- **Automated evaluation** of retrieval quality, groundedness and answer accuracy.
- **Portfolio-level knowledge** across multiple projects rather than a single programme.
- **Structured delivery insights** such as automated risk summaries, overdue actions, milestone changes and executive briefings.

The current MVP demonstrates the core architecture and user experience while keeping the implementation transparent and easy to evaluate.

All project documents included in this repository are synthetic. No real client or confidential information is used.
