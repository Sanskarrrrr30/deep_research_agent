"""Simple multi-step reasoner:
Steps:
 1. Decompose query into sub-queries (very simple heuristic: split by 'and', ',', ';')
 2. Retrieve top chunks per sub-query
 3. Synthesize retrieved text (concatenate + summarizer)
"""
from typing import List, Tuple
import os

class Reasoner:
    def __init__(self, retriever):
        self.retriever = retriever
        from modules.summarizer import Summarizer
        self.summarizer = Summarizer()

    def _decompose(self, query: str) -> List[str]:
        # Very basic decomposition heuristic
        parts = [p.strip() for p in query.split(';') if p.strip()]
        if len(parts) == 1:
            parts = [p.strip() for p in query.replace(',', ';').split(';') if p.strip()]
        if len(parts) == 1:
            # further split by ' and ' if too long
            if ' and ' in query.lower():
                parts = [p.strip() for p in query.lower().split(' and ')]
            else:
                parts = [query]
        return parts

    def answer(self, query: str, topk_per_step:int=3) -> Tuple[str, str]:
        pieces = []
        for subq in self._decompose(query):
            hits = self.retriever.query(subq, topk=topk_per_step)
            texts = []
            for meta, score in hits:
                texts.append(f"(source: {meta.get('source')} chunk:{meta.get('chunk')} score:{score:.3f})\n" + meta.get('text_preview',''))
            if texts:
                synth = '\n\n'.join(texts)
                pieces.append(f"## Subquery: {subq}\n\n" + synth)
        combined = '\n\n'.join(pieces)
        summary = self.summarizer.summarize(combined)
        return combined, summary

    def answer_and_export(self, query: str, export_path: str = 'outputs/result.md') -> Tuple[str, str]:
        combined, summary = self.answer(query)
        md = []
        md.append(f"# Research Query\n\n**Query:** {query}\n\n")
        md.append("## Retrieved Evidence\n\n")
        md.append(combined)
        md.append("\n\n## Synthesized Summary\n\n")
        md.append(summary)
        md_text = '\n'.join(md)
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        with open(export_path, 'w', encoding='utf-8') as f:
            f.write(md_text)
        return md_text, summary
