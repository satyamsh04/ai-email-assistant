import csv
import tempfile
import unittest
from pathlib import Path

from src.feature_extraction import extract_feature_matrix, extract_features
from src.feedback_logger import log_feedback


class FeatureExtractionTests(unittest.TestCase):
    def test_feature_shape_and_urgent_signal(self):
        urgent = extract_features(
            {"subject": "URGENT deadline", "body": "Please act immediately."}
        )
        normal = extract_features({"subject": "Newsletter", "body": "For information."})

        self.assertEqual(urgent.shape, (8,))
        self.assertGreater(urgent[2], normal[2])

    def test_empty_matrix_has_expected_width(self):
        self.assertEqual(extract_feature_matrix([]).shape, (0, 8))


class FeedbackLoggerTests(unittest.TestCase):
    def test_logger_creates_header_and_row(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "feedback.csv"
            log_feedback(
                {"email_id": "123", "subject": "Test"},
                "Minor",
                "Medium",
                path,
            )
            with path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["corrected_label"], "Medium")


if __name__ == "__main__":
    unittest.main()
