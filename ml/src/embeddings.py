"""Local text embeddings based on TF-IDF."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer

from .feature_extraction import email_text


def create_vectorizer() -> TfidfVectorizer:
    """Create a lightweight vectorizer that requires no external API."""
    return TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=4000,
        min_df=1,
        strip_accents="unicode",
        sublinear_tf=True,
    )


def email_documents(emails: Iterable[Mapping[str, Any]]) -> list[str]:
    """Convert structured emails into vectorizer input documents."""
    return [email_text(email) for email in emails]
