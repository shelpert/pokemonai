from pyboy_agent import PyBoyAgent
import keyboard

agent = PyBoyAgent(emulation_speed=1)

def on_key_event(event: keyboard.KeyboardEvent):
    # Press v + number to save to that save slot
    if keyboard.is_pressed('v'):
        if event.name.isdigit():
            with open(f"state_file_{event.name}.state", "wb") as f:
                agent.save_state(f)

    # Press l + number to load that save
    if keyboard.is_pressed('l'):
        if event.name.isdigit():
            agent.load_state(f"state_file_{event.name}.state")


keyboard.hook(on_key_event)

while agent.tick(100):
    print(agent.menu_position)

agent.stop()