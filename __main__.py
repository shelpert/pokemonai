from pyboy import PyBoy
import keyboard
import mem_scanner

def on_key_event(event):

    # Press v + number to save to that save slot
    if keyboard.is_pressed('v'):
        if event.name.isdigit():
            with open("state_file_" + event.name + ".state", "wb") as f:
                pyboy.save_state(f)

    # Press l + number to load that save
    if keyboard.is_pressed('l'):
        if event.name.isdigit():
            with open("state_file_" + event.name + ".state", "rb") as f:
                pyboy.load_state(f)

    # Press m to activate the memory scanner. 
    if keyboard.is_pressed('m'):
        scan.update_mem(pyboy.memory[0x0000:0xFFFF])
        pyboy._pause()
        val = input()
        scan.set_val(int(val))
        scan.scan()
        print (scan.matches)
        hex_matches = [hex(x) for x in scan.matches_index]
        print(hex_matches)
        pyboy._unpause()

keyboard.hook(on_key_event)

pyboy = PyBoy('Pokemon - Red Version (USA, Europe).gb', sound=False)
pyboy.set_emulation_speed(1)

scan = mem_scanner.mem_scanner(pyboy.memory[0x0000:0xFFFF])
scan.init_scan()

while pyboy.tick():
    pass

pyboy.stop()