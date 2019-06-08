class Color:
    """ A color with an optional alpha. """
    def __init__(self, r: float, g: float, b: float, a: float = 1.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a
