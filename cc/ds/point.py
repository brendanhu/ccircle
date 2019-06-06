from cc.ds.color import Color
from cc.constant import BLACK


class NDCPoint:
    def __init__(self, x: float, y: float, z: float = 0.0, color: Color = None):
        """ An OpenGL (vec4) NDC Point with optional z-axis-coordinate and color.

        Notes:
            OpenGL NDC Point: [-1.0, 1.0] in all 3 axes (normalized to unit cube)."""
        self.x = x
        self.y = y
        self.z = z
        self.color = color


# TODO(Brendan): This is so messed up but will be rewritten for textured vertices anyway.
class GLPoint(NDCPoint):
    def __init__(self, x: float, y: float, z: float = 0.0, color: Color = BLACK, size: float = 1.0):
        """ An NDCPoint with a draw size in pixels and a color. Defaults to BLACK.

        Args:
            size: the point size in pixels.
        """
        super().__init__(x, y, z, color)
        self.size = size
