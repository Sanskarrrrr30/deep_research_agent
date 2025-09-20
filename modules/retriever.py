"""Retriever: loads documents, chunks them, builds FAISS index and retrieves top-k documents."""
from typing import List, Tuple
import os, glob, json
from tqdm import tqdm

class Retriever:
    def __init__(self, data_dir='data', index_dir='outputs/index', chunk_size=500, overlap=50, model_name='all-MiniLM-L6-v2'):
        self.data_dir = data_dir
        self.index_dir = index_dir
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.model_name = model_name
        self.index_path = os.path.join(index_dir, 'faiss.index')
        self.meta_path = os.path.join(index_dir, 'meta.json')
        self._index = None
        self._metadatas = []
        self._embeddings = None

    def _read_file(self, path: str) -> str:
        ext = os.path.splitext(path)[1].lower()
        if ext in ['.txt', '.md']:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        elif ext == '.pdf':
            try:
                import pdfplumber
            except Exception as e:
                raise ImportError('pdfplumber required to read PDF files. Install with pip install pdfplumber')
            text = ''
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ''
            return text
        else:
            return ''

    def _chunk_text(self, text: str):
        tokens = text.split()
        i = 0
        chunks = []
        while i < len(tokens):
            chunk = tokens[i:i+self.chunk_size]
            chunks.append(' '.join(chunk))
            i += self.chunk_size - self.overlap
        return chunks

    def build_or_load_index(self, force_rebuild=False):
        """Builds FAISS index from files under data_dir or loads existing index if present."""
        # lazy import to give nicer error messages
        try:
            import faiss
            import numpy as np
        except Exception as e:
            raise ImportError('faiss-cpu and numpy are required. Install with: pip install faiss-cpu numpy\nError: ' + str(e))

        if os.path.exists(self.index_path) and os.path.exists(self.meta_path) and not force_rebuild:
            print('Loading existing index...')
            self._index = faiss.read_index(self.index_path)
            with open(self.meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            self._metadatas = meta['metadatas']
            return

        # otherwise build
        texts = []
        metadatas = []
        files = []
        for ext in ('*.txt','*.md','*.pdf'):
            files.extend(glob.glob(os.path.join(self.data_dir, ext)))
        if not files:
            print('No files found in data/. A sample file has been created at data/sample.txt. Please add documents and rebuild (run with force_rebuild=True).')
            return

        for path in files:
            content = self._read_file(path)
            if not content:
                continue
            chunks = self._chunk_text(content)
            for idx, ch in enumerate(chunks):
                texts.append(ch)
                metadatas.append({'source': os.path.basename(path), 'chunk': idx, 'text_preview': ch[:200]})

        if not texts:
            print('No textual content extracted from files.')
            return

        print(f'Encoding {len(texts)} chunks with model "{self.model_name}" ...')
        from modules.embeddings import embed_texts
        emb = embed_texts(texts, model_name=self.model_name)
        import numpy as np, faiss
        d = emb.shape[1]
        index = faiss.IndexFlatIP(d)  # using inner product on normalized vectors (we'll normalize)
        # normalize
        faiss.normalize_L2(emb)
        index.add(emb.astype('float32'))
        # save index and metadata
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(index, self.index_path)
        with open(self.meta_path, 'w', encoding='utf-8') as f:
            json.dump({'metadatas': metadatas}, f, ensure_ascii=False, indent=2)
        self._index = index
        self._metadatas = metadatas
        print('Index built and saved to', self.index_path)

    def query(self, query_text: str, topk: int = 5) -> List[Tuple[dict, float]]:
        """Return top-k metadata and scores for the query."""
        try:
            import faiss, numpy as np
        except Exception as e:
            raise ImportError('faiss-cpu and numpy are required. Install with: pip install faiss-cpu numpy\nError: ' + str(e))
        if self._index is None:
            raise RuntimeError('Index not built. Run build_or_load_index() first.')
        from modules.embeddings import embed_texts
        q_emb = embed_texts([query_text], model_name=self.model_name)
        faiss.normalize_L2(q_emb)
        D, I = self._index.search(q_emb.astype('float32'), topk)
        results = []
        for score, idx in zip(D[0], I[0]):
            meta = self._metadatas[idx]
            results.append((meta, float(score)))
        return results
