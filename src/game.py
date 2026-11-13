from enum import Enum
import numpy as np
import random

class Action(Enum):
    UP = 0
    LEFT = 1
    RIGHT = 2
    DOWN = 3

class Game:
    def __init__(self):
        self.state = State(np.zeros((4, 4), dtype=int), 0)
        # insert 9 ints from deck
        self._shuffle_deck()
        for _ in range(0, 9):
            empty_spaces = self.state.board == 0
            coords = np.where(empty_spaces)
            coord_idx = np.random.randint(0, coords[0].shape[0])
            self.state.board[coords[0][coord_idx], coords[1][coord_idx]] = self.deck.pop()
        
        self.state.next = self.deck.pop()

    def move(self, action: Action):
        move_mask = self._move_mask(action)
        same_mask = np.logical_not(move_mask) # which elements should remain the same

        if not np.any(move_mask):
            print("Can't move in that direction.")
            return

        match action:
            case Action.UP:
                opposite = Action.DOWN
            case Action.DOWN:
                opposite = Action.UP
            case Action.LEFT:
                opposite = Action.RIGHT
            case Action.RIGHT:
                opposite = Action.LEFT

        same_move_mask = Game._shift(move_mask, opposite) # which elements just move and dont combine
        
        shifted = Game._shift(self.state.board, action)

        new_board = np.zeros_like(self.state.board)
        new_board[same_mask] = self.state.board[same_mask]
        new_board[move_mask] = (self.state.board + shifted)[move_mask]
        new_board[same_move_mask] = shifted[same_move_mask]

        self.state.board = new_board

        self._place_next(move_mask, action)
        self._new_next()

    def done(self):
        zeros = self.state.board == 0
        if np.any(zeros):
            return False

        for action in enumerate(Action):
            move_mask = self._move_mask(action)
            if np.any(move_mask):
                return False
        
        return True

    def _place_next(self, move_mask, action):
        next = self.state.next

        # get a boolean mask with an edge of True corresponding to where
        # numbers may appear
        edge_mask = np.ones_like(move_mask)
        edge_mask = Game._shift(edge_mask, action)
        edge_mask = np.logical_not(edge_mask)
        edge_mask = edge_mask & move_mask # if move_mask has a column or row of False exclude it

        coords = np.where(edge_mask)

        # pick the index in coords
        picked_coord = np.random.randint(0, coords[0].shape[0])

        self.state.board[coords[0][picked_coord], coords[1][picked_coord]] = next


    def _new_next(self):
        if len(self.deck) == 0:
            self._shuffle_deck()
        self.state.next = self.deck.pop()

    def _move_mask(self, action):
        board = self.state.board
        shifted = Game._shift(board, action)

        moves_into_zero = (board == 0) & (shifted > 0)
        combine_to_three = (board != 0) & (shifted != 0) & ((board + shifted) == 3)
        doubles = (board >= 3) & (shifted == board)

        move_mask = moves_into_zero | combine_to_three | doubles

        reverse = action == Action.DOWN or action == Action.RIGHT
        axis = 0 if action == Action.UP or action == Action.DOWN else 1

        move_mask = np.flip(move_mask, axis=axis) if reverse else move_mask
        move_mask = np.logical_or.accumulate(move_mask, axis=axis)
        move_mask = np.flip(move_mask, axis=axis) if reverse else move_mask
        
        return move_mask

    def _shift(board, action):
        shifted = np.zeros_like(board)
        if action == Action.UP:
            shifted[:-1, :] = board[1:, :]
        elif action == Action.DOWN:
            shifted[1:, :] = board[:-1, :]
        elif action == Action.LEFT:
            shifted[:, :-1] = board[:, 1:]
        elif action == Action.RIGHT:
            shifted[:, 1:] = board[:, :-1]

        return shifted
    
    def _shuffle_deck(self):
        self.deck = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
        random.shuffle(self.deck)

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
    print(game.state)

if __name__ == "__main__":
    main()