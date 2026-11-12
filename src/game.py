from enum import Enum
import numpy as np

class Action(Enum):
    UP = 0
    LEFT = 1
    RIGHT = 2
    DOWN = 3

class Game:
    def __init__(self):
        self.state = State(np.array(
            [[0, 3, 0, 2],
             [3, 0, 1, 1],
             [0, 2, 3, 0],
             [1, 1, 0, 0],
            ],
            dtype=int,
        ), 1)
    
    def move(self, action: Action):
        move_mask = self._move_mask(action)

        if not np.any(move_mask):
            print("Can't move in that direction.")
            return

    def done(self):
        zeros = self.state.board == 0
        if np.any(zeros):
            return False

        for action in enumerate(Action):
            move_mask = self._move_mask(action)
            if np.any(move_mask):
                return False
        
        return True

    def _move_mask(self, action):
        board = self.state.board
        shifted = np.zeros_like(board)
        if action == Action.UP:
            shifted[:-1, :] = board[1:, :]
        elif action == Action.DOWN:
            shifted[1:, :] = board[:-1, :]
        elif action == Action.LEFT:
            shifted[:, :-1] = board[:, 1:]
        elif action == Action.RIGHT:
            shifted[:, 1:] = board[:, :-1]

        moves_into_zero = (board == 0) & (shifted > 0)
        combine_to_three = (board != 0) & (shifted != 0) & ((board + shifted) == 3)
        doubles = (board >= 3) & (shifted == board)

        return moves_into_zero | combine_to_three | doubles
    

class State:
    def __init__(self, board: np.ndarray[(4, 4), int], next: int):
        self.board = board
        self.next = next
    
    def __str__(self):
        return f"""Next: {self.next}
Board:
{self.board}"""

def main():
    game = Game()

    while not game.done():
        print(game.state)

        direction = input("WASD?")
        direction = direction.lower()
        
        if direction == "w":
            game.move(Action.UP)
        elif direction == "a":
            game.move(Action.LEFT)
        elif direction == "s":
            game.move(Action.DOWN)
        elif direction == "d":
            game.move(Action.RIGHT)
        elif direction == "q":
            break
        else:
            print("Incorrect input.")

    print("GAME OVER")

if __name__ == "__main__":
    main()