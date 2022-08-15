from random import randint

class Battleship():

    def __init__(
             self
            ,num_of_ships: int = 2
            ,num_of_total_guesses: int = 20
            ,show_hidden_board: bool = False
        ) -> None:
        """
        This constructor defines class variables and initializes their state
        Number of ships, total guesses are paramertized and assigned at runtime
        The Board size is dynamic and depends on the number of labels
        The hidden board can also be displayed at runtime for testing purposes
        """
        self.NUM_OF_SHIPS = num_of_ships
        self.NUM_OF_TOTAL_GUESSES = num_of_total_guesses
        self.SHOW_HIDDEN_BOARD = show_hidden_board

        self.BOARD_LABELS_COLS = [
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
        ]
        self.BOARD_LABELS_ROWS = [
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
        ]
        self.BOARD_SIZE_COLS = len(self.BOARD_LABELS_COLS)
        self.BOARD_SIZE_ROWS = len(self.BOARD_LABELS_ROWS)
        self.BOARD_BLANK_TILE = " "
        self.BOARD_TILE_EDGE = "|"

        self.HIDDEN_BOARD = self.create_board()
        self.PLAYING_BOARD = self.create_board()

        self.SHIP_ICON = "s"
        self.HIT_ICON = "@"
        self.MISS_ICON = "x"

        self.HIT = "Hit!"
        self.HOT = "Hot"
        self.WARM = "Warm"
        self.COLD = "Cold"

        # chose sets because like dict, and unlike tuple or lists, they don't contain duplicate values
        self.SHIPS_LIST = set()
        self.GUESS_LIST = set()
        self.NUM_OF_GUESSES = 0
        self.NUM_OF_SUNK_SHIPS = 0


    def create_board(self) -> list:
        """
        This method generates a board based on the size of the column and row labels
        """
        return [[self.BOARD_BLANK_TILE] * self.BOARD_SIZE_COLS for _ in range(self.BOARD_SIZE_ROWS)]


    def display_board(self, board: list, board_title: str) -> None:
        """
        This method displays a board in a formatted and presentable manner and can include a title
        """
        formatted_col_label = ""
        formatted_row_label = ""
        row_index = 0

        for label in self.BOARD_LABELS_COLS:
            formatted_col_label += f"{label} "

        print(f"\n   {formatted_col_label.strip()}")
        
        for row in board:
            formatted_row_label = self.BOARD_LABELS_ROWS[row_index].rjust(2, " ")
            print(f"{formatted_row_label}{self.BOARD_TILE_EDGE}{self.BOARD_TILE_EDGE.join(row)}{self.BOARD_TILE_EDGE}")
            row_index += 1

        divide_by_half = 2
        title_padding_size = int(self.BOARD_SIZE_COLS / divide_by_half) + len(board_title)
        board_name = board_title.rjust(title_padding_size, " ")
        print(f"{board_name}\n")

    def display_hidden_board(self) -> None:
        """
        This method displays the hidden board
        """
        self.display_board(self.HIDDEN_BOARD, "Hidden Board")


    def display_playing_board(self) -> None:
        """
        This method displays the playing board
        When the flag show_hidden_board is set to True displays the hidden board as well
        """
        if self.SHOW_HIDDEN_BOARD:
            self.display_hidden_board()

        self.display_board(self.PLAYING_BOARD, "Playing Board")


    def display_score_board(self, stdout: str) -> None:
        """
        This method displays the score board
        """
        print(f"""
-- -- -- Score Board -- -- --
Ships sunk: {self.NUM_OF_SUNK_SHIPS} of {self.NUM_OF_SHIPS}
Guesses left: {self.NUM_OF_TOTAL_GUESSES - self.NUM_OF_GUESSES} of {self.NUM_OF_TOTAL_GUESSES}
Accuracy: {self.NUM_OF_SUNK_SHIPS / self.NUM_OF_GUESSES * 100}%

{stdout}
-- -- -- -- -- -- -- -- -- --
        """)


    def generate_random_ship_locations(self) -> None:
        """
        This method generates random ship locations and adds them to a list of ships
        """
        while len(self.SHIPS_LIST) < self.NUM_OF_SHIPS:
            ship_col, ship_row = randint(0, self.BOARD_SIZE_COLS - 1), randint(0, self.BOARD_SIZE_ROWS - 1)
            self.SHIPS_LIST.add((ship_col, ship_row))


    def place_icon_on_board(self, board: list, location: tuple, icon: str) -> None:
        """
        This method is useful for writing and/or removing icons on/from a board
        Removed icons are simply replaced with a blank tile
        """
        ship_col, ship_row = location
        board[ship_row][ship_col] = icon


    def place_ships_on_hidden_board(self) -> None:
        """
        This method places randomly generated ships on the hidden board
        """
        self.generate_random_ship_locations()

        for ship_location in self.SHIPS_LIST:
            self.place_icon_on_board(
                 board = self.HIDDEN_BOARD
                ,location = ship_location
                ,icon = self.SHIP_ICON
            )


    def prompt_for_ship_location(self) -> str:
        """
        This method prompts the user for a guess of a ship's location and returns the valid input
        It also verifies that a valid entry is provided otherwise keeps prompting
        Valid inputs are then added to a "guess list" :)
        """
        col_first_label = self.BOARD_LABELS_COLS[0]
        col_last_label = self.BOARD_LABELS_COLS[-1]
        row_first_label = self.BOARD_LABELS_ROWS[0]
        row_last_label = self.BOARD_LABELS_ROWS[-1]
        min_input_size = len(col_first_label) + len(row_first_label)
        col_regex_format = f"[{col_first_label}-{col_last_label}]"
        row_regex_format = f"[{row_first_label}-{row_last_label}]"
        
        prompt_1st = f"\nPlease guess a ship's location: "
        prompt_nth = f"\nInvalid entry provided, please re-try in this format {row_regex_format}{col_regex_format} i.e d6: "
        prompt_guessed_already = "\nYou've guessed that one already, please try another: "
        
        guessed_ship_location = input(prompt_1st).lower()

        while len(guessed_ship_location) < min_input_size or guessed_ship_location[0] not in self.BOARD_LABELS_ROWS or guessed_ship_location[1:] not in self.BOARD_LABELS_COLS or guessed_ship_location in self.GUESS_LIST:
            if guessed_ship_location in self.GUESS_LIST:
                guessed_ship_location = input(prompt_guessed_already).lower()
            else:
                guessed_ship_location = input(prompt_nth).lower()

        self.GUESS_LIST.add(guessed_ship_location)
        return guessed_ship_location

    
    def translate_input_to_board_location(self, guessed_ship_location: str) -> tuple:
        ship_col = self.BOARD_LABELS_COLS.index(guessed_ship_location[1:])
        ship_row = self.BOARD_LABELS_ROWS.index(guessed_ship_location[0])
        return ship_col, ship_row


    def distance_to_nearest_ship(self, guessed_ship_location: tuple) -> str:
        """
        This method determines the distance between the guessed location and the nearest ship
        The user enters a co-ordinate, for example d6 and the computer locates the nearest ship to that co-ordinate
        and tells them they're "hot" if they're 1 to 2 cells away, "warm" if they're 3 to 4 cells away, or "cold" if they're further away.

        For instance, d6 is 3 cells away from c8 because (3 - 2) + (7 - 5) = 3, so they'd be told they were "warm"
        Returns "hit" when distance is 0
        """
        furthest_possible_distance = (self.BOARD_SIZE_COLS + self.BOARD_SIZE_ROWS) - 2
        nearest_ship = furthest_possible_distance
        guessed_ship_col, guessed_ship_row = guessed_ship_location

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
      in this format [a-h][1-8] i.e d6
    - Invalid or repeat inputs don't count as guesses, you'll be prompted to try again

Enjoy the game!
        """)
        self.place_ships_on_hidden_board()
        self.display_playing_board()

        while self.NUM_OF_GUESSES < self.NUM_OF_TOTAL_GUESSES:
            guessed_ship_location = self.translate_input_to_board_location(
                self.prompt_for_ship_location()
            )
            guess = self.distance_to_nearest_ship(guessed_ship_location)

            if guess == self.HIT:
                self.SHIPS_LIST.remove(guessed_ship_location)
                self.NUM_OF_SUNK_SHIPS += 1
                self.place_icon_on_board(
                     board = self.PLAYING_BOARD
                    ,location = guessed_ship_location
                    ,icon = self.HIT_ICON
                )
                self.place_icon_on_board(
                     board = self.HIDDEN_BOARD
                    ,location = guessed_ship_location
                    ,icon = self.BOARD_BLANK_TILE
                )

            else:
                self.place_icon_on_board(
                     board = self.PLAYING_BOARD
                    ,location = guessed_ship_location
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
                self.place_icon_on_board(
                     board = self.PLAYING_BOARD
                    ,location = ship_location
                    ,icon = self.SHIP_ICON
                )

            self.display_playing_board()
            self.display_score_board("Sorry, you're out of guesses. Thanks for playing")