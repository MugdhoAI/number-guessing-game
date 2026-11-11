"""
Tests for the CLI entry point in main.py: leaving the game mid-prompt
should exit cleanly, whether the player presses Ctrl+C or the input
stream simply ends (Ctrl+D, or piped stdin running out).

Run with:
    python -m unittest discover tests
"""

import io
import unittest
from contextlib import redirect_stdout
from unittest import mock

from main import main


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
