import time
from mss import mss
import configparser
import pyautogui


pyautogui.PAUSE = 0

# Macro (parameters)
class CaseSensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        """
        Overridden method from the ConfigParser class to preserve case sensitivity.
        """
        return optionstr
    
# Load configurations
config = CaseSensitiveConfigParser()
config.read('keyboard_config.ini')

# Key mappings for press events
key_mapping = dict(config['key_mapping'])

# location of buttons
config.read('position_adjustment.ini')  
screen_width, screen_height = pyautogui.size()

# Coordinates on the screen for each key
expected_keys = ["move_control", "space", "r", "e", "q", "j", "p", "c1", "c2", "c3", "h"]
screen_coordinates = {key: (screen_width * config.getfloat('ScreenCoordinates', f'{key}_x'),
                            screen_height * config.getfloat('ScreenCoordinates', f'{key}_y')) 
                      for key in expected_keys}

# Load functionalities
config.read('functionalities.ini')
aim_assistant = config.getboolean('functionalities', 'aim_assistant') 

class KeyStateManager:
    def __init__(self):
        # all keys are intialized to False (not being pressed)
        self.key_state = {key: False for key in key_mapping.values()}  
        self.key_state['last'] = None 
        self.move_x = 0
        self.move_y = 0
        # Dictionary to save screenshots
        # Key: timestamp
        # Value: image
        self.screenshots = {}
        self.sct = mss()  

    def __move_with_acceleration(self, x, y, duration, steps):
        """
        Moves the mouse cursor to the target position with acceleration.
        """
        start_x, start_y = pyautogui.position()
        step_x = (x - start_x) / steps
        step_y = (y - start_y) / steps
        step_duration = duration / steps
        for i in range(steps):
            time.sleep(step_duration)
            pyautogui.moveRel(step_x * (i)**2.1, step_y * (i)**2)

    def execute_operation(self, event):
        """
        Executes operations based on the current state of keys.
        """
        # If key k is pressed
        if self.key_state['k']:
            self.__execute_k_operation(event)

        # If the last key pressed was h
        elif self.key_state['last'] == 'h':
            self.__execute_h_operation()

        # If the last key pressed was u or i
        elif self.key_state['last'] in ['u', 'i']:
            self.__execute_ui_operation()

        # If the last key pressed was space, q, e, r, j, p, c1, c2 or c3
        elif self.key_state['last'] in ['space', 'q', 'e', 'r', 'j', 'p', 'c1', 'c2', 'c3']:
            self.__execute_last_key_operation(event)

        # If any of the movement keys are pressed
        elif any([self.key_state[key] for key in ['w', 'a', 's', 'd']]):
            self.__execute_movement_operation()

        # If no keys are pressed
        else:
            pyautogui.mouseUp()

    def __execute_k_operation(self, event):
        """
        Execute operations when 'k' key is pressed.
        """
        if aim_assistant:
            event.set() 
        pyautogui.mouseUp()
        pyautogui.moveTo(screen_coordinates['q'])  
        time.sleep(0.10)
        pyautogui.mouseDown()  
        pyautogui.mouseUp()
        time.sleep(0.3)
        pyautogui.mouseDown()  
        pyautogui.mouseUp()   
        time.sleep(0.01)
        pyautogui.mouseDown()    
        time.sleep(0.25)
        pyautogui.mouseUp() 
        if aim_assistant:
            event.clear()


    def __execute_h_operation(self):
        """
        Execute operations when 'h' key is pressed.
        """
        pyautogui.moveTo(screen_coordinates['h']) # aim
        pyautogui.mouseDown()  
        pyautogui.mouseUp()

    def __execute_ui_operation(self):
        """
        Execute operations when 'u' or 'i' key is pressed.
        """
        pyautogui.mouseUp()
        c_x, c_y = screen_coordinates['space']
        pyautogui.moveTo(c_x, c_y) 
        self.move_x = (self.key_state['i'] - self.key_state['u']) * 10
        self.move_y = 0
        pyautogui.mouseDown()  # press the mouse
        self.__move_with_acceleration(c_x+self.move_x, c_y+self.move_y, 0.00001, 5)
        pyautogui.mouseUp()

    def __execute_last_key_operation(self, event):
        """
        Execute operations when the last key pressed is space, q, e, r, j, p, c1, c2 or c3.
        """
        pyautogui.mouseUp()
        pyautogui.moveTo(*screen_coordinates[self.key_state['last']])  
        pyautogui.mouseDown()  # press the mouse
        if self.key_state['last'] == 'q' and aim_assistant:
            event.set()  # Signal process autoaim to start working

    def __execute_movement_operation(self):
        """
        Execute operations when any of the movement keys are pressed.
        """
        self.move_x = (self.key_state['d'] - self.key_state['a']) * 100
        self.move_y = (self.key_state['s'] - self.key_state['w']) * 100
        pyautogui.mouseUp()
        pyautogui.moveTo(*screen_coordinates['move_control'])  # move the mouse to the move_control of the screen
        pyautogui.mouseDown()  # press the mouse
        pyautogui.move(self.move_x, self.move_y)  # move the mouse up (y axis decreases as you go up)
