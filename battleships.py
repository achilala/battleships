from random import randint

class Board():
    """
    The single responsibility of this class is the board
    The Board size is dynamic and depends on the number of labels
    """
    COL_LABELS = (
         "1"
        ,"2"
        ,"3"
        ,"4"
        ,"5"
        ,"6"
        ,"7"
        ,"8"
        # ,"9"
        # ,"10"
    )
    ROW_LABELS = (
         "a"
        ,"b"
        ,"c"
        ,"d"
        ,"e"
        ,"f"
        ,"g"
        ,"h"
        # ,"i"
        # ,"j"
    )
    COL_INPUT_FORMAT = f"[{COL_LABELS[0]}-{COL_LABELS[-1]}]"
    ROW_INPUT_FORMAT = f"[{ROW_LABELS[0]}-{ROW_LABELS[-1]}]"
    INPUT_FORMAT = f"{ROW_INPUT_FORMAT}{COL_INPUT_FORMAT}"
    COL_SIZE = len(COL_LABELS)
    ROW_SIZE = len(ROW_LABELS)
    MIN_INPUT_SIZE = len(COL_LABELS[0]) + len(ROW_LABELS[0])
    MAX_BOARD_DISTANCE = (COL_SIZE + ROW_SIZE) - 2
    TILE_BLANK = " "
    TILE_EDGE = "|"    


    def get_col_labels() -> tuple:
        """
        This method returns column labels
        """
        return Board.COL_LABELS


    def get_row_labels() -> tuple:
        """
        This method returns row labels
        """
        return Board.ROW_LABELS


    def get_col_size() -> int:
        """
        This method returns column label size
        """
        return Board.COL_SIZE


    def get_row_size() -> int:
        """
        This method returns row label size
        """
        return Board.ROW_SIZE


    def get_min_input_size() -> int:
        """
        This method returns the minimum allowed input size for a valid coordinate on the board
        """
        return Board.MIN_INPUT_SIZE


    def get_max_board_distance() -> int:
        """
        This method returns the furthest possible distance between two coordinates on the board
        """
        return Board.MAX_BOARD_DISTANCE


    def get_input_format() -> str:
        """
        This method returns the allowed range of inputs
        """
        return Board.INPUT_FORMAT


    def create() -> list:
        """
        This method generates a board based on the size of the column and row labels
        """
        return [[Board.TILE_BLANK] * Board.COL_SIZE for _ in range(Board.ROW_SIZE)]


    def display(board: list, board_title: str) -> None:
        """
        This method displays a board in a formatted and presentable manner and can include a title
        """
        col_label_formatted = " ".join(Board.COL_LABELS)
        row_label_formatted = ""
        row_label_index = 0

        print(f"\n   {col_label_formatted}")
        
        for row in board:
            row_label_formatted = Board.ROW_LABELS[row_label_index].rjust(2, " ")
            print(f"{row_label_formatted}{Board.TILE_EDGE}{Board.TILE_EDGE.join(row)}{Board.TILE_EDGE}")
            row_label_index += 1

        split_in_half = 0.5
        title_padding_size = int(Board.COL_SIZE * split_in_half) + len(board_title)
        board_name = board_title.rjust(title_padding_size, " ")
        print(f"{board_name}\n")


    def place_icon(board: list, location: tuple, icon: str) -> None:
        """
        This method is useful for writing and/or removing icons on/from a board
        Removed icons are simply replaced with a blank tile
        """
        ship_col, ship_row = location
        board[ship_row][ship_col] = icon


    def remove_icon(board: list, location: tuple) -> None:
        """
        This method is useful for writing and/or removing icons on/from a board
        Removed icons are simply replaced with a blank tile
        """
        ship_col, ship_row = location
        board[ship_row][ship_col] = Board.TILE_BLANK


