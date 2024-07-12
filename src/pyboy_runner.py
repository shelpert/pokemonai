from memory_wrapper import MemoryViewWrapper
from pyboy import PyBoy


class PyBoyRunner:
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
