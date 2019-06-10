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

    def validate(self):
        """ Validates this vertex, throwing an error if it is invalid. """
        if not self.pos.is_valid():
            raise RuntimeError("Invalid position: %s." % self.pos.as_list())
        if not self.color.is_valid():
            raise RuntimeError("Invalid color: %s." % self.color.as_list())