class Battleships():

    def __init__(
             self
            ,num_of_ships: int = 2
            ,num_of_total_guesses: int = 20
            ,show_hidden_board: bool = False
        ) -> None:
        """
        This constructor defines class variables and initializes their state
        Number of ships, total guesses are paramertized and assigned at runtime
        The hidden board can also be displayed at runtime for testing purposes
        """
        self.NUM_OF_SHIPS = num_of_ships
        self.NUM_OF_TOTAL_GUESSES = num_of_total_guesses
        self.SHOW_HIDDEN_BOARD = show_hidden_board

        self.HIDDEN_BOARD = Board.create()
        self.PLAYING_BOARD = Board.create()

        self.SHIP_ICON = "s"
        self.HIT_ICON = "@"
        self.MISS_ICON = "x"

        self.HIT = "Hit!"
        self.HOT = "Hot"
        self.WARM = "Warm"
        self.COLD = "Cold"

        # chose a set because like dict, and unlike tuple or lists, they don't contain duplicate values
        self.SHIPS_LIST = set()
        # chose a list because unlike sets they are ordered
        self.GUESS_LIST = []
        self.NUM_OF_GUESSES = 0
        self.NUM_OF_SUNK_SHIPS = 0


    def display_hidden_board(self) -> None:
        """
        This method displays the hidden board
        """
        Board.display(self.HIDDEN_BOARD, "Hidden Board")


    def display_playing_board(self) -> None:
        """
        This method displays the playing board
        When the flag show_hidden_board is set to True displays the hidden board as well
        """
        if self.SHOW_HIDDEN_BOARD:
            self.display_hidden_board()

        Board.display(self.PLAYING_BOARD, "Playing Board")


    def display_score_board(self, stdout: str) -> None:
        """
        This method displays the score board
        """
        print(f"""
-- -- -- Score Board -- -- --
Ships sunk: {self.NUM_OF_SUNK_SHIPS} of {self.NUM_OF_SHIPS}
Guesses left: {self.NUM_OF_TOTAL_GUESSES - self.NUM_OF_GUESSES} of {self.NUM_OF_TOTAL_GUESSES}
Accuracy: {self.NUM_OF_SUNK_SHIPS / self.NUM_OF_GUESSES * 100}%
Guesses: {" ".join(self.GUESS_LIST)}

{stdout}
-- -- -- -- -- -- -- -- -- --
        """)


    def generate_random_ship_locations(self) -> None:
        """
        This method generates random ship locations and adds them to a list of ships
        """
        while len(self.SHIPS_LIST) < self.NUM_OF_SHIPS:
            ship_col, ship_row = randint(0, Board.get_col_size() - 1), randint(0, Board.get_row_size() - 1)
            self.SHIPS_LIST.add((ship_col, ship_row))


    def place_ships_on_hidden_board(self) -> None:
        """
        This method places randomly generated ships on the hidden board
        """
        self.generate_random_ship_locations()

        for ship_location in self.SHIPS_LIST:
            Board.place_icon(
                 board = self.HIDDEN_BOARD
                ,location = ship_location
                ,icon = self.SHIP_ICON
            )


    def prompt_for_guess(self) -> str:
        """
        This method prompts the user for a guess of a ship's location and returns the valid input
        It also verifies that the format of the guess is valid otherwise keeps prompting
        Valid inputs are then added to the "guess list", excuse the pun :)
        """        
        prompt_1st = f"\nPlease guess a ship's location: "
        prompt_nth = f"\nInvalid entry provided, please re-try in this format {Board.get_input_format()} i.e d6: "
        prompt_guessed_already = "\nYou've guessed that one already, please try another: "
        
        guessed_location = input(prompt_1st).lower()

        while len(guessed_location) < Board.get_min_input_size() or guessed_location[0] not in Board.get_row_labels() or guessed_location[1:] not in Board.get_col_labels() or guessed_location in self.GUESS_LIST:
            if guessed_location in self.GUESS_LIST:
                guessed_location = input(prompt_guessed_already).lower()
            else:
                guessed_location = input(prompt_nth).lower()

        self.GUESS_LIST.append(guessed_location)
        return guessed_location


    def translate_input_to_board_location(self, guessed_location: str) -> tuple:
        ship_col = Board.get_col_labels().index(guessed_location[1:])
        ship_row = Board.get_row_labels().index(guessed_location[0])
        return (ship_col, ship_row)


    def distance_to_nearest_ship(self, guessed_location: tuple) -> str:
        """
        This method determines the distance between the guessed location and the nearest ship
        The user enters a co-ordinate, for example d6 and the computer locates the nearest ship to that co-ordinate
        and tells them they're "hot" if they're 1 to 2 cells away, "warm" if they're 3 to 4 cells away, or "cold" if they're further away.

        For instance, d6 is 3 cells away from c8 because (3 - 2) + (7 - 5) = 3, so they'd be told they were "warm"
        Returns "hit" when distance is 0
        """
        nearest_ship = Board.get_max_board_distance()
        guessed_ship_col, guessed_ship_row = guessed_location

        for ship in self.SHIPS_LIST:
            ship_col, ship_row = ship
            ship_distance = abs(guessed_ship_col - ship_col) + abs(ship_row - guessed_ship_row)
            nearest_ship = min(nearest_ship, ship_distance)
            
        if nearest_ship == 0:
            return self.HIT
        elif nearest_ship in [1, 2]:
            return self.HOT
        elif nearest_ship in [3, 4]:
            return self.WARM
        else:
            return self.COLD


    def play(self):
        """
        This method starts the game
        """
        print(f"""
Welcome to Battleship

How to play:
    - You're allowed a total of {self.NUM_OF_TOTAL_GUESSES} guesses to sink {self.NUM_OF_SHIPS} ships
    - At the bottom of the Score Baord, you'll see the result of your guess as either:
        - "{self.HIT}" if 0 cells away
        - "{self.HOT}" if 1 to 2 cells away
        - "{self.WARM}" if 3 to 4 cells away
        - or "{self.COLD}" if further away
    - The icon for a hit is "{self.HIT_ICON}" and "{self.MISS_ICON}" for a miss
    - Guesses should be provided starting with the letter of the board and then the number
      in this format {Board.get_input_format()} i.e d6
    - Invalid or repeat inputs don't count as guesses, you'll be prompted to try again

Enjoy the game!
        """)
        self.place_ships_on_hidden_board()
        self.display_playing_board()

        while self.NUM_OF_GUESSES < self.NUM_OF_TOTAL_GUESSES:
            guessed_location = self.translate_input_to_board_location(
                self.prompt_for_guess()
            )
            guess = self.distance_to_nearest_ship(guessed_location)

            if guess == self.HIT:
                self.SHIPS_LIST.remove(guessed_location)
                self.NUM_OF_SUNK_SHIPS += 1
                Board.place_icon(
                     board = self.PLAYING_BOARD
                    ,location = guessed_location
                    ,icon = self.HIT_ICON
                )
                Board.remove_icon(
                     board = self.HIDDEN_BOARD
                    ,location = guessed_location
                )

            else:
                Board.place_icon(
                     board = self.PLAYING_BOARD
                    ,location = guessed_location
                    ,icon = self.MISS_ICON
                )

            self.display_playing_board()
            self.NUM_OF_GUESSES += 1

            if self.NUM_OF_SUNK_SHIPS == self.NUM_OF_SHIPS:
                self.display_score_board(f"Congratulations! You've sunk all {self.NUM_OF_SHIPS} ships!")
                break

            self.display_score_board(guess)

        else:
            """
            When out of guesses display remaining ships on playing board
            """
            for ship_location in self.SHIPS_LIST:
                Board.place_icon(
                     board = self.PLAYING_BOARD
                    ,location = ship_location
                    ,icon = self.SHIP_ICON
                )

            self.display_playing_board()
            self.display_score_board("Sorry, you're out of guesses. Thanks for playing")