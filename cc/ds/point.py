from cc.ds import color


class Point:
    def __init__(self, x: float, y: float, z: float, color: color):
        """OOP representation of a 3D Point with an optional color."""
        self.x = x
        self.y = y
        self.z = z
        self.color = color
