import math
from dataclasses import dataclass


@dataclass
class BoardMapperConfig(object):
    """
        Class designed to produce config object needed to perform mapping dart position to board field.
        Radiuses relate to subsequent rounds on dartboard.

        Arguments:
            inner_bull_radius       radius of inner bull round
            outer_bull_radius       radius of outer bull round
            inner_normal_radius     radius of inner round with "normal" values
            treble_radius           radius of treble round
            outer_normal_radius     radius of outer round with "normal" values
            double_radius           radius of double round
            board_radius            radius of whole dartboard round
            segment_order           list with order of standard segments on board, counterclockwise,
                                        starts with right middle field

        Source for default values: https://www.bdodarts.com/images/bdo-content/doc-lib/B/bdo-playing-rules.pdf
    """
    inner_bull_radius: float = 0.635
    outer_bull_radius: float = 1.59
    inner_normal_radius: float = 10.74 - 0.8
    treble_radius: float = 10.74
    outer_normal_radius: float = 17.0 - 0.8
    double_radius: float = 17.0
    board_radius: float = 22.5
    segment_order = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]


class BoardMapper(object):
    """
        Manages dart to field mapping, based on config object.
    """
    def __init__(self, config: BoardMapperConfig):
        self.config = config

    def map_dart_position_to_segment(self, dart_x, dart_y):
        """
            Assigns dart position to dartboard segment (also called field).

            Arguments:
                dart_x      first coord of dart
                dart_y      second coord of dart

            Returns one board segment, in which a dart connected.
        """
        dart_x -= self.config.board_radius  # change to board coordinate system (centre bull is (0,0))
        dart_y -= self.config.board_radius  # change to board coordinate system (centre bull is (0,0))
        dart_y *= -1
        radius, angle = self._convert_cartesian_to_polar(dart_x, dart_y)
        angle = (angle + (1/2) * 2*math.pi / len(self.config.segment_order)) % (2*math.pi)
        base_segment_idx = math.floor(angle / (2*math.pi / len(self.config.segment_order)))
        base_segment = self.config.segment_order[base_segment_idx]

        if radius < self.config.inner_bull_radius:
            return 50
        elif radius < self.config.outer_bull_radius:
            return 25
        elif radius < self.config.inner_normal_radius:
            return base_segment
        elif radius < self.config.treble_radius:
            return base_segment * 3
        elif radius < self.config.outer_normal_radius:
            return base_segment
        elif radius < self.config.double_radius:
            return base_segment * 2
        else:
            return 0

    @staticmethod
    def _convert_cartesian_to_polar(x, y):
        """
            Converts cartesian coordinates to polar coordinates.
        """
        radius = math.sqrt(x**2 + y**2)
        if x == 0:
            if y >= 0:
                angle = math.pi / 2
            else:
                angle = 3 * math.pi / 2
            return radius, angle
        elif y == 0 and x < 0:
            return radius, math.pi
        else:
            angle = math.atan(y / x)
            if x < 0:
                angle += math.pi
            elif y < 0:
                angle += 2 * math.pi
            return radius, angle
