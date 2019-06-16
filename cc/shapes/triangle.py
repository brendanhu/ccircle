from cc._texture import Texture
from cc.vertex import Vertex


class Triangle:
    """ An NDC-compatible triangle comprised of 3 Vertices and an optional texture.

    XXX(Brendan): make TexturedTriangle and ColoredTriangle.
    """
    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex, texture: Texture = None):
        if texture and (v1.color or v2.color or v3.color):
            raise RuntimeError("A textured triangle must have vertices with UVs.")
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.texture = texture

    def is_valid(self):
        """ Checks if this triangle is valid. (i.e. if it would be seen on the screen).

        Notes: This is more an optimization.
        """
        return \
            self.v1.is_valid() and \
            self.v2.is_valid() and \
            self.v3.is_valid()
