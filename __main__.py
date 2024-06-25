from pyboy import PyBoy

pyboy = PyBoy('Pokemon - Red Version (USA, Europe).gb', sound=True)
pyboy.set_emulation_speed(1)
while pyboy.tick():
    pass
pyboy.stop()