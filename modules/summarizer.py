"""Simple summarizer using transformers' pipeline if available; otherwise a naive extractor."""
from typing import List
import os

class Summarizer:
    def __init__(self, model_name: str = 'sshleifer/distilbart-cnn-12-6'):
        self.model_name = model_name
        self._use_transformers = False
        try:
            from transformers import pipeline
            # try to create summarization pipeline lazily
            self._pipe = pipeline('summarization', model=self.model_name, truncation=True)
            self._use_transformers = True
        except Exception:
            self._pipe = None
            self._use_transformers = False

    def summarize(self, text: str, max_length: int = 200) -> str:
        if not text or len(text.split()) < 50:
            # short text -> return as-is
            return text.strip()
        if self._use_transformers and self._pipe is not None:
            try:
                out = self._pipe(text, max_length=max_length, min_length=30)
                return out[0]['summary_text']
            except Exception as e:
                # fallback
                pass
        # naive summarization: take the top-n sentences by length / presence of keywords
        sents = [s.strip() for s in text.split('.') if s.strip()]
        # take first 6 sentences as a quick summary
        return ('. '.join(sents[:6]) + ('.' if sents[:6] else '')).strip()
