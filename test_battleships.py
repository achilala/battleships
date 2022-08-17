import unittest
from battleships import Battleships

class TestBattleships(unittest.TestCase):
    """
    Here's an example of how I tested the distance_to_nearest_ship method using TDD
    """
    # instantiate test object
    game = Battleships(
         num_of_ships=0
        ,num_of_total_guesses=0
        ,show_hidden_board=True
    )


    def test__distance_from_nearest_ship__hit(self):
        """
        The distance_to_nearest_ship method determines the distance between the guessed location and nearest ship.

        The user enters a co-ordinate, for example d6 and the computer locates the nearest ship to that co-ordinate
        and tells them they're "hot" if they're 1 to 2 cells away, "warm" if they're 3 to 4 cells away, or "cold" if they're further away.

        As an example, d6 is 0 cells away from d6 because abs(3 - 3) + abs(5 - 5) = 0, so they'd be told they it's a "Hit!"
        """
        guessed_input = "d6"
        ship1_input = "d6"
        guessed_location = self.game.translate_input_to_board_location(guessed_input)
        ship1_location = self.game.translate_input_to_board_location(ship1_input)

        self.game.SHIPS_LIST = set()
        self.game.SHIPS_LIST.add(ship1_location)
        
        expected_result = self.game.HIT
        actual_result = self.game.distance_to_nearest_ship(guessed_location)

        self.assertEqual(expected_result, actual_result)


    def test__distance_from_nearest_ship__hot(self):
        """
        As an example, d6 is 2 cells away from e5 because abs(3 - 4) + abs(4 - 5) = 2, so they'd be told they were "Hot"
        """
        guessed_input = "d6"
        ship1_input = "e5"
        guessed_location = self.game.translate_input_to_board_location(guessed_input)
        ship1_location = self.game.translate_input_to_board_location(ship1_input)

        self.game.SHIPS_LIST = set()
        self.game.SHIPS_LIST.add(ship1_location)
        
        expected_result = self.game.HOT
        actual_result = self.game.distance_to_nearest_ship(guessed_location)

        self.assertEqual(expected_result, actual_result)

        """
        In this example, d6 is 1 cells away from d5 because abs(3 - 3) + abs(4 - 5) = 1, so they'd be told they were still "Hot"
        """
        ship1_input = "d5"
        ship1_location = self.game.translate_input_to_board_location(ship1_input)

        self.game.SHIPS_LIST = set()
        self.game.SHIPS_LIST.add(ship1_location)
        
        expected_result = self.game.HOT
        actual_result = self.game.distance_to_nearest_ship(guessed_location)

        self.assertEqual(expected_result, actual_result)


    def test__distance_from_nearest_ship__warm(self):
        """
        As an example, d6 is three cells away from c8 because abs(3 - 2) + abs(7 - 5) = 3, so they'd be told they were "Warm"
        """
        guessed_input = "d6"
        ship1_input = "c8"
        guessed_location = self.game.translate_input_to_board_location(guessed_input)
        ship1_location = self.game.translate_input_to_board_location(ship1_input)

        self.game.SHIPS_LIST = set()
        self.game.SHIPS_LIST.add(ship1_location)
        
        expected_result = self.game.WARM
        actual_result = self.game.distance_to_nearest_ship(guessed_location)

        self.assertEqual(expected_result, actual_result)

        """
        In this example, d6 is 4 cells away from f4 because abs(3 - 5) + abs(3 - 5) = 4, so they'd be told they were still "Warm"
        """
        ship1_input = "f4"
        ship1_location = self.game.translate_input_to_board_location(ship1_input)

        self.game.SHIPS_LIST = set()
        self.game.SHIPS_LIST.add(ship1_location)
        
        expected_result = self.game.WARM
        actual_result = self.game.distance_to_nearest_ship(guessed_location)

        self.assertEqual(expected_result, actual_result)


    def test__distance_from_nearest_ship__cold(self):
        """
        In this example, d6 is 5 cells away from h7 because abs(3 - 7) + abs(6 - 5) = 5, so they'd be told they were "Cold"
        """
        guessed_input = "d6"
        ship1_input = "h7"
        guessed_location = self.game.translate_input_to_board_location(guessed_input)
        ship1_location = self.game.translate_input_to_board_location(ship1_input)

        self.game.SHIPS_LIST = set()
        self.game.SHIPS_LIST.add(ship1_location)
        
        expected_result = self.game.COLD
        actual_result = self.game.distance_to_nearest_ship(guessed_location)

        self.assertEqual(expected_result, actual_result)


if __name__ == "__main__":
    unittest.main()