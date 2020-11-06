import time
from dataclasses import dataclass

import cv2
import numpy as np
from picamera import PiCamera


@dataclass
class CameraConfig:
    """
        Class designed to produce config camera object.
        Contains all parameters required to correct camera handling.

        Arguments:
            width           width of image in pixels (need to be divisible by 16)
            height          height of image in pixels (need to be divisible by 16)
            fps             number of frames per second
            initial_delay   time in seconds needed for camera warm up
            test_frames     test frames that are taken to adjust internal camera parameters
            awb_mode        white balance mode, possible options are same as for PiCamera.awb_mode
                            https://picamera.readthedocs.io/en/release-1.13/api_camera.html#picamera.PiCamera.awb_mode
    """
    width: int = 2592
    height: int = 1936
    fps = 5
    initial_delay: int = 2
    test_frames: int = 10
    awb_mode: str = 'tungsten'

    horizontal_fov = 53.5


class Camera(object):
    """
        Wrapper to picamera class, allows passing config object to constructor
        and then convenient usage.

        Arguments:
            camera      PiCamera object
            config      CameraConfig object, all parameters are got from that
    """

    def __init__(self, config: CameraConfig):
        self.camera = PiCamera()
        self.config = config
        self.setup_camera()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Closes/releases the camera. """
        print("[INFO] Closing the camera")
        self.camera.close()

    def take_image(self, should_rotate=True):
        """
            Captures image and convert to OpenCV format.
            Perform rotating if needed.

            Arguments:
                should_rotate   indicates if image need to be rotated 180 degrees
        """
        image = np.empty((self.config.height * self.config.width * 3,), dtype=np.uint8)
        self.camera.capture(image, 'bgr')
        image = image.reshape((self.config.height, self.config.width, 3))
        asdf = 2
        return cv2.rotate(image, cv2.ROTATE_180) if should_rotate else image

    def setup_camera(self):
        """ Sets up all camera parameter and waits for warm up. """
        self.camera.resolution = (self.config.width, self.config.height)
        self.camera.framerate = self.config.fps
        time.sleep(self.config.initial_delay)
        self.camera.awb_mode = self.config.awb_mode
        for _ in range(self.config.test_frames):
            self.take_image(should_rotate=False)
        print("[INFO] Camera is ready!")
