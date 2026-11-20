#!/usr/bin/env python3
"""
Number Guessing Game
----------------------
The classic beginner project: the computer picks a random number,
you try to guess it, and get hints (higher/lower) until you run out
of attempts or guess correctly.

Usage:
    python main.py
    python main.py --difficulty hard
"""

import argparse
import json
import sys
from pathlib import Path

from game import generate_target, check_guess, max_attempts_for, DIFFICULTY_RANGES


SCORES_FILE = Path(__file__).with_name("best_scores.json")


def load_best_scores(scores_file=SCORES_FILE) -> dict:
    """
    Load the saved best scores from the scores file.

    Returns a dict mapping difficulty name to the fewest guesses used
    to win at that difficulty. A missing, unreadable, or invalid file
    returns an empty dict instead of crashing the game, since losing
    a saved score should never stop someone from playing.
    """
    try:
        data = json.loads(Path(scores_file).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}

    if not isinstance(data, dict):
        return {}

    scores = {}
    for difficulty, value in data.items():
        if difficulty in DIFFICULTY_RANGES and isinstance(value, int) and not isinstance(value, bool) and value > 0:
            scores[difficulty] = value
    return scores


def save_best_scores(scores: dict, scores_file=SCORES_FILE) -> None:
    """Save best scores to the scores file, ignoring write failures."""
    try:
        Path(scores_file).write_text(json.dumps(scores, indent=2, sort_keys=True), encoding="utf-8")
    except OSError:
        pass


def record_best_score(difficulty: str, attempts: int, scores_file=SCORES_FILE):
    """
    Record a winning score for a difficulty if it beats the saved best.

    Returns a tuple of the best score for that difficulty after the
    update and a flag that is True when this game set a new best.
    """
    scores = load_best_scores(scores_file)
    previous_best = scores.get(difficulty)

    if previous_best is not None and attempts >= previous_best:
        return previous_best, False

    scores[difficulty] = attempts
    save_best_scores(scores, scores_file)
    return attempts, True


def get_valid_guess(low: int, high: int) -> int:
    """
    Prompt the player until they enter a valid integer within range.
    Keeps asking on bad input instead of crashing the whole program
    on a typo, since that would be a frustrating way to lose a guess.
    """
    while True:
        raw = input(f"Enter your guess ({low}-{high}): ").strip()
        try:
            value = int(raw)
        except ValueError:
            print("That's not a whole number. Try again.")
            continue

        if value < low or value > high:
            print(f"Out of range. Pick a number between {low} and {high}.")
            continue

        return value


def play(difficulty: str, scores_file=SCORES_FILE) -> None:
    """Run one full game at the given difficulty."""
    low, high = DIFFICULTY_RANGES[difficulty]
    target = generate_target(difficulty)
    attempts_allowed = max_attempts_for(difficulty)

    print(f"\nI'm thinking of a number between {low} and {high}.")
    print(f"You have {attempts_allowed} attempts. Good luck!")

    best = load_best_scores(scores_file).get(difficulty)
    if best is not None:
        print(f"Best score for {difficulty}: {best} attempt(s). Try to beat it!")
    print()

    for attempt_number in range(1, attempts_allowed + 1):
        guess = get_valid_guess(low, high)
        result = check_guess(guess, target)

        if result.is_correct:
            print(f"\nCorrect! The number was {target}. You got it in {attempt_number} attempt(s).")
            best, is_new_best = record_best_score(difficulty, attempt_number, scores_file)
            if is_new_best:
                print(f"New best score for {difficulty}: {best} attempt(s).")
            else:
                print(f"Best score for {difficulty}: {best} attempt(s).")
            return

        remaining = attempts_allowed - attempt_number
        direction = "higher" if result.hint == "higher" else "lower"
        print(f"Go {direction}. ", end="")
        if remaining > 0:
            print(f"{remaining} attempt(s) left.\n")
        else:
            print()

    print(f"\nOut of attempts. The number was {target}. Better luck next time!")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Play a number guessing game against the computer."
    )
    parser.add_argument(
        "--difficulty", default="medium", choices=list(DIFFICULTY_RANGES.keys()),
        help="Game difficulty, which changes the number range and attempts allowed. Default: medium."
    )
    args = parser.parse_args()

    try:
        play(args.difficulty)
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C interrupts the prompt, and Ctrl+D (or a closed/piped
        # stdin) raises EOFError from the same input() call. Both mean
        # "the player left mid-game", so both exit the same clean way
        # instead of dumping a traceback.
        print("\n\nGame interrupted. See you next time.")
        sys.exit(0)


if __name__ == "__main__":
    main()
