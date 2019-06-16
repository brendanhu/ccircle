from cc._vertex import Vertex
from cc.image import Image


class Triangle:
    """ An NDC-compatible triangle comprised of 3 Vertices and an optional texture.

    XXX(Brendan): make TexturedTriangle and ColoredTriangle.
    """
    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex, image: Image = None):
        """ A triangle comprised of 3 vertices and an optional image.
            If an image is desired, the vertices need UV coordinates--how to map the image onto the triangle.
        """
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.image = image

    def is_valid(self) -> bool:
        """ Confirms the triangle is either textured or colored. """
        return (
            self.image and
            self.v1.uv and self.v1.uv.is_valid() and
            self.v2.uv and self.v2.uv.is_valid() and
            self.v3.uv and self.v3.uv.is_valid()
        ) or (
            self.v1.color and self.v1.color.is_valid() and
            self.v2.color and self.v2.color.is_valid() and
            self.v3.color and self.v3.color.is_valid()
        )
