# Number Guessing Game

A classic terminal game where the computer picks a secret number and you try to guess it within a limited number of tries, getting a higher or lower hint after every guess.

## How it works

Run the game and pick a difficulty. Easy gives you a range of 1 to 50 with ten guesses. Medium is 1 to 100 with eight guesses. Hard is 1 to 500, also with ten guesses since the wider range needs a bit more room to work with. After every guess you are told whether to go higher or lower, and the game ends the moment you either guess correctly or run out of attempts.

## Getting started

You need Python 3.9 or newer and nothing else, since this project only uses the standard library.

Clone the repo and run it straight away.

```
git clone https://github.com/MugdhoAI/number-guessing-game
cd number-guessing-game
python main.py
```

Want a harder round right away.

```
python main.py --difficulty hard
```

## Project layout

The game logic lives in game.py on its own, completely separate from anything that reads keyboard input or prints to the screen. That part just answers questions like "is this guess correct" or "what number should the game pick this round." All of the actual back and forth with the player happens in main.py instead. Keeping those two apart means the logic can be tested on its own without ever needing to simulate someone typing at their keyboard. 

```
number-guessing-game
    main.py
    game.py
    tests
        test game.py
    gitignore
```

## Running the tests

```
python -m unittest discover tests
```

Nine tests cover the guessing logic itself: making sure generated numbers stay inside the chosen range, that higher and lower hints come back correctly, and that an unknown difficulty is rejected with a clear error instead of quietly doing something wrong.

## What I learned building this

This was a good reminder that not every project needs to be complicated to be worth building properly. The interesting part here was separating the game's decision making from the part that actually talks to the player, and thinking through what happens when someone types something that is not a number at all, which is an easy thing to overlook in a first draft.

## What could be added later

A running high score based on fewest guesses used. A mode where the player picks the number and the computer guesses instead, using a proper binary search. Maybe a simple graphical version down the line.

## About

Built by Mugdho, also known as All Asmaul Husnain.
GitHub: github.com/MugdhoAI
