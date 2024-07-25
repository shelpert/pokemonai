from src.environment.pyboyenv import PyBoyEnv
from src.rl_models import BasicRL


env = PyBoyEnv()
model = BasicRL(env)

for _ in range(10):
    model.run_training_session()
