from numpy import array, ndarray, float32

from cc.color import Color
from cc.position import Position


class Vertex:
    """ A 2D Vertex (for a shape), consisting of a position and a color.

    Notes:
        Equality checks do not consider color.
    """
    def __init__(self, pos: Position, color: Color):
        self.pos = pos
        self.color = color

    def is_valid(self):
        """ Validates this vertex. """
        return self.pos.is_valid() and self.color.is_valid()

    def as_array(self) -> ndarray:
        """ Transform this vertex into a single-precision ndarray of floats: [XYZRGB]. """
        return array([self.pos.x, self.pos.y, self.pos.z, self.color.r, self.color.g, self.color.b], dtype=float32)

    def __eq__(self, other) -> bool:
        """ Equality check.

        Notes:
            Does not consider color.
            For the 3D move, should check position, UVs and normals.
        """
        return self.pos.__eq__(other.pos)

    def __hash__(self) -> int:
        return self.pos.__hash__()
