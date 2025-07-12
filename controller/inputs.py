import time

import pydirectinput

class PlayerInputs:

    @staticmethod
    def use_skill():
        pydirectinput.keyDown('x')
        time.sleep(0.2)
        pydirectinput.keyUp('x')
        time.sleep(0.2)

    @staticmethod
    def move_right():
        print("Moving right...")
        pydirectinput.keyDown('right')
        time.sleep(0.1)

    @staticmethod
    def move_left():
        print("Moving left...")
        pydirectinput.keyDown('left')
        time.sleep(0.3)

    @staticmethod
    def move_up():
        pydirectinput.keyDown('up')
        time.sleep(0.1)

    @staticmethod
    def move_down():
        pydirectinput.keyDown('down')
        time.sleep(0.1)

    @staticmethod
    def jump():
        pydirectinput.keyDown('alt')
        time.sleep(0.1)
        pydirectinput.keyUp('alt')
        time.sleep(0.1)


if __name__ == '__main__':
    for i in range(100):
        print("Jumping")
        PlayerInputs.jump()

    print("Done")