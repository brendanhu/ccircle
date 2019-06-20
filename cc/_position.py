from cc._util import hash_combine
from cc._vec4 import Vec4


class Position(Vec4):
    """ A 2D position. """

    def __init__(self, x: float, y: float):
        super().__init__(x, y, 1.0, 1.0)

    def is_valid(self) -> bool:
        """ Checks if this represents a valid position in NDC space. """
        return \
            -1.0 <= self.x <= 1.0 and \
            -1.0 <= self.y <= 1.0 and \
            -1.0 <= self.z <= 1.0 and \
            self.w == 1.0

    def __hash__(self) -> int:
        """ Hash of the position (x,y). """
        combine = hash_combine(0, hash(self.x))
        combine = hash_combine(combine, hash(self.y))
        return combine
