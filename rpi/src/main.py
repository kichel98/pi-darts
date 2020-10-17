import random
import string
import time

import cv2
import numpy as np
import picamera

"""
    TODO:
    - extract all constants (pack into dict?)
    - adjust all constants (thresholds etc.)
    - test get_landing_point and uncomment
    - implement is_contour_dart
    - general tests (see images at various stages: after diff, after threshold)
    - general refactor
"""


WIDTH = 2592
HEIGHT = 1936
FPS = 10


def get_landing_point(contour):
    return contour[0] # maybe contour[0][0]


def save_contour(after, contour, area):
    after_copy = after.copy()
    cv2.drawContours(after_copy, [contour], 0, (0, 255, 0), 5)
    rand_string = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
    cv2.imwrite(f"images/img-{area}-{rand_string}.jpg", after_copy)


def is_contour_dart(contour):
    # TODO: measure if contour is a dart
    # you can use contourArea, minAreaRect, arcLength and others
    # limits need to be determined empirically
    MIN_AREA = 15000
    MAX_AREA = 205000
    area = cv2.contourArea(contour)
    return MIN_AREA < area < MAX_AREA


def look_for_throw(before, after):
    THRESHOLD = 40
    diff = cv2.absdiff(before, after)
    _, diff = cv2.threshold(diff, THRESHOLD, 255, cv2.THRESH_BINARY)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return False, None
    biggest_contour = max(contours, key=len)
    if is_contour_dart(biggest_contour):
        area = cv2.contourArea(biggest_contour)
        print("Dart detected!")
        print(area)
        save_contour(after, biggest_contour, cv2.contourArea(biggest_contour))
        return True, biggest_contour
    else:
        return False, None


def take_image(cam):
    image = np.empty((HEIGHT * WIDTH * 3,), dtype=np.uint8)
    cam.capture(image, 'bgr')
    image = image.reshape((HEIGHT, WIDTH, 3))
    return image


def main():
    with picamera.PiCamera() as main_cam:
        main_cam.resolution = (WIDTH, HEIGHT)
        main_cam.framerate = FPS
        time.sleep(2)
        print("[INFO] Cam is ready!")
        previous_frame = take_image(main_cam)
        previous_frame = cv2.rotate(previous_frame, cv2.ROTATE_180)
        while True:
            frame = take_image(main_cam)
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            ret, cnt = look_for_throw(previous_frame, frame)
            if ret:
                pass
                # print(get_landing_point(cnt))
            previous_frame = frame


if __name__ == '__main__':
    main()
