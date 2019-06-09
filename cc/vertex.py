from cc._vec4 import Vec4
from cc.color import Color


class Vertex(Vec4):
    """ A Vertex for a shape, consisting of a Vec4 and a color.

    Notes:
        Equality checks do not consider color.
    """
    def __init__(self, position: Vec4, color: Color):
        super().__init__(
            position.x,
            position.y,
            position.z,
            position.w,
        )
        self.color = color
