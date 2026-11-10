from enum import Enum

class Action(Enum):
    UP = 0
    LEFT = 1
    RIGHT = 2
    DOWN = 3

class Game:
    def __init__(self):
        self.state = State((
            (1,2,0,0),
            (0,0,0,0),
            (0,0,0,0),
            (0,0,0,0),
        ), 0)
    
    def move(self, action: Action):
        print(action)
    
    def done(self):
        return False

class State:
    Row = tuple[int, int, int, int]
    
    def __init__(self, board: tuple[Row, Row, Row, Row], next: int):
        self.board = board
        self.next = next
    
    def __str__(self):
        return f"""Next: {self.next}
Board:
{self.board[0]}
{self.board[1]}
{self.board[2]}
{self.board[3]}"""

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