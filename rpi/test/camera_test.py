import picamera
import numpy as np
import time
import cv2

with picamera.PiCamera() as camera:
    camera.resolution = (2592, 1936)
    camera.framerate = 2
    time.sleep(2)

    image = np.empty((1936 * 2592 * 3,), dtype=np.uint8)
    camera.capture(image, 'bgr')
    image = image.reshape((1936, 2592, 3))
    cv2.imwrite("test.jpg", image)

