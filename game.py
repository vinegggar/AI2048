import random as rd
import numpy as np


class GameLogic:

    def __init__(self, board=np.zeros((4, 4))):
        """
        Initialize the game
        """
        self.board = board
        self.score = 0
        self.is_over = False
        self.won = False

        # add two random tiles to the board
        if self.board.sum() == 0:
            self.add_random_tile()
            self.add_random_tile()

    def add_random_tile(self):
        """
        Selects a random empty tile and adds a 2 or 4 with 80% and 20% probability respectively
        """
        empty_tiles = np.argwhere(self.board == 0)
        if len(empty_tiles) > 0:
            i, j = rd.choice(empty_tiles)
            self.board[i, j] = 4 if rd.random() < 0.1 else 2

    def move(self, direction):
        """
        Move the board in the specified direction and add a new tile
        0: right, 1: up, 2: left, 3: down
        """
        match direction:
            case 0:
                self.move_right()
            case 1:
                self.move_up()
            case 2:
                self.move_left()
            case 3:
                self.move_down()
            case _:
                raise ValueError("Invalid direction")

    def merge_tiles(self, row):
        """
        Merge tiles in already moved row and update the score
        """
        for i in range(3, 0, -1):
            if row[i] == row[i - 1]:
                self.score += row[i] * 2
                row[i] *= 2
                row[i - 1] = 0
        return row

    def move_right(self):
        """
        Move the board to the right
        """
        # for each row, move all tiles to the right
        for i in range(4):
            # move non-zero tiles to the right
            non_zeros = self.board[i][self.board[i] != 0]
            zeros = np.zeros(4 - len(non_zeros))
            row = np.concatenate((zeros, non_zeros))
            # merge tiles
            row = self.merge_tiles(row)
            # move non-zero tiles to the right
            non_zeros = row[row != 0]
            zeros = np.zeros(4 - len(non_zeros))
            row = np.concatenate((zeros, non_zeros))
            self.board[i] = row

    def move_left(self):
        """
        Move the board to the left
        """
        # we need to flip the board, move right and flip it back
        self.board = np.flip(self.board, axis=1)
        self.move_right()
        self.board = np.flip(self.board, axis=1)

    def move_down(self):
        """
        Move the board down
        """
        # we need to transpose the board, move right and transpose it back
        self.board = np.transpose(self.board)
        self.move_right()
        self.board = np.transpose(self.board)

    def move_up(self):
        """
        Move the board up
        """
        # we need to transpose the board, move left and transpose it back
        self.board = np.transpose(self.board)
        self.move_left()
        self.board = np.transpose(self.board)

    def update_score(self, score):
        """
        Update the score
        """
        self.score += score

    def check_game_over(self):
        """
        Check if the game is over. The game is over if there are no empty tiles or if no tiles can be merged
        """
        # if there's an empty tile, the game is not over
        if 0 in self.board:
            return False
        # if board stays the same after moving in all directions, the game is over
        board_copy = GameLogic(self.board.copy())
        moves = [board_copy.move_right(), board_copy.move_up(), board_copy.move_left(), board_copy.move_down()]

        return all((board_copy == self.board).all() for board_copy in moves)

    def check_won(self):
        """
        Check if the game is won. The game is won if there is a 2048 tile
        """
        if max(self.board) >= 2048:
            return True
        return False

    def get_state(self):
        """
        Get the current state of the board
        """
        return self.board

    def get_score(self):
        """
        Get the current score
        """
        return self.score

    def is_valid_move(self, direction):
        """
        Check if the given move is valid
        """
        board_copy = GameLogic(self.board.copy())
        board_copy.move(direction)
        #if copy after move is the same as the original, the move is invalid
        return not (board_copy.board == self.board).all()

def play():
    """
    Play the game from user input
    """
    # initialize the game
    game = GameLogic()

    # play until the game is over
    while not game.is_over:
        # print the current state of the board
        print(game.board)
        print("Score: ", game.score)

        # get the next move from the user
        move = int(input("Enter next move (0: right, 1: up, 2: left, 3: down): "))


        # move the board and check if the move is valid
        while not game.is_valid_move(move):
            print("Invalid move!")
            move = int(input("Enter next move (0: right, 1: up, 2: left, 3: down): "))
        game.move(move)

        # add a new tile
        game.add_random_tile()

        # check if the game is over
        game.is_over = game.check_game_over()

        # check if the game is won
        game.won = game.check_won()

    # print the final state of the board
    print(game.board)
    print("Score: ", game.score)

    # print game over or won
    if game.won:
        print("You won!")
    else:
        print("Game over!")


if __name__ == "__main__":
    play()