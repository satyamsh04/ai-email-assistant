"""Deterministic numeric features for email-priority ranking."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Mapping

import numpy as np

URGENT_TERMS = (
    "urgent",
    "asap",
    "immediately",
    "deadline",
    "overdue",
    "final notice",
    "cannot access",
    "action required",
)
QUESTION_RE = re.compile(r"\?")
UPPER_WORD_RE = re.compile(r"\b[A-Z]{3,}\b")


def email_text(email: Mapping[str, Any]) -> str:
    """Combine fields used by the text vectorizer."""
    return " ".join(
        str(email.get(field, "") or "")
        for field in ("subject", "sender", "body")
    ).strip()


def extract_features(email: Mapping[str, Any]) -> np.ndarray:
    """Return model-ready numeric features for one email."""
    subject = str(email.get("subject", "") or "")
    body = str(email.get("body", "") or "")
    text = f"{subject} {body}"
    lowered = text.lower()
    received_at = _parse_datetime(email.get("received_at"))
    now = datetime.now(timezone.utc)
    age_hours = max(0.0, (now - received_at).total_seconds() / 3600.0)

    values = [
        min(len(subject), 200) / 200.0,
        min(len(body), 5000) / 5000.0,
        min(sum(lowered.count(term) for term in URGENT_TERMS), 5) / 5.0,
        min(len(QUESTION_RE.findall(text)), 5) / 5.0,
        min(len(UPPER_WORD_RE.findall(text)), 5) / 5.0,
        1.0 if bool(email.get("has_attachments")) else 0.0,
        1.0 if bool(email.get("is_from_vip")) else 0.0,
        min(age_hours, 168.0) / 168.0,
    ]
    return np.asarray(values, dtype=float)


def extract_feature_matrix(emails: list[Mapping[str, Any]]) -> np.ndarray:
    """Return a two-dimensional matrix for a list of emails."""
    if not emails:
        return np.empty((0, 8), dtype=float)
    return np.vstack([extract_features(email) for email in emails])


def _parse_datetime(value: Any) -> datetime:
    if not value:
        return datetime.now(timezone.utc)
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return datetime.now(timezone.utc)
