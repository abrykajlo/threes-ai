import torch
import torch.optim as optim

import numpy as np

from argparse import ArgumentParser

from model import ThreesModel
from game import Game, Action

def main():
    parser = ArgumentParser()
    parser.add_argument("--buffer_size", type=int)
    parser.add_argument("--episodes", type=int)
    parser.add_argument("--epsilon", type=float)

    args = parser.parse_args()
    buffer_size = args.buffer_size
    episodes = args.episodes
    epsilon = args.epsilon


    model = ThreesModel()
    replay_buffer = ExperienceReplayBuffer(buffer_size)
    game = Game()

    for episode in range(0, args.episodes):
        phi_state = phi(game.state)
        while not game.done():
            if np.random.random() < epsilon:
                action = Action(np.random.randint(0, len(Action)))
            else:
                action = Action(model())
            
            game.move(action)
            phi_state_next = phi(game.state)

            # store experience
            replay_buffer.record(phi_state, action, reward, phi_state_next, done)

            # sample minibatch from replay buffer
            batch = replay_buffer.sample()

            # set y

        game = Game() # reset

def phi():
    pass

class ExperienceReplayBuffer:
    def __init__(self, buffer_size):
        self.state = np.ndarray((4, 4, buffer_size))
        self.action
        self.state_prime
        self.reward
        self.done
        self.curr_exp = 0
        self.buffer_size = buffer_size
    
    def record(self):
        pass

if __name__ == "__main__":
    main()