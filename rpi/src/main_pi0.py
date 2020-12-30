import faulthandler
from camera import CameraConfig, Camera
from pi_connector import ClientConnector
from throw_detector import DetectorConfig, ThrowDetector

# added to show more debug info about e.g. segfaults
faulthandler.enable()


def main():
    """
        Main entry point for Pi 0.
        Sets connection with Pi 4 and starts dart detection.
    """
    with ClientConnector() as connector, Camera(CameraConfig()) as cam:
        connector.connect_client_to_server()
        detector = ThrowDetector(DetectorConfig())
        previous_frame = cam.take_image()
        counter = 0
        while True:
            frame = cam.take_image()
            ret, cnt = detector.look_for_throw(previous_frame, frame)
            if ret:
                counter += 1
                x, y = detector.get_landing_point(cnt)
                print(f"Dart no. {counter} was detected!")
                print(f"Pixel coords: ({x}, {y})")
                connector.send_throw_info(counter, x, y)
                print("-----------------------------")
            previous_frame = frame


if __name__ == '__main__':
    main()
