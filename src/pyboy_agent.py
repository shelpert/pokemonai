from typing import Iterable
from src.memory_values import BattleStatus, PokemonMemory
from enum import StrEnum, auto
from pyboy import PyBoy


class Inp(StrEnum):
    A = auto()
    B = "s"
    START = auto()
    SELECT = auto()
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()


class PyBoyAgent:
    """
    Wrapper for pyboy.PyBoy for running Pokemon Red.

    Includes interfaces for accessing memory values etc.
    """

    def __init__(
        self,
        emulation_speed: float = 0,
        options_byte: int = 0xC0,
        state_path: str | None = None,
        rom_path: str = "Pokemon - Red Version (USA, Europe).gb",
    ) -> None:
        self._pyboy_instance = PyBoy(rom_path, sound=False)
        self._pyboy_instance.set_emulation_speed(emulation_speed)
        if state_path is not None:
            self.load_state(state_path)

        self._pyboy_instance.memory[0xD355] = options_byte

        # Allow direct access to memory if needed
        self.memory = self._pyboy_instance.memory

    def run(self):
        """Run PyBoy as normal."""
        while self._pyboy_instance.tick():
            pass
        self._pyboy_instance.stop()
    
    def stop(self):
        self._pyboy_instance.stop()
    
    def load_state(self, path):
        with open(path, "rb") as f:
            self._pyboy_instance.load_state(f)
        self._pyboy_instance.tick(50)
    
    def tick(self, ticks=1):
        self._pyboy_instance.tick(ticks)

    # Memory getters
    # NOTE: Accessed values will not update live with the game.

    @property
    def player_status(self):
        return BattleStatus.from_memory(self.memory[0xD062:0xD065])

    @property
    def enemy_status(self):
        return BattleStatus.from_memory(self.memory[0xD067:0xD06A])

    @property
    def player_pokemon(self):
        return PokemonMemory.party_from_memory(self.memory[0xD16B : 0xD16B + 44 * 6])

    @property
    def enemy_pokemon(self):
        return PokemonMemory.party_from_memory(self.memory[0xD8A4 : 0xD8A4 + 44 * 6])

    @property
    def menu_position(self):
        return self.memory[0xCC25], self.memory[0xCC26]

    # Input-related methods

    def press(self, key: Inp | str):
        """Press a key."""
        self._pyboy_instance.button(key)
        self._pyboy_instance.tick(2)

    def press_sequence(self, keys: Iterable[Inp | str]):
        """Press a sequence of keys."""
        for key in keys:
            self.press(key)

    def battle_attack(self, num):
        """Attack during a turn"""
        #TODO account for menu item storage
        if (self.menu_position[0] != 9 and self.menu_position[1] != 0):
            pass
        self.press(Inp.A)
        while (self.menu_position[1] != num):
            self.press(Inp.DOWN)
        self.press(Inp.A)

    def battle_switch(self, num):
        """Switch pokemon during a turn"""
        #TODO account for menu item storage
        self.press_sequence([Inp.RIGHT, Inp.A])
        self.press_sequence([Inp.DOWN] * (num - 1))
        self.press(Inp.A)

    def wait_for_turn(self):
        while (self.menu_position[0] == 5):
            pass
