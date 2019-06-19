import math
from typing import List

from cc._color import Color
from cc._position import Position
from cc._vertex import Vertex
from cc.shapes.shape import Shape
from cc.shapes.triangle import Triangle


class Circle(Shape):
    """ An NDC-compatible circle comprised of a center Vec4, a color, and a radius.

    Args:
        center: the center point of the circle (with optional color).
        color: the color of the circle (interpolated w/ center's color if given).
        radius: the radius of the circle (NDC -- max visible radius = 1.0)

    TODO(Brendan): Support textured circles.
    """

    def __init__(self, center: Vertex, color: Color, radius: float):
        super().__init__()
        self.center = center
        self.color = color
        self.radius = radius
        self.tris = self.__calculate_triangles()

    def to_triangles(self):
        return self.tris
    
    def __calculate_triangles(self) -> List[Triangle]:
        """ Calculate the triangles needed to draw this circle on the screen.

            Notes:
                This is the old-school OpenGL way to draw a circle. Perhaps conceptually easier?
                Unsure about performance compared to GL_TRIANGLE_STRIP.
            """
        fv = self.radius / 4.0
        fv = max(fv, 64)
        num_tris = int(fv)

        tris = []
        for i in range(num_tris):
            angle1 = math.tau * (i + 0) / fv
            angle2 = math.tau * (i + 1) / fv
            tri = Triangle(
                Vertex(
                    Position(self.center.pos.x, self.center.pos.y),
                    color=self.center.color
                ),
                Vertex(
                    Position(self.center.pos.x + self.radius * math.cos(angle1),
                             self.center.pos.y + self.radius * math.sin(angle1)),
                    color=self.color
                ),
                Vertex(
                    Position(self.center.pos.x + self.radius * math.cos(angle2),
                             self.center.pos.y + self.radius * math.sin(angle2)),
                    color=self.color
                ),
            )
            tris.append(tri)
        return tris
