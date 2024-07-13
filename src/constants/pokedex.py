"""
Enums of pokemon data.

To access by name, use Class.THING
To access by id (found in memory), use Class(thing_id)
"""

from enum import IntEnum


class Move(IntEnum):
    """Index of pokemon moves."""

    NONE = 0  # Empty move
    LEECH_SEED = 73
    GROWL = 45
    TACKLE = 33
    DEFENSE_CURL = 111
    BIDE = 117
    SCREECH = 103


class Pokemon(IntEnum):
    """Index of pokemon species."""

    # NOTE: This is not pokedex entry number, but the ID from this list:
    # https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_index_number_(Generation_I)
    NONE = 0  # No pokemon in this slot
    ONIX = 34
    BULBASAUR = 153
    GEODUDE = 169
    CHARMANDER = 176
    SQUIRTLE = 177
