"""Train and persist the local email-priority classifier."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import joblib
from scipy.sparse import csr_matrix, hstack
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

from .embeddings import create_vectorizer, email_documents
from .feature_extraction import extract_feature_matrix

ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "data" / "seed_emails.json"
FEEDBACK_PATH = ROOT / "data" / "feedback_log.csv"
MODEL_PATH = ROOT / "models" / "priority_ranker.joblib"
LABELS = {"Urgent", "Medium", "Minor"}


def load_training_data() -> tuple[list[dict[str, Any]], list[str]]:
    """Load seed examples and valid user corrections."""
    with SEED_PATH.open(encoding="utf-8") as handle:
        seed_rows = json.load(handle)

    emails = [{key: value for key, value in row.items() if key != "label"} for row in seed_rows]
    labels = [row["label"] for row in seed_rows]

    if FEEDBACK_PATH.exists():
        with FEEDBACK_PATH.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                label = row.get("corrected_label", "")
                if label not in LABELS:
                    continue
                emails.append(
                    {
                        "email_id": row.get("email_id", ""),
                        "subject": row.get("subject", ""),
                        "sender": row.get("sender", ""),
                        "body": row.get("body", ""),
                        "received_at": row.get("received_at", ""),
                        "has_attachments": row.get("has_attachments", "").lower() == "true",
                        "is_from_vip": row.get("is_from_vip", "").lower() == "true",
                    }
                )
                labels.append(label)
    return emails, labels


def train(model_path: Path = MODEL_PATH) -> Path:
    """Fit the ranker and save all preprocessing objects."""
    emails, labels = load_training_data()
    vectorizer = create_vectorizer()
    text_features = vectorizer.fit_transform(email_documents(emails))
    scaler = StandardScaler()
    numeric_features = scaler.fit_transform(extract_feature_matrix(emails))
    features = hstack([text_features, csr_matrix(numeric_features)])

    classifier = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
    )
    classifier.fit(features, labels)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "vectorizer": vectorizer,
            "scaler": scaler,
            "classifier": classifier,
        },
        model_path,
    )
    return model_path


if __name__ == "__main__":
    print(f"Saved model to {train()}")
