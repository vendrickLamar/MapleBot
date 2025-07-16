import time

import pydirectinput

class PlayerInputs:

    @staticmethod
    def attack():
        print("Attacking...")
        pydirectinput.keyDown('x')
        time.sleep(0.01)
        pydirectinput.keyUp('x')
        time.sleep(0.01)

    @staticmethod
    def move_right():
        print("Moving right...")
        pydirectinput.keyDown('right')
        time.sleep(1)
        pydirectinput.keyUp('right')
        time.sleep(0.1)


    @staticmethod
    def move_left():
        print("Moving left...")
        pydirectinput.keyDown('left')
        time.sleep(0.5)
        pydirectinput.keyUp('left')
        time.sleep(0.1)

    @staticmethod
    def move_up():
        print("Moving up...")
        pydirectinput.keyDown('up')
        time.sleep(0.5)
        pydirectinput.keyUp('up')
        time.sleep(0.1)

    @staticmethod
    def move_down():
        print("Moving down...")
        pydirectinput.keyDown('down')
        time.sleep(0.5)
        pydirectinput.keyUp('down')
        time.sleep(0.1)


    @staticmethod
    def jump():
        pydirectinput.keyDown('alt')
        time.sleep(0.1)
        pydirectinput.keyUp('alt')
        time.sleep(0.1)

    @staticmethod
    def jump_left():
        print("Jumping left...")
        pydirectinput.keyDown('left')
        time.sleep(0.1)
        pydirectinput.keyDown('alt')
        time.sleep(0.1)
        pydirectinput.keyUp('alt')
        time.sleep(0.2)
        pydirectinput.keyUp('left')
        time.sleep(0.1)

    @staticmethod
    def jump_right():
        print("Jumping right...")
        pydirectinput.keyDown('right')
        time.sleep(0.1)
        pydirectinput.keyDown('alt')
        time.sleep(0.1)
        pydirectinput.keyUp('alt')
        time.sleep(0.2)
        pydirectinput.keyUp('right')
        time.sleep(0.1)

    @staticmethod
    def climb_ladder(direction=None):
        print(f"Climbing ladder with direction: {direction}...")

        # Make directional adjustment if needed
        if direction == 'left':
            # Jump left to position correctly on the ladder
            pydirectinput.keyDown('left')
            time.sleep(0.1)
            pydirectinput.keyDown('alt')
            time.sleep(0.1)
            pydirectinput.keyUp('alt')
            time.sleep(0.2)
            pydirectinput.keyUp('left')
            time.sleep(0.1)

        elif direction == 'right':
            # Jump right to position correctly on the ladder
            pydirectinput.keyDown('right')
            time.sleep(0.2)
            pydirectinput.keyDown('alt')
            time.sleep(0.1)
            pydirectinput.keyUp('alt')
            time.sleep(0.2)
            pydirectinput.keyUp('right')
            time.sleep(0.1)
        else:
            # Standard jump to get onto the ladder
            pydirectinput.keyDown('alt')
            time.sleep(0.1)
            pydirectinput.keyUp('alt')
            time.sleep(0.1)

        # Press up for 5 seconds to climb the ladder
        print("Pressing up to climb...")
        pydirectinput.keyDown('up')
        time.sleep(4.0)  # Hold for 5 seconds
        pydirectinput.keyUp('up')
        time.sleep(0.1)

    @staticmethod
    def jump_down():
        print("Jumping down...")
        pydirectinput.keyDown('alt')
        time.sleep(0.1)
        pydirectinput.keyUp('down')
        time.sleep(0.1)
        pydirectinput.keyUp('alt')
        pydirectinput.keyUp('down')

class MouseInputs:
    @staticmethod
    def move_mouse(x, y):
        pydirectinput.moveTo(x, y)
