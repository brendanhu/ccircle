class Color:
    def __init__(self, r: float, g: float, b: float, a: float = 1.0):
        """ A color with an optional alpha. """
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def to_list(self):
        """ Returns an array representation of the color.

        Returns:
            [r, g, b, a]: the rgba values as a list.
        """
        return [
            self.r,
            self.g,
            self.b,
            self.a,
        ]
