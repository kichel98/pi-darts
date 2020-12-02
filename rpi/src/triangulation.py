import math
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from camera import CameraConfig


@dataclass
class TriangulationConfig(object):
    # TODO: Consult camera thickness.
    down_cam_config: CameraConfig
    right_cam_config: CameraConfig
    down_side_length: float = 74.5 - 0.9
    right_side_length: float = 74.5 - 0.9
    board_radius: float = 22.505


class Triangulation(ABC):
    """
        Provides a template for all ways of getting dart position based on pixels coords.
    """

    @abstractmethod
    def __init__(self, config: TriangulationConfig):
        """
            Abstract constructor, which assigns TriangulationConfig object as `config` property
        """
        self.config = config

    @abstractmethod
    def triangulate(self, down_cam_point, right_cam_point):
        """
            Calculates dart position.

            Arguments:
                down_cam_point      (x, y) dart landing point in pixels from down camera
                right_cam_point      (x, y) dart landing point in pixels from right camera

            Returns:
                TODO: (x,y) coords of dart on board or number of field on board
        """
        pass


class InterpolatedTriangulation(Triangulation):

    def __init__(self, config: TriangulationConfig):
        super().__init__(config)

    def triangulate(self, down_cam_point, right_cam_point):
        down_cam_x = down_cam_point[0]
        right_cam_x = right_cam_point[0]
        down_cam_angle = self._interpolate_angle(down_cam_x, self.config.down_cam_config)
        right_cam_angle = self._interpolate_angle(right_cam_x, self.config.right_cam_config)
        down_cam_angle = 45 + down_cam_angle * (-1)
        right_cam_angle = 45 + right_cam_angle
        x, y = self.solve(down_cam_angle, right_cam_angle)
        return x + self.config.board_radius, self.config.right_side_length - y

    def _interpolate_angle(self, cam_y, cam_config):
        # TODO: you should state which point of pixel represents it:
        # left border, right border or center
        absolute_angle = cam_y * cam_config.horizontal_fov / cam_config.width
        return absolute_angle - (cam_config.horizontal_fov / 2)

    def solve(self, alfa, beta):
        gamma = 180 - (alfa + beta)
        w = self.config.down_side_length - self.config.board_radius
        h = self.config.right_side_length - self.config.board_radius
        cams_dist = math.sqrt(w ** 2 + h ** 2)
        b = cams_dist * math.sin(math.radians(beta)) / math.sin(math.radians(gamma))

        a2 = 1 + h ** 2 / w ** 2
        a1 = -2 * b * cams_dist * h * math.cos(math.radians(alfa)) / w ** 2
        a0 = b ** 2 * (cams_dist ** 2 * math.cos(math.radians(alfa)) ** 2 / w ** 2 - 1)

        y_all = np.roots([a2, a1, a0])
        calc_x = (lambda y: (b * cams_dist * math.cos(math.radians(alfa)) - y * h) / w)
        points = list(filter(
            lambda p: not isinstance(p[0], complex) and not isinstance(p[1], complex) and p[1] > 0,
            zip(map(calc_x, y_all), y_all)))
        return points[0]
