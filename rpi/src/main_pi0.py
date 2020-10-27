import random
import socket
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
"""


WIDTH = 2592
HEIGHT = 1936
FPS = 1


# Returns lowest (closest to bottom of image) point of contour
# Point is list [x, y]
def get_landing_point(contour):
    # don't know why, but every element of contour is not [x, y], but [[x, y]]
    # we use max, because [0, 0] is left upper corner
    return tuple(max(contour, key=lambda p: p[0][1])[0])


def save_contour(after, contour, area):
    after_copy = after.copy()
    cv2.drawContours(after_copy, [contour], 0, (0, 255, 0), 5)
    cv2.circle(after_copy, get_landing_point(contour), 5, (0, 0, 255), 5)
    rand_string = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
    cv2.imwrite(f"../test/test-images/img-{area}-{rand_string}.jpg", after_copy)


# Measures if contour represents dart, based on heuristic and experiments.
# Returns True or False.
def is_contour_dart(contour):
    # possible improvements:
    # you can use contourArea, minAreaRect, arcLength and others
    # limits need to be determined empirically
    MIN_AREA = 15000
    MAX_AREA = 100000
    area = cv2.contourArea(contour)
    return MIN_AREA < area < MAX_AREA


# Takes two frames and analyzes whether dart throw occured between them.
# Returns tuple: (throw_occured, throw_contour)
# If throw occured, throw_occured is True and throw_contour is array of points in contour
# Otherwise, throw_occured is False and throw_contour is empty array
def look_for_throw(before, after):
    THRESHOLD = 20
    diff = cv2.absdiff(before, after)
    _, diff = cv2.threshold(diff, THRESHOLD, 255, cv2.THRESH_BINARY)
    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    # possible improvement: change second and third parameter of findContours
    contours = cv2.findContours(diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    if not contours:
        return False, []
    # possible improvement: change key from len to contourArea
    biggest_contour = max(contours, key=len)
    if is_contour_dart(biggest_contour):
        area = cv2.contourArea(biggest_contour)
        print("Dart detected!")
        print(area)
        save_contour(after, biggest_contour, cv2.contourArea(biggest_contour))
        return True, biggest_contour
    else:
        return False, []


# Captures image and convert to OpenCV format
def take_image(cam):
    image = np.empty((HEIGHT * WIDTH * 3,), dtype=np.uint8)
    cam.capture(image, 'bgr')
    image = image.reshape((HEIGHT, WIDTH, 3))
    return cv2.rotate(image, cv2.ROTATE_180)


# Sets up all camera parameter and waits for warm up
# TODO: may capture some initial frames to adjust camera settings
def setup_camera(cam):
    INITIAL_DELAY = 2
    TEST_FRAMES = 10
    cam.resolution = (WIDTH, HEIGHT)
    cam.framerate = FPS
    time.sleep(INITIAL_DELAY)
    cam.awb_mode = 'tungsten'
    for _ in range(TEST_FRAMES):
        take_image(cam)  # unnecessary rotate
    # cam.shutter_speed = cam.exposure_speed
    # cam.exposure_mode = 'off'
    # g = cam.awb_gains
    # cam.awb_gains = g
    # cam.iso = 800

    print("[INFO] Cam is ready!")


def main():
    counter = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("192.168.1.51", 1234))
        with picamera.PiCamera() as main_cam:
            setup_camera(main_cam)
            previous_frame = take_image(main_cam)
            while True:
                frame = take_image(main_cam)
                ret, cnt = look_for_throw(previous_frame, frame)
                if ret:
                    counter += 1
                    x, y = get_landing_point(cnt)
                    print(x, y)
                    counter_b = int(counter).to_bytes(4, byteorder="big")
                    x_b = int(x).to_bytes(4, byteorder="big")
                    y_b = int(y).to_bytes(4, byteorder="big")
                    data = bytes(counter_b + x_b + y_b)
                    s.send(data)
                previous_frame = frame


if __name__ == '__main__':
    main()
