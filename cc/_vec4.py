from typing import List

from numpy import allclose


class Vec4:
    """ An object used to store 4 floats.
        Generally used as an OpenGL homogeneous coordinate (*1) in NDC ([-1.0, 1.0]) where:
            If w == 1, then the vector (x,y,z,1) is a position in space.
            If w == 0, then the vector (x,y,z,0) is a direction.

    Notes:
        This isn't needed until 3D.

    *1: https://en.wikipedia.org/wiki/Homogeneous_coordinates
    """

    def __init__(self, x: float, y: float, z: float = 0.0, w: float = 1.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __eq__(self, other) -> bool:
        """ Equality check.
            Uses numpy's allclose, which WILL need to be adjusted because floating point arithmetic is silly.
        """
        return allclose(self.as_list(), other.as_list())

    def __str__(self) -> str:
        return "[x, y, z, w] = [%.4f, %.4f, %.4f, %.4f]" % (self.x, self.y, self.z, self.w)

    def as_list(self) -> List[float]:
        return [self.x, self.y, self.z, self.w]
