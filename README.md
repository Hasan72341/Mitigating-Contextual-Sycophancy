# Mitigating Contextual Sycophancy in RAG Pipelines

A lightweight demonstration of how Retrieval-Augmented Generation (RAG) systems can be tricked by **poisoned context** — and a multi-stage pipeline that mitigates this by combining strict reading-note generation, RAG synthesis, intrinsic reasoning, and answer merging.

---

## Overview

Large Language Models tend to blindly trust whatever context they are given (contextual sycophancy). This project implements a **4-step mitigation pipeline**:

| Step | What it does |
|------|-------------|
| **1 — Reading Notes** | Summarises each retrieved document without adding outside knowledge. |
| **2 — RAG Synthesis** | Produces an answer strictly from the notes; abstains if evidence is weak. |
| **3 — Intrinsic Reasoning** | Generates a separate answer using the model's own knowledge. |
| **4 — Merge** | Combines both answers with explicit decision rules to pick the most reliable source. |

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| **Python** | 3.9 + |
| **Ollama** | Latest |

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Hasan72341/Mitigating-Contextual-Sycophancy.git
cd Mitigating-Contextual-Sycophancy
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

**Activate it:**

- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```

### 3. Install Ollama

Download and install Ollama from [https://ollama.com/download](https://ollama.com/download).

**macOS (Homebrew):**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**  
Download the installer from the Ollama website.

### 4. Sign In to Ollama

Sign in to your Ollama account from the terminal:

```bash
ollama signin
```

This will open a browser tab for authentication. **Sign in with your Ollama account**, then **close the browser tab** once authentication is complete.

### 5. Start the Ollama Server

```bash
ollama serve
```

> [!NOTE]  
> The server runs on `http://localhost:11434` by default. Keep this terminal open.

### 6. Run the GLM-5 Cloud Model

In a **new** terminal, start the GLM-5 cloud model:

```bash
ollama run glm-5:cloud
```

This connects to the cloud-hosted GLM-5 model through your authenticated Ollama account. You can verify it's working by sending a test prompt, then type `/bye` to exit the interactive session.

> [!IMPORTANT]  
> The `glm-5:cloud` model runs remotely — it does **not** download weights to your machine. An active internet connection and a signed-in Ollama account are required.

### 7. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

### Run the Pipeline

```bash
python rag.py
```

The script ships with a built-in example:

- **Query:** *"Who does Fez marry in That '70s Show?"*
- **Poisoned context:** Two misleading documents that suggest incorrect answers.

The pipeline walks through all four steps and prints intermediate outputs before returning the final answer.

### Customise the Query & Context

Open `rag.py` and edit the variables near the bottom of the file:

```python
user_query = "Your question here"

poisoned_context = [
    "First retrieved document...",
    "Second retrieved document..."
]
```

You can also uncomment the `clean_context` block to test with accurate documents and compare the pipeline's behaviour.

### Use a Different Model

Change the `MODEL` constant at the top of `rag.py`:

```python
MODEL = "llama3"  # or any other model you've pulled via `ollama pull`
```

---

## Project Structure

```
Mitigating Contextual Sycophancy/
├── rag.py              # Main pipeline implementation
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## How It Works

```
         ┌─────────────────┐
         │  User Query +   │
         │  Retrieved Docs │
         └───────┬─────────┘
                 │
     ┌───────────▼───────────┐
     │  Step 1: Reading Notes│  ← Strict per-doc summarisation
     └───────────┬───────────┘
                 │
     ┌───────────▼───────────┐
     │  Step 2: RAG Synthesis│  ← Answer from notes only
     └───────────┬───────────┘
                 │                ┌──────────────────────┐
                 │                │ Step 3: Intrinsic    │
                 │                │ Reasoning (parallel) │
                 │                └──────────┬───────────┘
                 │                           │
     ┌───────────▼───────────────────────────▼───┐
     │         Step 4: Merge Answers             │
     │  RAG ✓ → use RAG                          │
     │  RAG ✗ + Intrinsic ✓ → use Intrinsic      │
     │  Both uncertain → Abstain                 │
     └────────────────────┬──────────────────────┘
                          │
                  ┌───────▼───────┐
                  │  Final Answer │
                  └───────────────┘
```

---

## License

This project is provided for educational and research purposes.
