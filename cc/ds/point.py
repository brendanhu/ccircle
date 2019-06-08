from cc.ds.color import Color


class NDCPoint:
    """ An OpenGL (vec4) NDC Point with optional z-axis-coordinate and color.

        Notes:
            OpenGL NDC Point: [-1.0, 1.0] in all 3 axes (normalized to unit cube).
    """
    def __init__(self, x: float, y: float, z: float = 0.0, color: Color = None):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
