# NovaChat 📚🚀



---

## Overview

**NovaChat** is a lightweight Retrieval‑Augmented Generation (RAG) assistant that helps you query a knowledge base (e.g., company policies, FAQs, documentation) using **natural language**.  It is built on top of a simple **retrieval pipeline** (`retrival.py`) and can be accessed **through two interfaces**:

1. **Streamlit UI** – an interactive web app that mimics a terminal‑style chat experience.
2. **FastAPI endpoint** – a programmable HTTP API (`fast.py`) that can be integrated into other services.

Both interfaces share the same backend logic, so the answers are consistent regardless of how you call the system.

---

## Problem it solves

- **Quick access to scattered information** – avoid digging through PDFs, wikis, or SharePoint.
- **Consistent answers** – the RAG pipeline always returns the most relevant snippet followed by a concise response.
- **Flexible consumption** – developers can embed the API in bots or automation scripts, while non‑technical users get a friendly UI.

---

## Core Techniques & Stack

| Layer | Technology | Purpose |
|------|------------|---------|
| **Frontend** | **Streamlit** (`app.py`) | Rich, dark‑theme UI with streaming, terminal‑like output. |
| **API** | **FastAPI** (`fast.py`) | Exposes `/chat` POST endpoint for programmatic use. |
| **Retrieval** | **ChromaDB** + **transformers** (`retrival.py`) | Vector store using embedding similarity and keyword matching, plus LLM‑based text generation. |
| **Prompt templating** | **Jinja2** (`prompt.jinja`) | Guarantees consistent prompts for the LLM. |
| **Environment** | **Python 3.11**, **virtualenv** (`.venv`) | Isolated dependencies. |

---

## Installation & Setup

```bash
# 1️⃣ Clone the repository (or open the existing folder)
git clone https://github.com/yourusername/novachat.git
cd novachat

# 2️⃣ Create & activate a virtual environment
python -m venv .venv
# PowerShell
.venv\Scripts\Activate.ps1
# Bash (if using WSL/git‑bash)
source .venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt   # make sure this file exists, otherwise:
# pip install streamlit fastapi uvicorn chromadb transformers jinja2
```

> **Note** – The `torchvision` import error you saw earlier indicates that the optional `torchvision` package is missing. It is only required if you plan to use image‑based models. Install it with:
>
> ```bash
> pip install torchvision
> ```

---

## Running the Project

### 1️⃣ Streamlit UI (recommended for interactive use)

```bash
# Activate the environment if not already active
.venv\Scripts\Activate.ps1   # PowerShell
# or source .venv/bin/activate on Bash

streamlit run app.py
```

- Open the URL printed in the console (usually <http://localhost:8501>).
- Paste a question in the **"📋 Paste your input here"** box and press **⚡ Send Query**.
- The answer will appear with a terminal‑style typing animation.

### 2️⃣ FastAPI endpoint (for programmatic access)

```bash
uvicorn fast:app --host 0.0.0.0 --port 8000 --reload
```

Then send a POST request (e.g., via `curl` or Python `requests`):

```bash
curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the leave policy?"}'
```

The response will be a JSON object:

```json
{ "query": "What is the leave policy?", "answer": "[generated answer]" }
```

---

## Project Structure

```
Novachat/
├─ app.py            # Streamlit front‑end (UI)
├─ fast.py           # FastAPI back‑end (HTTP API)
├─ retrival.py       # Core RAG logic (vector store + LLM)
├─ prompt.jinja      # Jinja2 prompt template used by retrival.py
├─ chroma_db/        # Persistent vector store (auto‑created)
├─ .venv/            # Virtual environment (excluded from Git)
└─ README.md         # 📖 This file
```

---

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/awesome‑feature`).
3. Make your changes and ensure the UI/API still works.
4. Open a Pull Request with a clear description of the enhancement.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

*Happy chatting with NovaChat!*
