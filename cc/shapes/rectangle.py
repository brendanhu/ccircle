from cc.image import Image
from cc._uv import UV
from cc._color import Color
from cc._position import Position
from cc.image import Image
from cc.shapes.triangle import Triangle
from cc._vertex import Vertex


class Rectangle:
    """ A 2D rectangle comprised of 2 triangles sharing 2 vertices. """
    def __init__(self, top_left: Position, width: float, height: float, color: Color = None, image: Image = None):
        """ Create a rectangle with 1 Vertex, width, height, and optional Image.
            If a texture is given, UVs are figured out internally.

        Returns:
            Rectangle: a newly created rectangle.
        """
        if color and image:
            raise RuntimeError("Rectangle must either have a color or a texture, not both.")

        if not image:
            v1 = Vertex(top_left, color)
            v2 = Vertex(Position(top_left.y.x + width, top_left.y.y), color)
            v3 = Vertex(Position(top_left.y.x + width, top_left.y.y + height), color)
            v4 = Vertex(Position(top_left.y.x, top_left.y.y + height), color)
        else:
            v1 = Vertex(top_left, uv=UV(0.0, 1.0))
            v2 = Vertex(Position(top_left.x + width, top_left.y), uv=UV(1.0, 1.0))
            v3 = Vertex(Position(top_left.x + width, top_left.y - height), uv=UV(1.0, 0.0))
            v4 = Vertex(Position(top_left.x, top_left.y - height), uv=UV(0.0, 0.0))

        self.t1 = Triangle(v1, v2, v4, image=image)
        self.t2 = Triangle(v2, v4, v3, image=image)
