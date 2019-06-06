from cc.ds import color


class NDCPoint:
    def __init__(self, x: float, y: float, z: float, color: color = None):
        """ An OpenGL (vec4) NDC Point with an optional color.

        Notes:
            OpenGL NDC Point: [-1.0, 1.0] in all 3 axes (normalized to unit cube)."""
        self.x = x
        self.y = y
        self.z = z
        self.color = color
