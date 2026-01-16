# AI-Powered Google Drive Organizer
**(Hybrid AI: Gemini Cloud + Ollama TinyLlama Local)**

An intelligent Python-based automation system that organizes Google Drive files by understanding their content, not just filenames.
It uses a hybrid AI classification approach combining cloud LLMs (Google Gemini) and a local LLM fallback (Ollama + TinyLlama) to ensure accuracy, reliability, and cost control.

## 🎯 What This Project Does

*   **Scans files** in the root of Google Drive
*   **Reads content** from PDFs, Google Docs, and Google Sheets
*   **Understands file context** using AI
*   **Automatically creates category folders**
*   **Moves files** into the correct folders
*   **Safely handles uncertainty and failures**

---

## 🧠 Hybrid AI Classification Approach (Core Design)

This project is intentionally designed with multiple AI layers, following real-world AI engineering best practices.

### 1️⃣ Rule-Based Classifier (Fast & Free)

Checks filenames and content for strong keywords.

*   **Examples**:
    *   `invoice`, `salary`, `tax` → **Finance**
    *   `resume`, `interview` → **HR**
*   Handles obvious cases instantly.
*   Reduces AI usage and cost.

### 2️⃣ Google Gemini (Cloud LLM – Primary AI)

When `GEMINI_API_KEY` is provided, the system uses Google Gemini for classification.

*   **Why Gemini?**
    *   High accuracy.
    *   Strong contextual understanding.
    *   Excellent for complex or ambiguous documents.
*   **Usage characteristics**:
    *   Cloud-based.
    *   Requires API key.
    *   Subject to rate limits.
    *   Used only when rule-based classification fails.
*   **Logged clearly as**:
    ```text
    [SYSTEM] Using LLM Provider: Gemini (cloud)
    [LLM] Using Gemini for classification
    ```

### 3️⃣ Ollama + TinyLlama (Local Fallback AI)

If Gemini is unavailable, fails, or hits rate limits, the system automatically falls back to a local LLM.

*   **Local model used**: `TinyLlama` (via Ollama)
*   **Characteristics**:
    *   Runs fully offline.
    *   ~600 MB model.
    *   No API keys.
    *   No rate limits.
*   **Why Ollama fallback matters**:
    *   Guarantees uninterrupted execution.
    *   Enables offline usage.
    *   Prevents failures during demos or evaluations.
    *   Shows production-grade AI system design.
*   **Logged clearly as**:
    ```text
    [SYSTEM] Using LLM Provider: Ollama (TinyLlama - local)
    [LLM] Using Ollama (TinyLlama) for classification
    ```
*   **If Gemini fails mid-run**:
    ```text
    [LLM] Gemini failed, switching to Ollama (TinyLlama)
    ```

---

## 📁 Folder Categories

Files are classified into exactly one of the following:

*   **Finance**
*   **HR**
*   **Academics**
*   **Projects**
*   **Marketing**
*   **Personal**
*   **Review_Required** (low confidence or errors)

> Files with confidence < 70% are **never** auto-moved incorrectly.

---

## 🔐 Safety & Reliability Features

*   **Dry-Run Mode (default)**: Preview actions without moving files.
*   **Strict JSON validation**: Ensures AI output is machine-readable.
*   **Text truncation**: Shortens content before sending to AI (privacy-first).
*   **Graceful fallbacks**: System adapts instead of crashing.
*   **Explicit Logging**: Runtime logs clearly show which AI is used.

---

## 🛠️ Prerequisites

### 1️⃣ Python
*   Python 3.10+

### 2️⃣ Google Drive Access
*   `credentials.json` (OAuth 2.0 – Desktop App)
*   Google Drive API enabled

### 3️⃣ Ollama (Required for Local AI)
*   Install Ollama from: [https://ollama.com](https://ollama.com)
*   Pull the TinyLlama model:
    ```bash
    ollama pull tinyllama
    ```
*   *Ollama runs as a local service on `localhost:11434`*

---

## 📦 Installation

```bash
git clone <repository-url>
cd AI-Powered-Google-Drive-Organizer
pip install -r requirements.txt
```

---

## ⚙️ Environment Setup

Create a `.env` file:

```ini
# Optional (recommended) - If provided, Gemini is used first.
GEMINI_API_KEY=your_gemini_api_key_here

# Safety mode - Set to False to actually move files.
DRY_RUN=True
```

**Behavior**:
*   If `GEMINI_API_KEY` exists → **Gemini** is used.
*   If missing → **Ollama (TinyLlama)** is used automatically.

---

## ▶️ Usage

```bash
python main.py
```

### Execution Flow
1.  **Detects** available LLM provider.
2.  **Logs** active AI (Gemini or Ollama).
3.  **Scans** Google Drive root.
4.  **Extracts** file content.
5.  **Classifies** using: **Rule-based → Gemini → Ollama**.
6.  **Creates** folders if needed.
7.  **Moves** files (or previews in dry-run).

---

## 📜 Example Logs

**Using Gemini**:
```text
[SYSTEM] Using LLM Provider: Gemini (cloud)
[LLM] Using Gemini for classification
[RESULT] Salary_Report.pdf → Finance (confidence: 88)
```

**Using Ollama**:
```text
[SYSTEM] Using LLM Provider: Ollama (TinyLlama - local)
[LLM] Using Ollama (TinyLlama) for classification
[RESULT] Notes.pdf → Academics (confidence: 74)
```

---

## 📂 Project Structure

```text
├── main.py              # Orchestrates the workflow
├── config.py            # Configuration & environment loading
├── ai_classifier.py     # Rule-based + Gemini + Ollama logic
├── drive_service.py     # Google Drive API interactions
├── text_extractor.py    # PDF / Docs text extraction
├── folder_manager.py    # Folder creation & lookup
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (ignored)
└── README.md            # Documentation
```

---

## ⚠️ Notes & Limitations

*   Organizes only the **Root** of Google Drive.
*   Skips existing folders intentionally.
*   Local model accuracy is slightly lower than cloud LLMs.
*   Designed for clarity and safety over aggression.


