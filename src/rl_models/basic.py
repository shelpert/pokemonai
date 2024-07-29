from src.environment import PyBoyEnv
from collections import defaultdict
import random
import numpy as np
import csv
from abc import ABC, abstractmethod


class RL(ABC):
    def __init__(self, env: PyBoyEnv, data_fp: str = "data.csv"):
        self.env = env
        obs, info = self.env.reset()
        info |= self.get_info(obs)

        self.f = open(data_fp, "a")
        self.writer = csv.DictWriter(self.f, fieldnames=info.keys())
        self.writer.writeheader()

    @abstractmethod
    def get_info(self, obs):
        pass

    @abstractmethod
    def get_action(self, obs):
        pass

    def apply_reward(self, obs, reward):
        pass

    def apply_end_reward(self, obs, reward):
        pass

    def run_training_session(self):
        obs, info = self.env.reset()
        self.path.clear()

        self.save_row(obs, info)

        terminated = False
        reward = 0
        t = 0
        while not terminated and t < 100:
            action = self.get_action(obs)
            obs, reward, terminated, _, info = self.env.step(action)
            self.save_row(obs, info)

            self.apply_reward(obs, reward)
            t += 1
            print(f"turn {t} complete")

        print(f"apply reward {reward} to path {self.path}")
        self.apply_end_reward(reward)

    def save_row(self, obs, info):
        print(", ".join(f"{k!r}: {v!s}" for k,v in info.items()))
        self.writer.writerow(info | self.get_info(obs))
    
    def __del__(self):
        self.f.close()


class BasicRL(RL):
    def __init__(self, env: PyBoyEnv):
        self.state_dict = {}
        self.path = []
        self.e = 0.3
        super().__init__(env)

    def get_info(self, obs):
        state = tuple(obs.values())
        prob = self.state_dict.get(state, np.array([[0, 0, 0], [0, 0, 0]]))
        return {"win_prob": self.state_dict.get(state, prob.tolist())}

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
        # TODO account for pp
        print(state, action)
        return action

    def apply_end_reward(self, reward):
        for s, a in self.path:
            d = self.state_dict[s]
            d[:, a] += reward, 1
