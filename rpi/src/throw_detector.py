import random
import string
from dataclasses import dataclass

import cv2


@dataclass
class DetectorConfig:
    """
        Produces config object for ThrowDetector.

        Arguments:
            threshold           value that indicates which pixels should be treated as change
            min_contour_area    minimum value of contour area which qualifies contour to be a throw
            max_contour_area    maximum value of contour area which qualifies contour to be a throw
    """
    threshold = 25
    min_contour_area = 15000
    max_contour_area = 100000


class ThrowDetector(object):
    """
        Resposible for detecting single throw.
        Parametrized by DetectorConfig object.
    """
    def __init__(self, config: DetectorConfig):
        self.config = config

    def look_for_throw(self, before, after):
        """
            Takes two frames and analyzes whether dart throw occured between them, using background substraction.

            Arguments:
                before  frame/image, which had captured earlier than "after" image, is treated as base image
                after   frame/image, which was captured after "before" image, treated as image with possible change

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
            # self.save_contour(after, biggest_contour, cv2.contourArea(biggest_contour))
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

            Arguments:
                contour     one of contour from cv2.findContours()
        """
        area = cv2.contourArea(contour)
        return self.config.min_contour_area < area < self.config.max_contour_area

    @staticmethod
    def save_contour(after, contour, area):
        """
            Draws contour on image and saves is to file.

            Arguments:
                after       image with change in OpenCV format
                contour     detected contour, one of contour from cv2.findContours()
                area        contour area, return value from cv2.contourArea(), used as part of image filename
        """
        after_copy = after.copy()
        cv2.drawContours(after_copy, [contour], 0, (0, 255, 0), 5)
        cv2.circle(after_copy, ThrowDetector.get_landing_point(contour), 5, (0, 0, 255), 5)
        rand_string = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
        cv2.imwrite(f"../test/test-images/img-{area}-{rand_string}.jpg", after_copy)

    @staticmethod
    def get_landing_point(contour):
        """
            Returns lowest (closest to bottom of image) point of contour.
            Point is represented as list [x, y].

            Arguments:
                contour     detected contour, one of contour from cv2.findContours()
        """
        # don't know why, but every element of contour is not [x, y], but [[x, y]]
        # we use max, because [0, 0] is left upper corner
        return tuple(max(contour, key=lambda p: p[0][1])[0])
