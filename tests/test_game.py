"""
Tests for the number guessing game logic.

Run with:
    python -m unittest discover tests
"""

import unittest

from game import generate_target, check_guess, closeness, max_attempts_for, DIFFICULTY_RANGES


class TestCloseness(unittest.TestCase):

    def test_exact_guess_is_very_close(self):
        self.assertEqual(closeness(50, 50), "very close")

    def test_five_away_is_very_close(self):
        self.assertEqual(closeness(45, 50), "very close")
        self.assertEqual(closeness(55, 50), "very close")

    def test_fifteen_away_is_close(self):
        self.assertEqual(closeness(35, 50), "close")
        self.assertEqual(closeness(65, 50), "close")

    def test_sixteen_away_is_far(self):
        self.assertEqual(closeness(34, 50), "far")
        self.assertEqual(closeness(66, 50), "far")


class TestGenerateTarget(unittest.TestCase):

    def test_easy_target_within_range(self):
        for _ in range(50):  # run many times since it's random
            target = generate_target("easy")
            self.assertGreaterEqual(target, 1)
            self.assertLessEqual(target, 50)

    def test_hard_target_within_range(self):
        for _ in range(50):
            target = generate_target("hard")
            self.assertGreaterEqual(target, 1)
            self.assertLessEqual(target, 500)

    def test_invalid_difficulty_raises_error(self):
        with self.assertRaises(ValueError):
            generate_target("impossible")


class TestCheckGuess(unittest.TestCase):

    def test_correct_guess(self):
        result = check_guess(50, 50)
        self.assertTrue(result.is_correct)
        self.assertEqual(result.hint, "correct")

    def test_guess_too_low(self):
        result = check_guess(10, 50)
        self.assertFalse(result.is_correct)
        self.assertEqual(result.hint, "higher")

    def test_guess_too_high(self):
        result = check_guess(90, 50)
        self.assertFalse(result.is_correct)
        self.assertEqual(result.hint, "lower")


class TestMaxAttempts(unittest.TestCase):

    def test_known_difficulties_return_expected_values(self):
        self.assertEqual(max_attempts_for("easy"), 10)
        self.assertEqual(max_attempts_for("medium"), 8)
        self.assertEqual(max_attempts_for("hard"), 10)

    def test_invalid_difficulty_raises_error(self):
        with self.assertRaises(ValueError):
            max_attempts_for("nightmare")

    def test_all_difficulty_ranges_have_matching_attempt_entries(self):
        # Catches the case where someone adds a new difficulty to one
        # dict but forgets to add it to the other.
        self.assertEqual(set(DIFFICULTY_RANGES.keys()), set(max_attempts_for.__globals__["MAX_ATTEMPTS_BY_DIFFICULTY"].keys()))


if __name__ == "__main__":
    unittest.main()
