import cv2 as cv
import numpy as np
from time import time
from vision.screen_capture import WindowCapture
from vision.detection import Vision
from controller.inputs import PlayerInputs, MouseInputs
from threading import Thread

# initialize the WindowCapture class
wincap = WindowCapture('MapleStory')

cascade_chronos = cv.CascadeClassifier('cascade/cascade.xml')

# load an empty Vision class
vision_chronos = Vision(None)
player_inputs = PlayerInputs()
mouse_inputs = MouseInputs()
loop_time = time()

is_bot_in_action: bool = False

def bot_actions(target_rectangles: np.ndarray):
    # take bot actions
    global is_bot_in_action
    if len(target_rectangles) > 0:
        print('Executing Bot actions')
        player_inputs.use_skill()
    is_bot_in_action = False
while True:

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    # do object detection
    rectangles = cascade_chronos.detectMultiScale(screenshot)

    # draw the detection results onto the original image
    detection_image = vision_chronos.draw_rectangles(screenshot, rectangles)

    # display the images.
    cv.imshow('Matches', detection_image)
    # run the function in a thread that's separate from the main thread
    if not is_bot_in_action:
        is_bot_in_action = True
        t = Thread(target=bot_actions, args=(rectangles,))
        t.start()


    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # press 'f' to save a screenshot as a positive image, press 'd' to
    # save as a negative image.
    # waits 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    elif key == ord('f'):
        cv.imwrite('positive/{}.jpg'.format(loop_time), screenshot)
    elif key == ord('d'):
        cv.imwrite('negative/{}.jpg'.format(loop_time), screenshot)

print('Done.')