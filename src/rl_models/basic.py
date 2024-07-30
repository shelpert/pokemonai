from src.environment import PyBoyEnv
import random
import numpy as np
import csv
from abc import ABC, abstractmethod
import time


class RL(ABC):
    def __init__(self, env: PyBoyEnv, data_fp: str = "data.csv"):
        self.env = env
        self.data_fp = data_fp
        # Ensure file exists
        with open(data_fp, "w+") as _:
            pass

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
            self.writer = csv.DictWriter(
                f, fieldnames=info.keys() | self.get_info(obs).keys()
            )
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
            print(f"complete {reward=} {t=} {self.data_fp}")
            self.apply_end_reward(reward, t)

    def save_state(self, fp):
        pass


class BasicRL(RL):
    def __init__(self, env: PyBoyEnv, state_dict, state_lock, data_fp):
        self.state_dict = state_dict
        self.state_lock = state_lock
        self.path = []
        self.e = 0.3
        super().__init__(env, data_fp)

    def get_info(self, obs):
        state = tuple(obs.values())
        with self.state_lock.gen_rlock():
            prob = self.state_dict.get(
                state, np.array([[0, 0, 0], [0, 0, 0]], dtype=float)
            )
        return {"win_prob": prob.tolist()}

    def get_action(self, obs, info):
        usable = np.bool_(info["PP"][:3])
        state = tuple(obs.values())
        with self.state_lock.gen_rlock():
            if state in self.state_dict and random.random() > self.e:
                s = self.state_dict[state]
                action = np.argmax(s[0] / s[1] * usable)
            else:
                action = self.env.action_space.sample(usable.astype(np.int8))
        self.path.append((state, action))
        return action

    def apply_end_reward(self, reward, t):
        with self.state_lock.gen_wlock():
            for s, a in self.path:
                d = self.state_dict.setdefault(
                    s, np.array([[0.1, 0.1, 0.1], [0.1, 0.1, 0.1]], dtype=float)
                )
                d[:, a] += max(reward - 0.01 * t, 0), 1 - 0.01 * t
