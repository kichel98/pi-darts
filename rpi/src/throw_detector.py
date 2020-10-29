import random
import string
from dataclasses import dataclass

import cv2

from camera import Camera


@dataclass
class DetectorConfig:
    threshold = 25
    min_contour_area = 15000
    max_contour_area = 100000


class ThrowDetector(object):
    def __init__(self, camera: Camera, config: DetectorConfig):
        self.camera = camera  # useless
        self.config = config

    def look_for_throw(self, before, after):
        """
            Takes two frames and analyzes whether dart throw occured between them.
            Returns tuple: (throw_occured, throw_contour)
            If throw occured, throw_occured is True and throw_contour is array of points in contour
            Otherwise, throw_occured is False and throw_contour is empty array
        """
        diff = cv2.absdiff(before, after)
        _, diff = cv2.threshold(diff, self.config.threshold, 255, cv2.THRESH_BINARY)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        # possible improvement: change second and third parameter of findContours
        contours = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        if not contours:
            return False, []
        # possible improvement: change key from len to contourArea
        biggest_contour = max(contours, key=len)
        if self.is_contour_dart(biggest_contour):
            area = cv2.contourArea(biggest_contour)
            print("Dart detected!")
            print(area)
            self.save_contour(after, biggest_contour, cv2.contourArea(biggest_contour))
            return True, biggest_contour
        else:
            return False, []

    def is_contour_dart(self, contour):
        """
            Measures if contour represents dart, based on heuristic and experiments.
            Returns True or False.

            possible improvements:
                you can use contourArea, minAreaRect, arcLength and others
            limits need to be determined empirically
        """
        area = cv2.contourArea(contour)
        return self.config.min_contour_area < area < self.config.max_contour_area

    @staticmethod
    def save_contour(after, contour, area):
        after_copy = after.copy()
        cv2.drawContours(after_copy, [contour], 0, (0, 255, 0), 5)
        cv2.circle(after_copy, ThrowDetector.get_landing_point(contour), 5, (0, 0, 255), 5)
        rand_string = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
        cv2.imwrite(f"../test/test-images/img-{area}-{rand_string}.jpg", after_copy)

    @staticmethod
    def get_landing_point(contour):
        """
            Returns lowest (closest to bottom of image) point of contour
            Point is list [x, y]
        """
        # don't know why, but every element of contour is not [x, y], but [[x, y]]
        # we use max, because [0, 0] is left upper corner
        return tuple(max(contour, key=lambda p: p[0][1])[0])
