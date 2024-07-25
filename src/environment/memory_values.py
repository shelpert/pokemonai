from enum import IntFlag
from typing import NamedTuple
from src.environment import pokedex as P
from dataclasses import dataclass
from itertools import batched
import struct


class StatItems[T](NamedTuple):
    hp: T
    atk: T
    def_: T
    spd: T
    spc: T


def parse_ivs(iv: int) -> StatItems[int]:
    non_hp = [
        (iv >> 12) & 15,
        (iv >> 8) & 15,
        (iv >> 4) & 15,
        iv & 15,
    ]
    hp = (
        (non_hp[0] & 1) << 3
        | (non_hp[1] & 1) << 2
        | (non_hp[2] & 1) << 1
        | non_hp[3] & 1
    )
    return StatItems(hp, *non_hp)


@dataclass
class PokemonMemory:
    """Represents a pokemon as it is found in memory"""

    species: P.Pokemon
    level: int
    hp: int
    moves: tuple[P.Move, P.Move, P.Move, P.Move]
    types: tuple[int, int]
    stats: StatItems[int]
    ev: StatItems[int]
    iv: StatItems[int]

    @classmethod
    def from_memory(cls, data: list[int]):
        x = struct.unpack(">BHxB2Bx4B5x5HH4BB5H", bytes(data))
        return cls(
            species=P.Pokemon(x[0]),
            hp=x[1],
            # status=x[3],
            types=x[3:5],
            moves=tuple(P.Move(m) for m in x[5:9]),  # type: ignore
            ev=StatItems(*x[9:14]),
            iv=parse_ivs(x[14]),
            level=x[19],
            stats=StatItems(*x[20:25]),
        )

    @classmethod
    def party_from_memory(cls, data: list[int]):
        return [cls.from_memory(list(i)) for i in batched(data, 44)]

    def __repr__(self) -> str:
        return f"{self.species.name.capitalize()}[Lv{self.level}; {self.hp}/{self.stats.hp}HP]"  # type: ignore


class BattleStatus(IntFlag):
    # D062 / D067
    BIDE = 1 << 0
    THRASH = 1 << 1
    MULTI_ATTACK = 1 << 2
    FLINCH = 1 << 3
    ATK_CHARGE = 1 << 4
    MULTI_TURN = 1 << 5
    INVULNERABLE = 1 << 6
    CONFUSED = 1 << 7

    # D063 / D068
    X_ACCURACY = 1 << 8
    MIST = 1 << 9
    FOCUS_ENERGY = 1 << 10
    # bit 3 empty
    HAS_SUB = 1 << 12
    RECHARGE = 1 << 13
    RAGE = 1 << 14
    SEEDED = 1 << 15

    # D064 / D069
    TOXIC = 1 << 16
    LIGHT_SCREEN = 1 << 17
    REFLECT = 1 << 18
    TRANSFORMED = 1 << 19

    @classmethod
    def from_memory(cls, bytes_: list[int]):
        val = int.from_bytes(bytes_, "little")
        return cls(val)
