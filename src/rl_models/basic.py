from src.environment import PyBoyEnv
from collections import defaultdict
import random
import numpy as np


class BasicRL:
    def __init__(self, env: PyBoyEnv):
        self.env = env
        self.state_dict = {}
        self.path = []
        self.e = 0.3
    
    def get_action(self, obs):
        state = tuple(obs.values())
        if state not in self.state_dict:
            self.state_dict[state] = np.array([[1, 1, 1], [2, 2, 2]])
            action = self.env.action_space.sample()
        elif random.random() > self.e:
            s = self.state_dict[state]
            action = np.argmax(s[0] / s[1])
        else:
            action = self.env.action_space.sample()
        self.path.append((state, action))
        return action
    
    def apply_reward(self, obs, reward):
        pass
    
    def apply_end_reward(self, reward):
        for s, a in self.path:
            d = self.state_dict[s]
            d[:, a] += reward, 1

    def run_training_session(self):
        obs, _ = self.env.reset()
        self.path.clear()

        terminated = False
        reward = 0
        t = 0
        while not terminated and t < 100:
            action = self.get_action(obs)
            obs, reward, terminated, _, _ = self.env.step(action)
            self.apply_reward(obs, reward)
            t += 1
            print(f"turn {t} complete")

        print(f"apply reward {reward} to path {self.path}")
        self.apply_end_reward(reward)