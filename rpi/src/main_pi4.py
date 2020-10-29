from camera import CameraConfig, Camera
from pi_connector import create_server_and_wait_for_client, receive_dart_info
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
    try:
        s, conn = create_server_and_wait_for_client()
        cam = Camera(CameraConfig())
        detector = ThrowDetector(cam, DetectorConfig())
        previous_frame = cam.take_image()
        while True:
            frame = cam.take_image()
            ret, cnt = detector.look_for_throw(previous_frame, frame)
            if ret:
                print(detector.get_landing_point(cnt))
                counter, x, y = receive_dart_info(conn)
                print(f"Dart no. {counter}")
                print(f"x: {x}, y: {y}")
            previous_frame = frame
    finally:
        s.close()
        conn.close()
        cam.close()


if __name__ == '__main__':
    main()
