import faulthandler
from camera import CameraConfig, Camera
from pi_connector import ServerConnector
from throw_detector import DetectorConfig, ThrowDetector
from triangulation import InterpolatedTriangulation, TriangulationConfig
from board_mapping import BoardMapper, BoardMapperConfig

faulthandler.enable()


def main():
    with ServerConnector() as connector, Camera(CameraConfig()) as cam:
        connector.create_server_and_wait_for_client()
        detector = ThrowDetector(DetectorConfig())
        # TODO: pass original CameraConfig instead of new instances
        triangulation = InterpolatedTriangulation(TriangulationConfig(CameraConfig(), CameraConfig()))
        board_mapper = BoardMapper(BoardMapperConfig())
        previous_frame = cam.take_image()
        while True:
            frame = cam.take_image()
            ret, cnt = detector.look_for_throw(previous_frame, frame)
            if ret:
                print(detector.get_landing_point(cnt))
                counter, right_cam_x, right_cam_y = connector.receive_throw_info()
                print(f"Dart no. {counter}")
                print(f"x: {right_cam_x}, y: {right_cam_y}")
                dart_x, dart_y = triangulation.triangulate(detector.get_landing_point(cnt), (right_cam_x, right_cam_y))
                print(f"Segment: {board_mapper.map_dart_position_to_segment(dart_x, dart_y)}")
            previous_frame = frame


if __name__ == '__main__':
    main()
