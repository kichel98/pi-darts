import faulthandler
from camera import CameraConfig, Camera
from pi_connector import ClientConnector
from throw_detector import DetectorConfig, ThrowDetector

faulthandler.enable()


def main():
    counter = 0
    with ClientConnector() as connector, Camera(CameraConfig()) as cam:
        connector.connect_client_to_server()
        detector = ThrowDetector(DetectorConfig())
        previous_frame = cam.take_image()
        while True:
            frame = cam.take_image()
            ret, cnt = detector.look_for_throw(previous_frame, frame)
            if ret:
                counter += 1
                x, y = detector.get_landing_point(cnt)
                print(x, y)
                connector.send_throw_info(counter, x, y)
            previous_frame = frame


if __name__ == '__main__':
    main()
