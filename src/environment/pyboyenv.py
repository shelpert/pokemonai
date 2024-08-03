import gymnasium as gym
import numpy as np
from src.environment.pyboy_agent import PyBoyAgent
import random
from src.environment.memory_values import BattleStatus
from src.environment import pokedex

from gymnasium import spaces


STATE_PATH = "battle_start.state"


class PyBoyEnv(gym.Env):
    metadata = {"render_modes": [], "render_fps": 4}
    reward_range = (-1, 1)

    def __init__(self, mode=None):
        self._agent = PyBoyAgent(
            state_path=STATE_PATH,
            emulation_speed=0,
            headless=True,
        )

        self.observation_space = spaces.Dict(
            {
                "PlayerHP": spaces.Discrete(50),
                "GeodudeHP": spaces.Discrete(50),
                "OnixHP": spaces.Discrete(50),
                "Seeded": spaces.Discrete(2),
                "EffectiveGrowls": spaces.Discrete(7),
            }
        )
        self.action_space = spaces.Discrete(3)
        self.rng = np.random.default_rng()

    def _get_obs(self):
        a = self._agent
        return {
            "PlayerHP": a.player_pokemon[0].hp,
            "GeodudeHP": a.enemy_pokemon[0].hp,
            "OnixHP": a.enemy_pokemon[1].hp,
            "Seeded": BattleStatus.SEEDED in a.enemy_status,
            "EffectiveGrowls": 7 - a.memory[0xCD2E],
        }

    def _get_info(self):
        a = self._agent
        return {
            **self._get_obs(),
            "EnemyLastMove": pokedex.Move(a.memory[0xCCDC]).name,
            "PlayerLastMove": pokedex.Move(a.memory[0xCCDD]).name,
            "PP": a.player_pokemon[0].pp,
        }
    
    def wait_random(self):
        self.tick(self.rng.integers(50))

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # Parallel-safe PRNG
        self.rng = np.random.Generator(np.random.PCG64DXSM(seed=seed))
        self._agent.load_state(STATE_PATH)
        self.wait_random()
        return self._get_obs(), self._get_info()

    def step(self, action):
        self.wait_random()
        self._agent.battle_attack(action)
        terminated = not self._agent.wait_for_turn()

        obs = self._get_obs()
        info = self._get_info()
        terminated |= obs["PlayerHP"] == 0 or obs["OnixHP"] == 0
        reward = 1 if obs["OnixHP"] == 0 else 0

        return obs, reward, terminated, False, info

    def render(self):
        pass  # TODO

    def close(self):
        self.agent.stop()
