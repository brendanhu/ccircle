from cc._color import Color
from cc._vertex import Vertex


class Circle:
    """ An NDC-compatible circle comprised of a center Vec4, a color, and a radius.

    Args:
        center: the center point of the circle (with optional color).
        color: the color of the circle (interpolated w/ center's color if given).
        radius: the radius of the circle (NDC -- max visible radius = 1.0)
    """
    def __init__(self, center: Vertex, color: Color, radius: float = 0.1):
        self.center = center
        self.color = color
        self.radius = radius
