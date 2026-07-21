"""FastAPI application for local email-priority recommendations."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

import joblib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from scipy.sparse import csr_matrix, hstack

from .embeddings import email_documents
from .feature_extraction import extract_feature_matrix
from .feedback_logger import log_feedback

Priority = Literal["Urgent", "Medium", "Minor"]
ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "priority_ranker.joblib"
FEEDBACK_PATH = ROOT / "data" / "feedback_log.csv"

app = FastAPI(title="Email Recommendation Service", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:3000", "http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

_model = None
_model_mtime = None


class EmailInput(BaseModel):
    email_id: str = ""
    subject: str = ""
    sender: str = ""
    body: str = ""
    received_at: str | None = None
    has_attachments: bool = False
    is_from_vip: bool = False


class Recommendation(BaseModel):
    label: Priority
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str
    model: str


class FeedbackInput(BaseModel):
    email: EmailInput
    predicted_label: Priority
    corrected_label: Priority


def _load_model():
    global _model, _model_mtime
    if not MODEL_PATH.exists():
        return None
    mtime = MODEL_PATH.stat().st_mtime
    if _model is None or mtime != _model_mtime:
        _model = joblib.load(MODEL_PATH)
        _model_mtime = mtime
    return _model


def recommend(email: EmailInput) -> Recommendation:
    """Predict a label, falling back to transparent local rules."""
    model = _load_model()
    payload = email.model_dump()
    if model is None:
        return _rule_based_recommendation(email)

    text_features = model["vectorizer"].transform(email_documents([payload]))
    numeric = model["scaler"].transform(extract_feature_matrix([payload]))
    features = hstack([text_features, csr_matrix(numeric)])
    probabilities = model["classifier"].predict_proba(features)[0]
    best_index = int(probabilities.argmax())
    label = model["classifier"].classes_[best_index]
    return Recommendation(
        label=label,
        confidence=float(probabilities[best_index]),
        reason=f"The local ranker scored this email highest for {label}.",
        model="priority-ranker",
    )


def _rule_based_recommendation(email: EmailInput) -> Recommendation:
    text = f"{email.subject} {email.body}".lower()
    urgent_terms = ("urgent", "asap", "immediately", "deadline", "overdue", "final notice")
    medium_terms = ("please", "question", "request", "meeting", "review", "assignment")
    if email.is_from_vip or any(term in text for term in urgent_terms):
        return Recommendation(
            label="Urgent",
            confidence=0.72,
            reason="Time-sensitive wording or a VIP sender was detected.",
            model="rules-fallback",
        )
    if any(term in text for term in medium_terms) or "?" in text:
        return Recommendation(
            label="Medium",
            confidence=0.62,
            reason="The email appears to request attention or a response.",
            model="rules-fallback",
        )
    return Recommendation(
        label="Minor",
        confidence=0.58,
        reason="No time-sensitive or action-oriented signals were detected.",
        model="rules-fallback",
    )


@app.get("/health")
def health() -> dict[str, str | bool]:
    return {"status": "ok", "trained_model": MODEL_PATH.exists()}


@app.post("/recommend", response_model=Recommendation)
def recommendation_endpoint(email: EmailInput) -> Recommendation:
    return recommend(email)


@app.post("/feedback")
def feedback_endpoint(feedback: FeedbackInput) -> dict[str, bool]:
    log_feedback(
        feedback.email.model_dump(),
        feedback.predicted_label,
        feedback.corrected_label,
        FEEDBACK_PATH,
    )
    return {"saved": True}
