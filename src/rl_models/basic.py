from src.pyboyenv import PyBoyEnv
from collections import defaultdict


class BasicRL:
    def __init__(self, env: PyBoyEnv):
        self.env = env
        self.state_dict = defaultdict(list)

    def run_training_round(self):
        self.env.reset()
        print("hi")