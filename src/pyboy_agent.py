from typing import Iterable
from memory_wrapper import MemoryViewWrapper
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
            with open(state_path, "rb") as f:
                self._pyboy_instance.load_state(f)

        self._pyboy_instance.memory[0xD355] = options_byte
        self.memory = MemoryViewWrapper(self._pyboy_instance.memory)

    def run(self):
        """Run PyBoy as normal."""
        while self._pyboy_instance.tick():
            pass
        self._pyboy_instance.stop()

    # Input-related methods

    def press(self, key: Inp | str):
        """Press a key."""
        self._pyboy_instance.button(key)
        self._pyboy_instance.tick()
        self._pyboy_instance.tick()

    def press_sequence(self, keys: Iterable[Inp | str]):
        """Press a sequence of keys."""
        for key in keys:
            self.press(key)

    def battle_attack(self, num):
        """Attack during a turn"""
        self.press(Inp.A)
        self.press_sequence([Inp.DOWN] * (num - 1))
        self.press(Inp.A)

    def battle_switch(self, num):
        """Switch pokemon during a turn"""
        self.press_sequence([Inp.RIGHT, Inp.A])
        self.press_sequence([Inp.DOWN] * (num - 1))
        self.press(Inp.A)
