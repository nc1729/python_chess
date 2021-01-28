# python_chess

This project is a Python 3 implementation of chess, for one or two players.

## Dependencies
This project requires the Pygame module to run; it's tested under version 1.9.6. I believe everything else is Python inbuilt modules.

## How to play
With Python 3 installed and on your PATH, pull the repository and run 'python3 chess.py' to play. It's one player by default (against an AI) but can be made two player by tweaking the Game class. Tweaking that class also lets you choose your colour (will make this a console option/ include it as part of a GUI at some point.)
When the game ends, the window will hang out for a few seconds, and then the program will stop.
Press U to undo your last move, and press S to dump the game state to a text file (useful for debugging!)

## The AI
It's not really an AI. It picks a random, legal move, and does that. This makes it a fairly docile opponent, but occasionally it does something clever. Try not to back it into a corner! (Should attach some kind of actual chess engine.)