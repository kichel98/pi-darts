from camera import CameraConfig, Camera
from pi_connector import connect_client_to_server, send_dart_info
from throw_detector import DetectorConfig, ThrowDetector

"""
    TODO:
    - extract all constants (pack into dict?)
    - adjust all constants (thresholds etc.)
    - test get_landing_point and uncomment
    - implement is_contour_dart
    - general tests (see images at various stages: after diff, after threshold)
"""


def main():
    counter = 0
    try:
        s = connect_client_to_server()
        cam = Camera(CameraConfig())
        detector = ThrowDetector(cam, DetectorConfig())
        previous_frame = cam.take_image()
        while True:
            frame = cam.take_image()
            ret, cnt = detector.look_for_throw(previous_frame, frame)
            if ret:
                counter += 1
                x, y = detector.get_landing_point(cnt)
                print(x, y)
                send_dart_info(s, counter, x, y)
            previous_frame = frame
    finally:
        s.close()


if __name__ == '__main__':
    main()
