class Vec4:
    """ An object used to store 4 floats.
        Generally used as an OpenGL homogeneous coordinate (*1) in NDC ([-1.0, 1.0]) where:
            If w == 1, then the vector (x,y,z,1) is a position in space.
            If w == 0, then the vector (x,y,z,0) is a direction.

    Notes:
        This isn't needed until 3D, but better than having to refactor a Position class.

    *1: https://en.wikipedia.org/wiki/Homogeneous_coordinates
    """
    def __init__(self, x: float, y: float, z: float = 0.0, w: float = 1.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __eq__(self, other):
        return \
            self.x == other.x and \
            self.y == other.y and \
            self.z == other.z and \
            self.w == other.w
