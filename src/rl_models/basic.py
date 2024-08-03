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
    def __init__(self, env: PyBoyEnv, state_arr: np.ndarray, state_lock):
        self.state_arr = state_arr
        self.state_lock = state_lock
        self.path = []
        self.e = 0.3
        super().__init__(env)

    def arr_index(self, obs):
        return (
            obs["PlayerHP"],
            obs["GeodudeHP"] + obs["OnixHP"],
            int(obs["Seeded"]),
            obs["EffectiveGrowls"],
        )

    def get_info(self, obs):
        with self.state_lock.gen_rlock():
            prob = self.state_arr[self.arr_index(obs)].tolist()
        return {"win_prob": prob}

    def get_action(self, obs, info):
        usable = np.bool_(info["PP"][:3]).astype(np.int8)
        index = self.arr_index(obs)
        if np.random.random() < self.e:
            return self.env.action_space.sample(usable)
        else:
            with self.state_lock.gen_rlock():
                s = self.state_arr[index]
                print(index, s.shape)
                action = np.argmax(s[0] / s[1] * usable)
        self.path.append((index, action))
        return action

    def apply_end_reward(self, reward, t):
        with self.state_lock.gen_wlock():
            for s, a in self.path:
                self.state_arr[*s, :, a] += (
                    max(reward - 0.01 * t, 0),
                    1 - 0.01 * t,
                )
