from cc.color import Color
from cc.point import NDCPoint


class Circle:
    """ An NDC-compatible circle comprised of a center NDCPoint, a color, and a radius.

    Args:
        center: the center point of the circle (with optional color).
        color: the color of the circle (interpolated w/ center's color if given).
        radius: the radius of the circle (NDC -- max visible radius = 1.0)

    XXX(Brendan): accept colors for all verts of triangles.
    """
    def __init__(self, center: NDCPoint, color: Color, radius: float = 0.1):

        self.center = center
        self.color = color
        self.radius = radius
