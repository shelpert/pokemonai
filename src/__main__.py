from src.environment.pyboyenv import PyBoyEnv
from src.rl_models import BasicRL
import multiprocessing
from multiprocessing import shared_memory
import numpy as np
from readerwriterlock import rwlock


state_shape = (50, 100, 2, 7, 2, 3)
state_nbytes = np.prod(state_shape) * np.dtype(float).itemsize
state_mem = shared_memory.SharedMemory(create=True, size=state_nbytes)
state_arr = np.ndarray(state_shape, dtype=float, buffer=state_mem.buf)
state_arr[:] = [[0.1, 0.1, 0.1], [0.2, 0.2, 0.2]]
state_lock = rwlock.RWLockWrite()


try:
    env = PyBoyEnv()
    model = BasicRL(env, state_arr, state_lock)
    c = 0
    while True:
        model.run_training_session()
        c += 1
        if c % 500 == 0:
            model.save_state(f"states/basic{c:05}.pickle")
except:
    state_mem.close()
    state_mem.unlink()
    raise
