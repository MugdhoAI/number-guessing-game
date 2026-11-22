"""
Tests for the CLI entry point in main.py: leaving the game mid-prompt
should exit cleanly, whether the player presses Ctrl+C or the input
stream simply ends (Ctrl+D, or piped stdin running out).

Run with:
    python -m unittest discover tests
"""

import io
import random
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from main import ask_play_again, get_valid_guess, main


class TestAskPlayAgain(unittest.TestCase):

    def run_ask_play_again(self, answers):
        with mock.patch("builtins.input", side_effect=answers), \
                redirect_stdout(io.StringIO()):
            return ask_play_again()

    def test_yes_starts_another_round(self):
        self.assertTrue(self.run_ask_play_again(["y"]))

    def test_full_word_yes_is_accepted(self):
        self.assertTrue(self.run_ask_play_again(["YES"]))

    def test_no_ends_the_game(self):
        self.assertFalse(self.run_ask_play_again(["n"]))

    def test_invalid_answer_is_asked_again(self):
        self.assertTrue(self.run_ask_play_again(["maybe", "y"]))


class TestPlayAgainLoop(unittest.TestCase):

    def setUp(self):
        # Keep played games out of the real best_scores.json.
        self.tmpdir = tempfile.TemporaryDirectory()
        self.scores_file = Path(self.tmpdir.name) / "best_scores.json"
        self._patcher = mock.patch("main.SCORES_FILE", self.scores_file)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()
        self.tmpdir.cleanup()

    def test_winning_then_declining_plays_once(self):
        # Target fixed at 42, so the first guess wins and "n" ends it.
        with mock.patch("sys.argv", ["main.py", "--difficulty", "easy"]), \
                mock.patch("main.generate_target", return_value=42), \
                mock.patch("builtins.input", side_effect=["42", "n"]), \
                redirect_stdout(io.StringIO()) as out:
            main()
        self.assertIn("Correct!", out.getvalue())
        self.assertIn("You got it in 1 attempt(s)", out.getvalue())

    def test_winning_then_accepting_plays_twice(self):
        # Two winning rounds: guess 42, say yes, guess 42 again, say no.
        with mock.patch("sys.argv", ["main.py", "--difficulty", "easy"]), \
                mock.patch("main.generate_target", return_value=42), \
                mock.patch("builtins.input", side_effect=["42", "y", "42", "n"]), \
                redirect_stdout(io.StringIO()) as out:
            main()
        self.assertEqual(out.getvalue().count("Correct!"), 2)


class TestGetValidGuess(unittest.TestCase):

    def run_get_valid_guess(self, answers, low=1, high=100):
        with mock.patch("builtins.input", side_effect=answers), \
                redirect_stdout(io.StringIO()) as out:
            value = get_valid_guess(low, high)
        return value, out.getvalue()

    def test_non_numeric_input_is_asked_again(self):
        value, output = self.run_get_valid_guess(["abc", "42"])
        self.assertEqual(value, 42)
        self.assertIn("not a whole number", output)

    def test_out_of_range_input_is_asked_again(self):
        value, output = self.run_get_valid_guess(["0", "101", "42"])
        self.assertEqual(value, 42)
        self.assertEqual(output.count("Out of range"), 2)

    def test_blank_input_is_asked_again(self):
        value, _ = self.run_get_valid_guess(["   ", "7"])
        self.assertEqual(value, 7)

    def test_boundary_values_are_accepted(self):
        self.assertEqual(self.run_get_valid_guess(["1"])[0], 1)
        self.assertEqual(self.run_get_valid_guess(["100"])[0], 100)


class TestSeededGame(unittest.TestCase):

    def test_same_seed_gives_same_target(self):
        # The seeded target is known up front, so feed eight wrong
        # guesses and check the revealed number matches it.
        expected = random.Random(7).randint(1, 100)
        guesses = [n for n in range(1, 101) if n != expected][:8]
        inputs = [str(g) for g in guesses] + ["n"]
        with mock.patch("sys.argv", ["main.py", "--seed", "7"]), \
                mock.patch("builtins.input", side_effect=inputs), \
                redirect_stdout(io.StringIO()) as out:
            main()
        self.assertIn(f"The number was {expected}", out.getvalue())


class TestCleanExit(unittest.TestCase):

    def run_main_with_input_error(self, error):
        with mock.patch("sys.argv", ["main.py"]), \
                mock.patch("builtins.input", side_effect=error), \
                redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as ctx:
                main()
        return ctx.exception.code

    def test_eof_from_input_exits_cleanly(self):
        # Regression test: EOFError used to escape main() and crash
        # with a traceback whenever stdin closed mid-game.
        self.assertEqual(self.run_main_with_input_error(EOFError), 0)

    def test_keyboard_interrupt_still_exits_cleanly(self):
        self.assertEqual(self.run_main_with_input_error(KeyboardInterrupt), 0)


if __name__ == "__main__":
    unittest.main()
