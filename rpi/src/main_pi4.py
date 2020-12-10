import faulthandler
from camera import CameraConfig, Camera
from pi_connector import ServerConnector
from app_connector import AppConnector
from throw_detector import DetectorConfig, ThrowDetector
from triangulation import InterpolatedTriangulation, TriangulationConfig
from board_mapping import BoardMapper, BoardMapperConfig

faulthandler.enable()


def main():
    with ServerConnector() as connector, AppConnector() as app_connector, Camera(CameraConfig()) as cam:
        connector.create_server_and_wait_for_client()
        app_connector.start_server()
        detector = ThrowDetector(DetectorConfig())
        # TODO: pass original CameraConfig instead of new instances
        triangulation = InterpolatedTriangulation(TriangulationConfig(CameraConfig(), CameraConfig()))
        board_mapper = BoardMapper(BoardMapperConfig())
        previous_frame = cam.take_image()
        counter = 0
        while True:
            frame = cam.take_image()
            ret, cnt = detector.look_for_throw(previous_frame, frame)
            if ret:
                counter += 1
                down_cam_x, down_cam_y = detector.get_landing_point(cnt)
                print(f"Dart no. {counter} was detected")
                print(f"Pixel coords: ({down_cam_x}, {down_cam_y})")
                ext_counter, right_cam_x, right_cam_y = connector.receive_throw_info()
                print(f"Dart no. {ext_counter} was detected by Pi Zero")
                dart_x, dart_y = triangulation.triangulate(detector.get_landing_point(cnt), (right_cam_x, right_cam_y))
                segment = board_mapper.map_dart_position_to_segment(dart_x, dart_y)
                print(f"Segment: {segment}")
                app_connector.send_points(dart_x, dart_y, segment)
                print("-----------------------------")
            previous_frame = frame


if __name__ == '__main__':
    main()
