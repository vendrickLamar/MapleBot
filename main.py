import time
import cv2 as cv
import numpy as np

from vision.screen_capture import WindowCapture
from vision.detection import Vision
from vision.hsv_filter import HsvFilter
from controller.inputs import PlayerInputs
wincap = WindowCapture()
loop_time = time.time()
vision_chronos = Vision('chronos_hsv_filter.png')
hsv_filter = HsvFilter(h_min=0, s_min=0,v_min=98, h_max=179, s_max=123, v_max=255, s_add=59, s_sub=107, v_add=25, v_sub=57)
# vision_chronos.init_control_gui()
while True:

    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    # pre-process the image
    processed_image = vision_chronos.apply_hsv_filter(screenshot, hsv_filter)
    # do object detection
    rectangles = vision_chronos.find(processed_image, threshold=0.6)
    points = vision_chronos.get_click_points(rectangles)
    print(f'Monsters detected: {len(points)}')
    #draw the detection results onto the original image
    # output_image = vision_chronos.draw_corsairs(processed_image, points)

    # display the processed image
    # cv.imshow('Matches', output_image)
    # cv.imshow('Processed Image', processed_image)

    # debug the loop rate
    # print('FPS {}'.format(1 / (time() - loop_time)))
    # loop_time = time()

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
