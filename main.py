"""Deep Researcher Agent - Entry point
Usage:
    1. Install dependencies: pip install -r requirements.txt
    2. Put your documents into the data/ folder (txt, md, or pdf supported with pdfplumber).
    3. Run: python main.py
This prototype builds a local embedding index (FAISS) using sentence-transformers,
allows querying, performs a simple multi-step reasoning (retrieve -> synthesize -> summarize),
and can export results to outputs/result.md
"""
import os
from modules.retriever import Retriever
from modules.reasoning import Reasoner

def main():
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    INDEX_DIR = os.path.join(os.path.dirname(__file__), "outputs", "index")
    os.makedirs(INDEX_DIR, exist_ok=True)

    print("📚 Building / loading index from data/ ...")
    retriever = Retriever(data_dir=DATA_DIR, index_dir=INDEX_DIR)
    retriever.build_or_load_index(force_rebuild=True)


    print("\n✅ Ready. Enter a research query (type 'exit' to quit).")
    reasoner = Reasoner(retriever)
    while True:
        q = input("\n🔎 Query > ").strip()
        if not q:
            continue
        if q.lower() in ("exit", "quit"):
            print("Bye 👋")
            break

        # Run multi-step reasoning
        combined, summary = reasoner.answer(q)

        print("\n---\n📑 Retrieved Evidence:\n")
        print(combined)

        print("\n---\n📝 Synthesized Summary:\n")
        print(summary)

        # Export results to file
        reasoner.answer_and_export(q, export_path=os.path.join("outputs", "result.md"))
        print("\n✅ Full result also exported to outputs/result.md")


if __name__ == '__main__':
    main()
