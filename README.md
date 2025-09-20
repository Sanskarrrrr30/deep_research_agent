# Deep Researcher Agent (Prototype)

## Overview
This project is a local-only research assistant:
- Indexes local documents (data/)
- Generates embeddings using sentence-transformers
- Stores vectors in FAISS
- Retrieves relevant chunks, synthesizes and summarizes answers
- Exports results to `outputs/result.md`

## Quick start
1. Create a virtual environment (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # on Windows: .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Add files to `data/` (txt, md supported; PDFs supported via pdfplumber).
4. Run:
   ```bash
   python main.py
   ```

## Notes
- This is a hackathon-ready prototype. For large corpora, consider chunking, batching,
  and persistent vector stores (Chroma, Milvus, etc.).
- The code attempts to handle missing packages gracefully by telling you how to install them.
