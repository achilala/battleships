# Battleships

Your challenge is to implement this simplified game of Battleships using text input and output.

The computer randomly chooses the location of two single-cell "ships" on a board of 8 by 8 cells.  The user then has 20 guesses to find the two ships.

The user enters a co-ordinate, for example `3,5`, and the computer locates the nearest ship to that co-ordinate and tells them they're "hot" if they're 1 to 2 cells away, "warm" if they're 3 to 4 cells away, or "cold" if they're further away.

As an example, `3,5` is three cells away from `2,7` because (3 - 2) + (7 - 5) = 3, so they'd be told they were "warm".

If the user correctly guesses a ship's location, they're told they've got a hit and that ship is removed from the board.  The game ends when both ships have been hit by the user, or the user has used up their 20 guesses.

Some things to note:
* Write your code in a style that you consider to be production quality. 
* We're more interested in your logical thinking, process and coding style. Show us what you know about writing great software.
* Feel free to use your language of choice. We prefer C#, Java, JavaScript, TypeScript, or Python.
* Please include guidance on how to install and execute your solution.
* Please create a merge request when you are done.


## How to run the code
I chose to go with Python, and the code can be run from the CLI as follows:

### Play the game
```bash
python3 play_battleships.py
```

### Run tests
```bash
python3 test_battleships.py
```

### How To Instantiate a Game
You can override the default settings at runtime such as the number of ships and/or total number of guesses.
```py
from battleships import Battleships

game = Battleships(
     num_of_ships=3
    ,num_of_total_guesses=15
)
game.play()
```

You can choose to show the hidden board as well for testing or debugging purposes.
```py
from battleships import Battleships

game = Battleships(
     num_of_ships=3
    ,num_of_total_guesses=15
    ,show_hidden_board=True
)
game.play()
```