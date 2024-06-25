from pyboy import PyBoy
import keyboard

def on_key_event(event):
    if keyboard.is_pressed('v'):
        if event.name.isdigit():
            with open("state_file_" + event.name + ".state", "wb") as f:
                pyboy.save_state(f)
    if keyboard.is_pressed('l'):
        if event.name.isdigit():
            with open("state_file_" + event.name + ".state", "rb") as f:
                pyboy.load_state(f)

keyboard.hook(on_key_event)

pyboy = PyBoy('Pokemon - Red Version (USA, Europe).gb', sound=True)
pyboy.set_emulation_speed(1)

while pyboy.tick():
    pass

pyboy.stop()