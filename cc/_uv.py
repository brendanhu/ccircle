from numpy import ndarray, array, float32, allclose


class UV:
    """ Abstraction for vertex UV (how to map a texture to this vertex). """
    def __init__(self, u: float, v: float):
        self.u = u
        self.v = v

    def as_array(self) -> ndarray:
        """ Transform this uv into a vec2 single-precision ndarray of floats: [UV]. """
        return array([self.u, self.v], dtype=float32)

    def as_list(self) -> list:
        return [self.u, self.v]

    def is_valid(self) -> bool:
        """ Checks if this represents a valid uv texture coordinate. """
        return \
            0.0 <= self.u <= 1.0 and \
            0.0 <= self.v <= 1.0


    def __eq__(self, other) -> bool:
        """ Equality check. """
        return allclose(self.as_list(), other.as_list())
