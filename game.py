"""
game.py

Core logic for the number guessing game. No input() or print() calls
live here on purpose, same separation used in every earlier project:
this module only makes decisions given a guess and a target number,
it never talks to the terminal directly. That means it can be tested
without simulating keyboard input at all.
"""

import random
from dataclasses import dataclass


@dataclass
class GuessResult:
    """Outcome of a single guess."""
    is_correct: bool
    hint: str  # "higher", "lower", or "correct"


DIFFICULTY_RANGES = {
    "easy": (1, 50),
    "medium": (1, 100),
    "hard": (1, 500),
}

MAX_ATTEMPTS_BY_DIFFICULTY = {
    "easy": 10,
    "medium": 8,
    "hard": 10,
}


def generate_target(difficulty: str) -> int:
    """
    Pick a random target number for the given difficulty.

    Args:
        difficulty: One of "easy", "medium", "hard".

    Returns:
        A random integer within that difficulty's range.

    Raises:
        ValueError: If difficulty isn't a recognized option.
    """
    if difficulty not in DIFFICULTY_RANGES:
        raise ValueError(f"Unknown difficulty '{difficulty}'. Choose from: {', '.join(DIFFICULTY_RANGES)}")

    low, high = DIFFICULTY_RANGES[difficulty]
    return random.randint(low, high)


def check_guess(guess: int, target: int) -> GuessResult:
    """
    Compare a guess against the target and return the outcome.

    Args:
        guess: The player's guessed number.
        target: The actual number to guess.

    Returns:
        A GuessResult indicating whether the guess was correct, and
        if not, whether the real answer is higher or lower.
    """
    if guess == target:
        return GuessResult(is_correct=True, hint="correct")
    if guess < target:
        return GuessResult(is_correct=False, hint="higher")
    return GuessResult(is_correct=False, hint="lower")


def max_attempts_for(difficulty: str) -> int:
    """Return the number of guesses allowed for a given difficulty."""
    if difficulty not in MAX_ATTEMPTS_BY_DIFFICULTY:
        raise ValueError(f"Unknown difficulty '{difficulty}'. Choose from: {', '.join(MAX_ATTEMPTS_BY_DIFFICULTY)}")
    return MAX_ATTEMPTS_BY_DIFFICULTY[difficulty]
