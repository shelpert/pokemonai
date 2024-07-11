import random
from pyboy import PyBoy
from MemScanner import MemScanner
import mem_values
from Player import Player
import keyboard
import csv



def on_key_event(event: keyboard.KeyboardEvent):
    # Press v + number to save to that save slot
    if keyboard.is_pressed('v'):
        if event.name.isdigit():
            with open(f"pokemonai\\state_file_{event.name}.state", "wb") as f:
                pyboy.save_state(f)

    # Press l + number to load that save
    if keyboard.is_pressed('l'):
        if event.name.isdigit():
            with open(f"pokemonai\\state_file_{event.name}.state", "rb") as f:
                pyboy.load_state(f)

    # Press '/' to close the emulator when running in headless mode
    if keyboard.is_pressed('/'):
        pyboy.stop()


pyboy = PyBoy("pokemonai\\Pokemon - Red Version (USA, Europe).gb", window = 'null', sound=False)
pyboy.set_emulation_speed(0)

with open("pokemonai\\state_file_6.state", "rb") as f:
    pyboy.load_state(f)

keyboard.hook(on_key_event)