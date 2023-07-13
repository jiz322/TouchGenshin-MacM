import pyautogui
import numpy as np
from ultralytics import YOLO
from PIL import ImageGrab, Image
from mss import mss
from src.key_manager import config


class AutoAim:
    """
    Main function to start auto-aiming
    :param event: event to control the start and stop of the auto-aiming
    NOTICE: the run function can be only called once
        this is the limitation of python multiprocessing
    """
    def run(self, event):
        self.model = YOLO('./model/yuanmo_detect_320.pt')
        self.screenshot_size = ImageGrab.grab().size 
        self.screenWidth = pyautogui.size()[0]
        self.screenHeight = pyautogui.size()[1]
        self.position = pyautogui.position()
        self.move_c = 50.0 / 1728 * pyautogui.size()[0] # constant control mouse moving speed
        self.sct = mss()
        while True:
            event.wait()
            screenshot = self.sct.grab(self.sct.monitors[0])
            screenshot = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            detections = self.model(screenshot)[0].boxes.data.cpu().numpy()
            self._auto_aim(detections)
            if not event.is_set():
                continue

    def _auto_aim(self, detections):
        """
        Control the mouse to auto-aim at the detected object
        :param detections: Detected object's location
        """
        if detections.shape[0] > 0: # make sure something is detected
            center_x = self.screenshot_size[0] * config.getfloat('ScreenCoordinates', 'crosshair_x')
            center_y = self.screenshot_size[1] * config.getfloat('ScreenCoordinates', 'crosshair_y')
            displacement = self._get_displacement(detections, center_x, center_y)
            self.position = pyautogui.position()
            t_x = self.position[0] + displacement[0]/self.move_c
            t_y = self.position[1] + displacement[1]/self.move_c
            self._drag_cursor(t_x, t_y)
            self.position = pyautogui.position()

    def _get_displacement(self, detections, center_x, center_y):
        """
        Calculate the displacement from center of screen to the center of the closest detection
        :param detections: Detected object's location
        :param center_x: x-coordinate of the screen center
        :param center_y: y-coordinate of the screen center
        :return: Displacement of the object from the screen center
        """
        x1_values = detections[:, 0]
        y1_values = detections[:, 1]
        x2_values = detections[:, 2]
        y2_values = detections[:, 3]
        center_x_values = (x1_values + x2_values) / 2
        center_y_values = (y1_values + y2_values) / 2
        distances = np.sqrt((center_x_values - center_x) ** 2 + (center_y_values - center_y) ** 2)
        closest_index = np.argmin(distances)
        displacement = (center_x_values[closest_index] - center_x, center_y_values[closest_index] - center_y)
        return displacement
    
    def _drag_cursor(self, x, y):
        """
        Drag the cursor to the given position
        :param x: x-coordinate of the position
        :param y: y-coordinate of the position
        """
        start_x, start_y = pyautogui.position()
        step_x = x - start_x
        step_y = y - start_y
        pyautogui.moveRel((abs(step_x) ** 0.9 if step_x >= 0 else -(abs(step_x)) ** 0.9 ) , 
                        (abs(step_y) ** 0.9 if step_y >= 0 else -abs(step_y) ** 0.9 ))



