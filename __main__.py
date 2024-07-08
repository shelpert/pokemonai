import random
from pyboy import PyBoy
from MemScanner import MemScanner
import mem_values
from Player import Player
import keyboard


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

    # Press m to activate the memory scanner.
    if keyboard.is_pressed('m'):
        scan.update_mem(pyboy.memory[0x0000:0xFFFF])
        pyboy._pause()
        val = input()
        scan.set_val(int(val))
        scan.scan()
        print(scan.matches)
        hex_matches = [hex(x) for x in scan.matches_index]
        print(hex_matches)
        pyboy._unpause()


keyboard.hook(on_key_event)

pyboy = PyBoy("pokemonai\\Pokemon - Red Version (USA, Europe).gb", sound=False)
pyboy.set_emulation_speed(1)
with open("pokemonai\\state_file_6.state", "rb") as f:
    pyboy.load_state(f)

scan = MemScanner(pyboy.memory[0x0000:0xFFFF])
scan.init_scan()

player = Player(pyboy)
counter = -1
wins = 0
losses = 0
fightnum = 0

rand = random.SystemRandom()

battleData = []

while pyboy.tick():
    print (battleData)
    if counter == -1:
        battleData.append([])
        pyboy.tick(20)
        if pyboy.memory[0xCC26] == 0 and pyboy.memory[0xCC25] == 9:
            pyboy.button('a')
            pyboy.tick(10)
            pyboy.button ('down')
            pyboy.tick(10)
            pyboy.button ('down')
            pyboy.tick(10)
            pyboy.button ('a')
            battleData[fightnum].append(pyboy.memory[0xCCDC])
            
    
    counter += 1
    if counter % 5 == 0:
        if pyboy.memory[0xCC26] == 0 and pyboy.memory[0xCC25] == 9:
            if (pyboy.memory[0xCCDD] != 0):
                battleData[fightnum].append(pyboy.memory[0xCCDD])
            pyboy.button ('a')
            pyboy.tick(10)
            if (pyboy.memory[0xD02F] == 0):
                attack = rand.randint(1, 2)
            else :
                attack = rand.randint(1, 3)
            while pyboy.memory[0xCC26] != attack:
                pyboy.button ('down')
                pyboy.tick(10)
            pyboy.button ('a')
            pyboy.tick(10)
            battleData[fightnum].append(pyboy.memory[0xCCDC])
        elif (pyboy.memory[0xCC26] >=0 and pyboy.memory[0xCC26] <= 2) and pyboy.memory[0xCC25] == 5:
            pyboy.button ('a')
            pyboy.tick(10)
        else:
            if pyboy.memory[0xCC26] == 1:
                pyboy.button ('up')
            if pyboy.memory[0xCC25] == 15:
                pyboy.button ('left')
        
    if counter == 50:
        # print(str(wins) + " " + str (losses))
        counter = 0
    
    if pyboy.memory[mem_values.pkmn1_hp + 1] == 0:
        losses += 1
        counter = -1
        fightnum += 1
        with open("pokemonai\\state_file_6.state", "rb") as f:
            pyboy.load_state(f)
    if (pyboy.memory[mem_values.e_pkmn1_hp + 1] == 0) and (pyboy.memory[mem_values.e_pkmn2_hp + 1] == 0):
        wins += 1
        counter = -1
        fightnum += 1
        with open("pokemonai\\state_file_6.state", "rb") as f:
            pyboy.load_state(f)
        
    

pyboy.stop()
