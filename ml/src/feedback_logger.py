"""Append-only storage for user corrections."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

FIELDS = (
    "timestamp",
    "email_id",
    "subject",
    "sender",
    "body",
    "received_at",
    "has_attachments",
    "is_from_vip",
    "predicted_label",
    "corrected_label",
)


def log_feedback(
    email: Mapping[str, Any],
    predicted_label: str,
    corrected_label: str,
    path: Path,
) -> None:
    """Append one correction, creating the CSV header when needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    should_write_header = not path.exists() or path.stat().st_size == 0
    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "email_id": email.get("email_id", ""),
        "subject": email.get("subject", ""),
        "sender": email.get("sender", ""),
        "body": email.get("body", ""),
        "received_at": email.get("received_at", ""),
        "has_attachments": bool(email.get("has_attachments", False)),
        "is_from_vip": bool(email.get("is_from_vip", False)),
        "predicted_label": predicted_label,
        "corrected_label": corrected_label,
    }
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        if should_write_header:
            writer.writeheader()
        writer.writerow(row)
