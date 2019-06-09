class Color:
    """ A (linear RGB 0-1) color with an optional alpha.
        Creation via sRGB values (0-255) is supported via Color#sRgb().
    """

    def __init__(self, r: float, g: float, b: float, a: float = 1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    @staticmethod
    def sRgb(r: int, g: int, b: int, a: float = 1.0):
        """ Create a color via sRGB values. Alpha should still be within [0.0, 1.0]"""
        return Color(
            r / 255.0,
            g / 255.0,
            b / 255.0,
            a
        )
