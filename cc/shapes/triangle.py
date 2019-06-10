from numpy import array, float32

from cc.vertex import Vertex


class Triangle:
    """ An NDC-compatible triangle comprised of 3 Vertices. """
    def __init__(self, v1: Vertex, v2: Vertex, v3: Vertex):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

    def validate(self):
        """ Validates this triangle, throwing an error if it is invalid. """
        self.v1.validate()
        self.v2.validate()
        self.v3.validate()

    def as_interleaved_data_array(self):
        """ Convert a triangle's vertex and color data to an interleaved numpy array of single-precision floats.

        Args:
            tri: The triangle.

        Returns:
            data (ndarray): the triangle as an ndarray of form [XYZRGB XYZRGB XYZRGB]
        """
        return array(
            [
                self.v1.pos.x, self.v1.pos.y, self.v1.pos.z, self.v1.color.r, self.v1.color.g, self.v1.color.b,
                self.v2.pos.x, self.v2.pos.y, self.v2.pos.z, self.v2.color.r, self.v2.color.g, self.v2.color.b,
                self.v3.pos.x, self.v3.pos.y, self.v3.pos.z, self.v3.color.r, self.v3.color.g, self.v3.color.b,
            ],
            dtype=float32
        )
