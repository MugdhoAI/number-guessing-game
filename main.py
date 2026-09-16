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
import sys

from game import generate_target, check_guess, max_attempts_for, DIFFICULTY_RANGES


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


def play(difficulty: str) -> None:
    """Run one full game at the given difficulty."""
    low, high = DIFFICULTY_RANGES[difficulty]
    target = generate_target(difficulty)
    attempts_allowed = max_attempts_for(difficulty)

    print(f"\nI'm thinking of a number between {low} and {high}.")
    print(f"You have {attempts_allowed} attempts. Good luck!\n")

    for attempt_number in range(1, attempts_allowed + 1):
        guess = get_valid_guess(low, high)
        result = check_guess(guess, target)

        if result.is_correct:
            print(f"\nCorrect! The number was {target}. You got it in {attempt_number} attempt(s).")
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
    except KeyboardInterrupt:
        print("\n\nGame interrupted. See you next time.")
        sys.exit(0)


if __name__ == "__main__":
    main()
