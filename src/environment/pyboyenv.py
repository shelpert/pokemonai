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
        )

        self.observation_space = spaces.Dict({
            "PlayerHP": spaces.Discrete(50),
            "GeodudeHP": spaces.Discrete(50),
            "OnixHP": spaces.Discrete(50),
            "Seeded": spaces.Discrete(2),
            "EffectiveGrowls": spaces.Discrete(7),
        })
        self.action_space = spaces.Discrete(3)

    def _get_obs(self):
        a = self._agent
        return {
            "PlayerHP": a.player_pokemon[0].hp,
            "GeodudeHP": a.enemy_pokemon[0].hp,
            "OnixHP": a.enemy_pokemon[1].hp,
            "Seeded": BattleStatus.SEEDED in a.enemy_status,
            "EffectiveGrowls": 0,
        }

    def _get_info(self):
        a = self._agent
        return {
            **self._get_obs(),
            "EnemyLastMove": pokedex.Move(a.memory[0xCCDC]),
            "PlayerLastMove": pokedex.Move(a.memory[0xCCDD]),
            "PP": a.player_pokemon[0].pp,
        }

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._agent.load_state(STATE_PATH)
        self._agent.tick(50 + (seed or 0) % 25)
        return self._get_obs(), self._get_info()

    def step(self, action):
        self._agent.battle_attack(action)
        continue_ = self._agent.wait_for_turn()

        obs = self._get_obs()
        terminated = obs["PlayerHP"] == 0 or obs["OnixHP"] == 0 or not continue_
        reward = 1 if obs["OnixHP"] == 0 else 0
        info = self._get_info()
        
        return obs, reward, terminated, False, info

    def render(self):
        pass  # TODO

    def close(self):
        self.agent.stop()
