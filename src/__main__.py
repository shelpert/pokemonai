from src.environment.pyboyenv import PyBoyEnv
from src.rl_models import BasicRL


env = PyBoyEnv()
model = BasicRL(env)

model.run_training_round()
