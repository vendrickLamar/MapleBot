import cv2 as cv
import numpy as np

class Vision:

    needle_img = None
    needle_w = None
    needle_h = None
    method = None

    def __init__(self, needle_img_path: str,
                 method=cv.TM_CCOEFF_NORMED):
       # self.needle_img = cv.imread(needle_img_path, cv.IMREAD_GRAYSCALE)
       self.needle_img = cv.imread(needle_img_path)
       self.needle_w = self.needle_img.shape[1]
       self.needle_h = self.needle_img.shape[0]
       self.method = method

    def find(self,haystack_img, threshold: float = 0.5):
        # if len(haystack_img.shape) == 3:
        #     haystack_img = cv.cvtColor(haystack_img, cv.COLOR_BGR2GRAY)
        result = cv.matchTemplate(haystack_img,self.needle_img, self.method)

        locations = np.where(result >= threshold)
        # we can zip those up into position tuples
        locations = list(zip(*locations[::-1]))

        # build a rectangle list for groupRectangles() function from opencv
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, _ = cv.groupRectangles(rectangles, 1, 0.1)
        return rectangles

    @staticmethod
    def get_click_points(rectangles):
        points = []
        for (x,y,w,h) in rectangles:
            # Determine center position
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            points.append((center_x, center_y))
        return points

    @staticmethod
    def draw_rectangles(haystack_img, rectangles):
        if len(rectangles):
            line_color = (0, 0, 255)
            line_type = cv.LINE_4

            for (x,y,w,h) in rectangles:
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # Draw the box
                cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
        return haystack_img

    @staticmethod
    def draw_corsairs(haystack_img, points):
            # Draw markers
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS
            for (center_x, center_y) in points:
                cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)
            return haystack_img






