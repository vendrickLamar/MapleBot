import time

import pydirectinput

class PlayerInputs:

    @staticmethod
    def use_skill():
        print("Using skill...")
        pydirectinput.keyDown('x')
        time.sleep(0.2)
        pydirectinput.keyUp('x')

    @staticmethod
    def move_right():
        print("Moving right...")
        pydirectinput.keyDown('right')
        time.sleep(0.1)
        pydirectinput.keyUp('right')


    @staticmethod
    def move_left():
        print("Moving left...")
        pydirectinput.keyDown('left')
        time.sleep(0.1)
        pydirectinput.keyUp('left')

    @staticmethod
    def move_up():
        pydirectinput.keyDown('up')

    @staticmethod
    def move_down():
        pydirectinput.keyDown('down')


    @staticmethod
    def jump():
        pydirectinput.keyDown('alt')
        time.sleep(0.1)
        pydirectinput.keyUp('alt')
        time.sleep(0.1)

class MouseInputs:
    @staticmethod
    def move_mouse(x, y):
        pydirectinput.moveTo(x, y)

