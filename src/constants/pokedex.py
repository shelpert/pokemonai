"""
Enums of pokemon data.

To access by name, use Class.THING
To access by id (found in memory), use Class(thing_id)
"""

from enum import Enum


class Move(Enum):
    """Index of pokemon moves."""

    NONE = 0  # Empty move
    LEECH_SEED = 73
    GROWL = 45
    TACKLE = 33
    DEFENSE_CURL = 111
    BIDE = 117
    SCREECH = 103


class Pokemon(Enum):
    """Index of pokemon species."""

    NONE = 0  # No pokemon in this slot
    BULBASAUR = 153
    ONIX = 34
    GEODUDE = 169
