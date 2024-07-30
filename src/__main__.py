from src.environment.pyboyenv import PyBoyEnv
from src.rl_models import BasicRL


env = PyBoyEnv()
model = BasicRL(env)

c = 0
while True:
    model.run_training_session()
    c += 1
    if c % 500 == 0:
        model.save_state(f"states/basic{c:05}.pickle")
