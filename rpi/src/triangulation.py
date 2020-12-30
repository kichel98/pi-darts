import math
from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from camera import CameraConfig


@dataclass
class TriangulationConfig(object):
    """
        Class designed to produce config triangulation object.

        Arguments:
            down_cam_config         config object for down camera
            right_cam_config        config object for right camera
            down_side_length        length of down side of chassis
            right_side_length       length of right side of chassis
            board_radius            radius of dartboard
    """
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
                right_cam_point     (x, y) dart landing point in pixels from right camera

            Returns:
                (x,y) coords of dart on board
        """
        pass


class InterpolatedTriangulation(Triangulation):
    """
        Implementation of triangulation based on interpolation.
    """

    def __init__(self, config: TriangulationConfig):
        super().__init__(config)

    def triangulate(self, down_cam_point, right_cam_point):
        """
            For description, see abstract method docstring.

            Executes triangulation, taking care of changing coordinate system.
            Eventually, coordinate origin is middle of dartboard.
        """
        down_cam_x = down_cam_point[0]
        right_cam_x = right_cam_point[0]
        down_cam_angle = self._interpolate_angle(down_cam_x, self.config.down_cam_config)
        right_cam_angle = self._interpolate_angle(right_cam_x, self.config.right_cam_config)
        down_cam_angle = 45 + down_cam_angle * (-1)
        right_cam_angle = 45 + right_cam_angle
        x, y = self._solve(down_cam_angle, right_cam_angle)
        return x + self.config.board_radius, self.config.right_side_length - y

    def _interpolate_angle(self, x, cam_config):
        """
            Measures angle to dart using proportion to full field of view.
            
            Arguments:
                x               first coord of dart landing point on given camera
                cam_config      config object for given camera

            Returns angle between camera and dart, where middle of image is considered as 0 degree,
            points on the left from that point are negative, but on the right - positive.
        """
        # TODO: you should state which point of pixel represents it:
        # left border, right border or center
        absolute_angle = x * cam_config.horizontal_fov / cam_config.width
        return absolute_angle - (cam_config.horizontal_fov / 2)

    def _solve(self, alfa, beta):
        """
            Solves quadratic equation whose square is y position of dart on board,
            where down camera is coordinate origin.

            Arguments:
                alfa    angle to dart from down camera
                beta    angle to dart from right camera

            Returns point (x, y) representing position of dart on board.
        """
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
