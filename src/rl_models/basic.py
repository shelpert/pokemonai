from src.environment import PyBoyEnv
from collections import defaultdict
import random
import numpy as np
import csv
from abc import ABC, abstractmethod
import time
import pickle


class RL(ABC):
    def __init__(self, env: PyBoyEnv, data_fp: str = "data.csv"):
        self.env = env
        self.data_fp = data_fp

    @abstractmethod
    def get_info(self, obs):
        pass

    @abstractmethod
    def get_action(self, obs):
        pass

    def apply_reward(self, obs, reward):
        pass

    def apply_end_reward(self, obs, reward, t=0):
        pass

    def run_training_session(self):
        obs, info = self.env.reset()
        self.path.clear()

        with open(self.data_fp, "a") as f:
            self.writer = csv.DictWriter(f, fieldnames=info.keys() | self.get_info(obs).keys())
            self.writer.writeheader()
            
            def save_row(obs, info):
                self.writer.writerow(info | self.get_info(obs))

            save_row(obs, info)
            terminated = False
            reward = 0
            t = 0
            while not terminated and t < 100:
                action = self.get_action(obs, info)
                obs, reward, terminated, _, info = self.env.step(action)

                save_row(obs, info)

                self.apply_reward(obs, reward)
                t += 1

            f.write(f"END {reward} {t} {time.time()}")
            print(f"complete {reward=} {t=}")
            self.apply_end_reward(reward, t)
    
    def save_state(self, fp):
        pass

class BasicRL(RL):
    def __init__(self, env: PyBoyEnv):
        self.state_dict = {}
        self.path = []
        self.e = 0.3
        super().__init__(env)
    
    @classmethod
    def from_state_file(cls, env, fp):
        instance = cls(env)
        instance.load_state(fp)
        return instance

    def get_info(self, obs):
        state = tuple(obs.values())
        prob = self.state_dict.get(state, np.array([[0, 0, 0], [0, 0, 0]], dtype=float))
        return {"win_prob": prob.tolist()}

    def get_action(self, obs, info):
        usable = np.bool_(info["PP"][:3])
        state = tuple(obs.values())
        if state not in self.state_dict:
            self.state_dict[state] = np.array(
                [[0.1, 0.1, 0.1], [0.2, 0.2, 0.2]], dtype=float
            )
            action = self.env.action_space.sample(usable.astype(np.int8))
        elif random.random() > self.e:
            s = self.state_dict[state]
            action = np.argmax(s[0] / s[1] * usable)
        else:
            action = self.env.action_space.sample(usable.astype(np.int8))
        self.path.append((state, action))
        return action

    def apply_end_reward(self, reward, t):
        for s, a in self.path:
            d = self.state_dict[s]
            d[:, a] += max(reward - 0.01 * t, 0), 1 - 0.01 * t

    def load_state(self, fp):
        with open(fp, "rb") as f:
            self.state_dict = pickle.load(f)

    def save_state(self, fp):
        with open(fp, "wb") as f:
            pickle.dump(self.state_dict, f)
