from multiprocessing import Process, Event
from src.aim_assistant import AutoAim  
from pynput.keyboard import Listener as KeyboardListener
from src.key_manager import key_mapping, KeyStateManager

def on_press(key):
    """
    Function to handle key press events
    """
    key_str = key_mapping.get(str(key))
    if key_str and not key_state_manager.key_state[key_str]:
        
        key_state_manager.key_state[key_str] = True
        key_state_manager.key_state['last'] = key_str
        key_state_manager.execute_operation(event)


def on_release(key):
    """
    Function to handle key release events
    """
    key_str = key_mapping.get(str(key))
    if key_str:
        key_state_manager.key_state[key_str] = False
        if key_str == 'q':
            event.clear()  
        if key_state_manager.key_state['last'] == key_str:
            key_state_manager.key_state['last'] = None
        key_state_manager.execute_operation(event)

if __name__ == '__main__':

    auto_aim_instance = AutoAim() 
    event = Event()  
    auto_aim_process = Process(target=auto_aim_instance.run, args=(event,))
    auto_aim_process.start()
    key_state_manager = KeyStateManager()
    with KeyboardListener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    auto_aim_process.join()
