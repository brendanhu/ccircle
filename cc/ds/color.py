from cc.util import clamp_rgba


class Color:
    def __init__(self, r: float, g: float, b: float, a: float = 1.0):
        """ A color with an optional alpha. Values silently clamped to [0.0, 1.0]. """
        self.r = clamp_rgba(r)
        self.g = clamp_rgba(g)
        self.b = clamp_rgba(b)
        self.a = clamp_rgba(a)

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
