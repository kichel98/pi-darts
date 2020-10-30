from camera import CameraConfig, Camera
from pi_connector import connect_client_to_server, send_throw_info
from throw_detector import DetectorConfig, ThrowDetector


def main():
    counter = 0
    try:
        s = connect_client_to_server()
        cam = Camera(CameraConfig())
        detector = ThrowDetector(DetectorConfig())
        previous_frame = cam.take_image()
        while True:
            frame = cam.take_image()
            ret, cnt = detector.look_for_throw(previous_frame, frame)
            if ret:
                counter += 1
                x, y = detector.get_landing_point(cnt)
                print(x, y)
                send_throw_info(s, counter, x, y)
            previous_frame = frame
    finally:
        s.close()


if __name__ == '__main__':
    main()
