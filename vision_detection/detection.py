import cv2 as cv
import numpy as np
from threading import Thread, Lock

class Detection:

    # threading properties
    stopped = True
    lock = None
    rectangles = []
    # properties
    cascade = None
    screenshot = None

    def __init__(self, model_file_path):
        # create a thread lock object
        self.lock = Lock()
        # load the trained model
        self.cascade = cv.CascadeClassifier(model_file_path)

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            if not self.screenshot is None:
                # do object detection with improved parameters
                # Parameters: image, scaleFactor, minNeighbors, flags, minSize, maxSize
                rectangles = self.cascade.detectMultiScale(
                    self.screenshot,
                    scaleFactor=1.05,  # Smaller scale factor to detect more objects
                    minNeighbors=3,    # Minimum number of neighbors
                    minSize=(20, 20),  # Minimum size of detected objects
                    flags=cv.CASCADE_SCALE_IMAGE
                )
                # lock the thread while updating the results
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()
