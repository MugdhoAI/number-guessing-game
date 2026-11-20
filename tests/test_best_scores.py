"""
Tests for the persistent best score helpers in main.py.

Run with:
    python -m unittest discover tests
"""

import json
import tempfile
import unittest
from pathlib import Path

from main import load_best_scores, record_best_score, save_best_scores


class TestBestScores(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.scores_file = Path(self.tmpdir.name) / "best_scores.json"

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_missing_file_returns_empty_scores(self):
        self.assertEqual(load_best_scores(self.scores_file), {})

    def test_invalid_file_returns_empty_scores(self):
        self.scores_file.write_text("not json", encoding="utf-8")
        self.assertEqual(load_best_scores(self.scores_file), {})

    def test_non_dict_file_returns_empty_scores(self):
        self.scores_file.write_text(json.dumps([1, 2, 3]), encoding="utf-8")
        self.assertEqual(load_best_scores(self.scores_file), {})

    def test_unknown_difficulty_entries_are_ignored(self):
        self.scores_file.write_text(
            json.dumps({"easy": 3, "impossible": 1}), encoding="utf-8"
        )
        self.assertEqual(load_best_scores(self.scores_file), {"easy": 3})

    def test_save_and_load_round_trip(self):
        save_best_scores({"easy": 4, "hard": 7}, self.scores_file)
        self.assertEqual(load_best_scores(self.scores_file), {"easy": 4, "hard": 7})

    def test_first_win_records_best_score(self):
        best, is_new_best = record_best_score("medium", 5, self.scores_file)
        self.assertEqual(best, 5)
        self.assertTrue(is_new_best)
        self.assertEqual(load_best_scores(self.scores_file), {"medium": 5})

    def test_worse_score_does_not_replace_best(self):
        record_best_score("easy", 3, self.scores_file)
        best, is_new_best = record_best_score("easy", 6, self.scores_file)
        self.assertEqual(best, 3)
        self.assertFalse(is_new_best)
        self.assertEqual(load_best_scores(self.scores_file), {"easy": 3})

    def test_better_score_replaces_best(self):
        record_best_score("hard", 8, self.scores_file)
        best, is_new_best = record_best_score("hard", 4, self.scores_file)
        self.assertEqual(best, 4)
        self.assertTrue(is_new_best)
        self.assertEqual(load_best_scores(self.scores_file), {"hard": 4})

    def test_scores_are_kept_per_difficulty(self):
        record_best_score("easy", 2, self.scores_file)
        record_best_score("hard", 9, self.scores_file)
        self.assertEqual(load_best_scores(self.scores_file), {"easy": 2, "hard": 9})


if __name__ == "__main__":
    unittest.main()
