from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

import numpy as np


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "04_gate0_accuracy.py"
SPEC = importlib.util.spec_from_file_location("gate0_accuracy", SCRIPT)
GATE0 = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(GATE0)


class Gate0AccuracyTests(unittest.TestCase):
    def test_always_fake_is_chance_on_balanced_data(self) -> None:
        labels = np.asarray([0] * 50 + [1] * 50)
        predictions = np.asarray([1] * 100)
        scores = np.asarray([1.0] * 100)

        result = GATE0.classification_metrics(labels, predictions, scores)

        self.assertEqual(result["status"], "COMPUTABLE")
        self.assertEqual(result["accuracy"], 0.5)
        self.assertEqual(result["balanced_accuracy"], 0.5)
        self.assertEqual(result["real_recall"], 0.0)
        self.assertEqual(result["fake_recall"], 1.0)
        self.assertEqual(
            GATE0.permutation_p_balanced_accuracy(labels, predictions, permutations=499, seed=7),
            1.0,
        )

    def test_single_class_is_blocked_instead_of_called_accuracy(self) -> None:
        labels = np.asarray([1] * 80)
        predictions = np.asarray([1] * 80)
        scores = np.asarray([2.0] * 80)

        result = GATE0.classification_metrics(labels, predictions, scores)

        self.assertEqual(result["status"], "BLOCKED_SINGLE_CLASS")
        self.assertIsNone(result["accuracy"])
        self.assertIsNone(result["balanced_accuracy"])
        self.assertEqual(result["available_class_recall"]["fake_recall"], 1.0)

    def test_auc_ties_are_half_credit(self) -> None:
        labels = np.asarray([0, 0, 1, 1])
        scores = np.asarray([0.1, 0.5, 0.5, 0.9])
        self.assertAlmostEqual(GATE0.roc_auc(labels, scores), 0.875)


if __name__ == "__main__":
    unittest.main()
