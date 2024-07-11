import random
from pyboy import PyBoy
from MemScanner import MemScanner
import mem_values
from Player import Player
import keyboard
import csv
import multiprocessing

csvnum = 0

def run_pyboy_instance(rom_path, csvnum, save_state=None):

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

        if keyboard.is_pressed('/'):
            pyboy.stop()


    keyboard.hook(on_key_event)

    pyboy = PyBoy('pokemonai\\Pokemon - Red Version (USA, Europe).gb', window='null')
    pyboy.set_emulation_speed(1)
    with open("pokemonai\\state_file_6.state", "rb") as f:
        pyboy.load_state(f)
    pyboy.memory[0xD355] = 0xC0


    player = Player(pyboy)
    counter = -1
    wins = 0
    losses = 0
    fightnum = 0
    crit_flag = 0
    miss_flag = 0

    rand = random.SystemRandom()

    header = [
        'BattleNum',
        'Pokemon',
        'Move',
        'Crit?',
        'Miss?',
        'PlayerHP',
        'OpponentHP'
    ]

    header2 = [
        'BattleNum'
        'Win?',
        'Turns'
    ]

    movedict = {
        73: 'leech seed',
        45: 'growl',
        33: 'tackle',
        111: 'defense curl',
        117: 'bide',
        103: 'screech'
    }

    pokedex = {
        34: 'onix',
        169: 'geodude'
    }

    turns = 0
    
    with open ('BattleOverview' + str(csvnum) + '.csv', 'w', encoding='UTF8', newline = '') as fo:
        basicwriter = csv.writer(fo)
        basicwriter.writerow(header2)

        with open ('BattleData' + str(csvnum) + '.csv', 'w', encoding='UTF8', newline = '') as f:
            writer = csv.writer (f)
            writer.writerow(header)


            while pyboy.tick():
                if pyboy.memory[0xD05E] == 1:
                    crit_flag = 1
                
                if counter == -1:
                    
                    pyboy.tick(20)
                    if pyboy.memory[0xCC26] == 0 and pyboy.memory[0xCC25] == 9:
                        turns += 1
                        pyboy.button('a')
                        pyboy.tick(10)
                        pyboy.button ('down')
                        pyboy.tick(10)
                        pyboy.button ('down')
                        pyboy.tick(10)
                        pyboy.button ('a')
                        data = [
                            str(fightnum),
                            'bulbasaur',
                            movedict[pyboy.memory[0xCCDC]],
                            str(False if (crit_flag == 0) else True),
                            str(False),
                            str(pyboy.memory[mem_values.pkmn1_hp + 1]),
                            str(pyboy.memory[0xCFE7])
                        ]
                        if crit_flag == 1:
                            crit_flag = 0
                        
                        writer.writerow(data)
                        
                
                counter += 1
                if counter % 5 == 0:
                    if pyboy.memory[0xCC26] == 0 and pyboy.memory[0xCC25] == 9:
                        if (pyboy.memory[0xCCDD] != 0):
                            data = [
                                str(fightnum),
                                pokedex[pyboy.memory[0xCFD8]],
                                movedict[pyboy.memory[0xCCDD]],
                                str(False if (crit_flag == 0) else True),
                                str(True if (pyboy.memory[0xD0D8] == 0 and (pyboy.memory[0xCCDD] == 33 or pyboy.memory[0xCCDD] == 117)) else False),
                                str(pyboy.memory[mem_values.pkmn1_hp + 1]),
                                str(pyboy.memory[0xCFE7])
                            ]
                        if crit_flag == 1:
                            crit_flag = 0
                        
                        writer.writerow(data)
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
                        turns += 1

                        if pyboy.memory[0xD05E] == 1:
                            crit_flag = 1
                        


                        data = [
                            str(fightnum),
                            'bulbasaur',
                            movedict[pyboy.memory[0xCCDC]],
                            str(False if (crit_flag == 0) else True),
                            str(True if (pyboy.memory[0xD0D8] == 0 and (pyboy.memory[0xCCDC] == 33 or pyboy.memory[0xCCDC] == 117)) else False),
                            str(pyboy.memory[mem_values.pkmn1_hp + 1]),
                            str(pyboy.memory[0xCFE7])
                        ]
                        if crit_flag == 1:
                            crit_flag = 0
                        
                        writer.writerow(data)
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
                    data = [
                        str(fightnum),
                        pokedex[pyboy.memory[0xCFD8]],
                        movedict[pyboy.memory[0xCCDD]],
                        str(False if (crit_flag == 0) else True),
                        str(True if (pyboy.memory[0xD0D8] == 0 and (pyboy.memory[0xCCDD] == 33 or pyboy.memory[0xCCDD] == 117)) else False),
                        str(pyboy.memory[mem_values.pkmn1_hp + 1]),
                        str(pyboy.memory[0xCFE7])
                    ]
                    writer.writerow(data)
                    basicwriter.writerow([str(fightnum), 'false', str(turns)])
                    print ('loss')
                    losses += 1
                    counter = -1
                    fightnum += 1
                    turns = 0
                    with open("pokemonai\\state_file_6.state", "rb") as f:
                        pyboy.load_state(f)
                if (pyboy.memory[mem_values.e_pkmn1_hp + 1] == 0) and (pyboy.memory[mem_values.e_pkmn2_hp + 1] == 0):
                    # writer.writerow(data)
                    basicwriter.writerow([str(fightnum), 'true', str(turns)])
                    print ('win')
                    wins += 1
                    counter = -1
                    fightnum += 1
                    turns = 0
                    with open("pokemonai\\state_file_6.state", "rb") as f:
                        pyboy.load_state(f)
                pass

    pyboy.stop()

if __name__ == "__main__":
    rom_path = 'pokemonai\\Pokemon - Red Version (USA, Europe).gb'  # Update with your ROM file path
    save_state = 'pokemonai\\state_file_6.state'  # Optional: Update with your save state file if needed

    num_instances = 6  # Number of PyBoy instances to run in parallel
    processes = []

    for i in range(num_instances):
        p = multiprocessing.Process(target=run_pyboy_instance, args=(rom_path, i, save_state))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()