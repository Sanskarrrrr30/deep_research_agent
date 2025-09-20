"""Embeddings helper: loads a sentence-transformers model and encodes texts.
Falls back with a helpful message when dependencies are missing.
"""
from typing import List
import os

def get_model(model_name: str = 'all-MiniLM-L6-v2'):
    try:
        from sentence_transformers import SentenceTransformer
    except Exception as e:
        raise ImportError(
            "sentence-transformers is required. Install with: pip install sentence-transformers\n" +
            "(If you plan to use a GPU, also ensure torch is installed.)\nError: " + str(e)
        )
    return SentenceTransformer(model_name)

def embed_texts(texts: List[str], model_name: str = 'all-MiniLM-L6-v2'):
    model = get_model(model_name)
    # model.encode supports batching internally
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    return embeddings
