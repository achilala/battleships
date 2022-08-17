from battleships import Battleships

game = Battleships(
     num_of_ships=3
    ,num_of_total_guesses=15
    ,show_hidden_board=True
)
game.play()