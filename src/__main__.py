from time import sleep
from datetime import datetime
from src.environment.pyboyenv import PyBoyEnv
from src.rl_models import BasicRL
from readerwriterlock import rwlock
import threading
import pickle


state_dict = {}
state_lock = rwlock.RWLockWrite()


def run_model(id_):
    env = PyBoyEnv()
    model = BasicRL(env, state_dict, state_lock, f"data/basic{id_:02}.csv")
    while True:
        model.run_training_session()


THREAD_COUNT = 4
threads = [threading.Thread(target=run_model, args=(i,)) for i in range(THREAD_COUNT)]
for t in threads:
    t.start()


# Save state_dict every 5min
while True:
    time = datetime.now().isoformat()
    with state_lock.gen_rlock(), open(f"state/basic-{time}.pickle", "wb") as f:
        pickle.dump(state_dict, f)
    sleep(300)
