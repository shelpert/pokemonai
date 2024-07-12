from typing import Callable
from pyboy import PyBoyMemoryView
from constants import pokedex


class AddrGetter[T]:
    """Descriptor for accessing PyBoy memory addresses"""

    def __init__(
        self,
        offset: int,
        converter: Callable[[int], T] | None = None,
        width: int = 1,
    ) -> None:
        self.offset = offset
        self.width = width
        self.converter = converter or (lambda x: x)

    def __get__(self, obj, _=None):
        # Offset from the object's base address if present
        addr = getattr(obj, "base_addr", 0) + self.offset
        # Potentially read multiple bytes
        if self.width == 1:
            value = obj.view[addr]
        else:
            value = int.from_bytes(obj.view[addr : addr + self.width])

        value = self.converter(value)
        return value


class PokemonMemory:
    """Memory getters for a single pokemon"""

    def __init__(self, view: PyBoyMemoryView, base_addr: int) -> None:
        self.view = view
        self.base_addr = base_addr

    # Offsets are constant across multiple pokemon.
    # Addresses are based on player pokemon 1
    species = AddrGetter(0xD16B - 0xD16B, pokedex.Pokemon)
    hp = AddrGetter(0xD16C - 0xD16B, width=2)
    max_hp = AddrGetter(0xD18D - 0xD16B, width=2)
    level = AddrGetter(0xD18C - 0xD16B)
    status = AddrGetter(0xD16F - 0xD16B)
    type1 = AddrGetter(0xD170 - 0xD16B)
    type2 = AddrGetter(0xD171 - 0xD16B)
    move1 = AddrGetter(0xD173 - 0xD16B, pokedex.Move)
    move2 = AddrGetter(0xD174 - 0xD16B, pokedex.Move)
    move3 = AddrGetter(0xD175 - 0xD16B, pokedex.Move)
    move4 = AddrGetter(0xD176 - 0xD16B, pokedex.Move)

    def __str__(self) -> str:
        return f"{self.species.name.capitalize()}[Lv{self.level}; {self.hp}/{self.max_hp}HP]"  # type: ignore


class MemoryViewWrapper:
    """PyBoyMemoryView wrapper to add Pokemon-specific memory values"""

    def __init__(self, view: PyBoyMemoryView):
        self.view = view

        self.player_pkmn = [
            PokemonMemory(self.view, addr)
            for addr in (0xD16B, 0xD197, 0xD1C3, 0xD1EF, 0xD21B, 0xD247)
        ]
        self.opponent_pkmn = [
            PokemonMemory(self.view, addr)
            for addr in (0xD8A4, 0xD8D0, 0xD8FC, 0xD928, 0xD954, 0xD980)
        ]

    # In-battle statuses (includes confused, seeded, etc.)
    player_status = AddrGetter(0xD062, width=3)
    enemy_status = AddrGetter(0xD067, width=3,)
