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

    for episode in range(0, episodes):
        game = Game()
        while not game.done():
            # select action
            if np.random.random() < epsilon:
                action = Action(np.random.randint(0, len(Action)))
            else:
                action = Action(Q(game.state.board, game.state.next))
            
            score = game.state.score()
            game.move(action)
            next_score = game.state.score()
            reward = next_score - score

            # store experience
            replay_buffer.record(game.state, action, reward)

            # sample minibatch from replay buffer
            states, actions, rewards, next_states, dones = replay_buffer.sample(batch_size)

            # set y
        replay_buffer.finish(game.state)

class ExperienceReplayBuffer:
    def __init__(self, buffer_size):
        self.board_state = np.zeros((buffer_size, 4, 4), dtype=int)
        self.next_state = np.zeros((buffer_size, 3), dtype=int)
        self.action = np.zeros(buffer_size, dtype=int)
        self.reward = np.zeros(buffer_size, dtype=float)
        self.done = np.zeros(buffer_size, dtype=bool)
        self.curr_exp = 0
        self.buffer_size = buffer_size
    
    def record(self, state, action, reward):
        if self.curr_exp < self.buffer_size:
            self.board_state[self.curr_exp] = state.board
            self.next_state[self.curr_exp] = state.next
            self.action[self.curr_exp] = action
            self.reward[self.curr_exp] = reward
            self.curr_exp += 1

    def finish(self, state):
        if self.curr_exp < self.buffer_size:
            self.board_state[self.curr_exp] = state.board
            self.curr_exp += 1
    
    def sample(self, batch_size):
        batch_size = min(batch_size, self.curr_exp)

if __name__ == "__main__":
    main()