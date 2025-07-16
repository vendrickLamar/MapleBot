import cv2 as cv
import numpy as np
from time import time

from vision_detection.detection import Detection
from vision_detection.screen_capture import WindowCapture
from vision_detection.vision import Vision
from controller.inputs import PlayerInputs, MouseInputs
from bot import MapleBot, BotState

DEBUG = True

# initialize the WindowCapture class
wincap = WindowCapture('MapleStory')

# load detector
monster_detector = Detection('monster_cascade/monster_cascade.xml')
player_detector = Detection('player_cascade/player_cascade.xml')
# load bot
bot = MapleBot((wincap.offset_x, wincap.offset_y), (wincap.w, wincap.h))

# load an empty Vision class for general use
vision= Vision(None)
# load Vision class for ladder detection using template matching
ladder_vision = Vision('ladder.png', method=cv.TM_CCOEFF_NORMED)
player_inputs = PlayerInputs()
mouse_inputs = MouseInputs()
loop_time = time()

is_bot_in_action: bool = False



wincap.start()
monster_detector.start()
player_detector.start()
bot.start()
while True:
    if wincap.screenshot is None:
        continue

    # do object detection
    player_detector.update(wincap.screenshot)
    monster_detector.update(wincap.screenshot)

    # Get player and monster targets
    player_targets = vision.get_click_points(player_detector.rectangles)
    monster_targets = vision.get_click_points(monster_detector.rectangles)

    # Detect ladders using template matching
    ladder_rectangles = ladder_vision.find(wincap.screenshot, threshold=0.9)
    ladder_targets = ladder_vision.get_click_points(ladder_rectangles)

    if bot.state == BotState.INITIALIZING:
        # while the bot is waiting to start, go ahead and start giving it some targets to work
        # on right away when it does startxxx
        bot.update_targets(player_targets, monster_targets, ladder_targets)
    elif bot.state == BotState.SEARCHING:
        # when searching for something to click on next, the bot needs to know what the click
        # points are for the current detection results. it also needs an updated screenshot
        bot.update_targets(player_targets, monster_targets, ladder_targets)
        bot.update_screenshot(wincap.screenshot)
    elif bot.state == BotState.ATTACKING:
        bot.update_targets(player_targets, monster_targets, ladder_targets)
        bot.update_screenshot(wincap.screenshot)
    elif bot.state == BotState.CLIMBING:
        # When climbing, still update targets but don't interrupt the climbing process
        # This allows the bot to detect monsters after climbing is complete
        bot.update_targets(player_targets, monster_targets, ladder_targets)
        bot.update_screenshot(wincap.screenshot)


    if DEBUG:
        # display the images.
        # draw the detection results onto the original image
        # detection_image_player = vision.draw_rectangles(wincap.screenshot, player_detector.rectangles, color=(0, 255, 0))
        detection_image_chronos = vision.draw_rectangles(wincap.screenshot, monster_detector.rectangles)
        # detection_image_ladder = ladder_vision.draw_rectangles(wincap.screenshot.copy(), ladder_rectangles)
        # cv.imshow('Player', detection_image_player)
        cv.imshow('Monsters', detection_image_chronos)
        # cv.imshow('Ladders', detection_image_ladder)



    # debug the loop rate
    # print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # press 'f' to save a screenshot as a positive image, press 'd' to
    # save as a negative image.
    # waits 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if key == ord('q'):
        player_detector.stop()
        wincap.stop()
        bot.stop()
        cv.destroyAllWindows()
        break
    elif key == ord('f'):
        cv.imwrite('positive/{}.jpg'.format(loop_time), wincap.screenshot)
    elif key == ord('d'):
        cv.imwrite('negative/{}.jpg'.format(loop_time), wincap.screenshot)

print('Done.')
