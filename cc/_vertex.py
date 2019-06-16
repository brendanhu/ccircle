from numpy import array, ndarray, float32

from cc._uv import UV
from cc._color import Color
from cc._position import Position


class Vertex:
    """ A 2D Vertex (for a shape), consisting of either:
        a) a position and a color
        b) a position and a UV

    Notes:
        Equality checks do not consider color.
    """

    def __init__(self, pos: Position, color: Color = None, uv: UV = None):
        self.pos = pos
        self.color = color
        self.uv = uv

    def is_valid(self) -> bool:
        """ Validates this vertex. """
        if self.color:
            return self.pos.is_valid() and self.color.is_valid()
        return self.uv and self.uv.is_valid() and self.pos.is_valid()

    def as_array(self) -> ndarray:
        """ Transform this vertex into a single-precision ndarray of floats: [XYZRGB] OR [XYZUV]. """
        if self.color:
            return array([self.pos.x, self.pos.y, self.pos.z, self.color.r, self.color.g, self.color.b], dtype=float32)
        return array([self.pos.x, self.pos.y, self.pos.z, self.uv.u, self.uv.v], dtype=float32)

    def __eq__(self, other) -> bool:
        """ Equality check.

        Notes:
            Does not consider color.
            For the 3D move, should check position, UVs and normals.
        """
        if self.color and other.color:
            return self.pos.__eq__(other.pos)
        return self.pos.__eq__(other.pos) and self.uv.__eq__(other.uv)

    def __str__(self) -> str:
        return "[pos, color, uv] = [%s, %s, %s]" % (self.pos, self.color, self.uv)

    def __hash__(self) -> int:
        return self.pos.__hash__()
