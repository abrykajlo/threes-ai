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
        if action == Action.UP and self._can_move_up():
            self._move_up()
            return
        
        elif action == Action.DOWN and self._can_move_down():
            self._move_down()
            return

        elif action == Action.LEFT and self._can_move_left():
            self._move_left()
            return

        elif action == Action.RIGHT and self._can_move_right():
            self._move_right()
            return

        print("Can't move in that direction.")

    def _move_up(self):
        pass

    def _move_left(self):
        pass
    
    def _move_down(self):
        pass

    def _move_right(self):
        pass

    def _can_move_up(self):
        pass

    def _can_move_left(self):
        pass

    def _can_move_down(self):
        pass

    def _can_move_right(self):
        pass
    
    def done(self):
        return not self._can_move_up and not self._can_move_right and not self._can_move_left and not self._can_move_down

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