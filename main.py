from time import time
import cv2 as cv
import numpy as np

from vision.screen_capture import WindowCapture
from vision.detection import Vision

wincap = WindowCapture()
loop_time = time()
vision_chronos = Vision('chronos.png')
while True:

    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    # do object detection
    rectangles = vision_chronos.find(screenshot, threshold=0.5)

    #draw the detection results onto the original image
    output_image = vision_chronos.draw_rectangles(screenshot, rectangles)

    # display the processed image
    cv.imshow('Matches', output_image)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')

# wincap = WindowCapture()
#
# loop_time = time()
#
# while True:
#
#     # get an updated image of the game
#     screenshot = wincap.get_screenshot()
#
#     cv.imshow('Computer Vision', screenshot)
#     # find_monster_positions('chronos.png', screenshot, threshold=0.45, debug='points')
#     #debug the loop rate
#     print(f'FPS {1/(time()-loop_time)}')
