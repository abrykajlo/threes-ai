import torch
import torch.optim as optim

import numpy as np

from argparse import ArgumentParser

from model import ThreesModel
from game import Game, Action

def main():
    parser = ArgumentParser()
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--buffer_size", type=int, default=10000)
    parser.add_argument("--discount_factor", type=float, default=0.5)
    parser.add_argument("--episodes", type=int, default=100)
    parser.add_argument("--epsilon", type=float, default=0.5)
    parser.add_argument("--target_update_freq", type=int, default=20)

    args = parser.parse_args()
    batch_size = args.batch_size
    buffer_size = args.buffer_size
    discount_factor = args.discount_factor
    episodes = args.episodes
    epsilon = args.epsilon
    target_update_freq = args.target_update_freq

    # initialize replay memory
    replay_buffer = ExperienceReplayBuffer(buffer_size)
    
    # initialize Q function
    Q = ThreesModel()

    # initialize target Q function
    Q_target = ThreesModel()
    Q_target.load_state_dict(Q.state_dict())

    optimizer = optim.Adam(Q.parameters())

    experiences = 0
    for _ in range(0, episodes):
        game = Game()
        while not game.done():
            # select action
            if np.random.random() < epsilon:
                action = Action(np.random.randint(0, len(Action)))
            else:
                action = Action(Q(game.state.board, game.state.next))
            
            state = game.state
            score = state.score()

            game.move(action)
            
            next_state = game.state
            next_score = next_state.score()
            reward = next_score - score

            if game.done():
                next_state = None

            # store experience
            replay_buffer[experiences] = (state, action, reward, next_state)
            experiences += 1

            # sample minibatch from replay buffer
            indices = np.arange(experiences)
            np.random.shuffle(indices)
            indices = indices[:experiences] if experiences < batch_size else indices[:batch_size]
            states, actions, rewards, next_states, dones = replay_buffer[indices]

            # set y
            not_dones = not dones
            y = np.zeros_like(dones, dtype=float)
            y[not_dones] = rewards[not_dones] + discount_factor * Q_target()
            y[dones] = rewards[dones]

class ExperienceReplayBuffer:
    def __init__(self, buffer_size):
        self.states = StateBuffer(buffer_size)
        self.actions = np.zeros(buffer_size, dtype=int)
        self.rewards = np.zeros(buffer_size, dtype=float)
        self.dones = np.zeros(buffer_size, dtype=bool)
    
    def __getitem__(self, indices):
        return self.states[indices], self.actions[indices], self.rewards[indices], self.states[indices + 1], self.dones[indices]

    def __setitem__(self, index, tuple):
        state = tuple[0]
        action = tuple[1]
        reward = tuple[2]
        next_state = tuple[3]

        # state
        self.states[index] = state
        self.actions[index] = action
        self.rewards[index] = reward

        # next state
        if next_state:
            self.states[index + 1] = next_state
            self.dones[index] = False
        else:
            self.dones[index] = True

    def __len__(self):
        return self.dones.shape[0]

class StateBuffer:
    def __init__(self, buffer_size):
        self.board = np.zeros((buffer_size, 4, 4), dtype=int)
        self.next = np.zeros((buffer_size, 3), dtype=int)

    def __setitem__(self, index, state):
        pass

    def __getitem__(self, indices):
        pass

if __name__ == "__main__":
    main()