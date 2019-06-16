from cc._vec4 import Vec4


class Color(Vec4):
    """ A (linear RGB 0-1) color with an optional alpha.
        Creation via 0-255 values is supported via Color#from255().
    """
    def __init__(self, r: float, g: float, b: float, a: float = 1.0):
        super().__init__(
            x=r,
            y=g,
            z=b,
            w=a,
        )
        self.r = self.x
        self.g = self.y
        self.b = self.z
        self.a = self.w

    def is_valid(self) -> bool:
        """ Validates rgba in [0.0, 1.0]. """
        return \
            0.0 <= self.r <= 1.0 and \
            0.0 <= self.g <= 1.0 and \
            0.0 <= self.b <= 1.0 and \
            0.0 <= self.a <= 1.0

    @staticmethod
    def from255(r: int, g: int, b: int, a: float = 1.0):
        """ Create a color via sRGB values. Alpha should still be within [0.0, 1.0]"""
        return Color(
            r / 255.0,
            g / 255.0,
            b / 255.0,
            a
        )
