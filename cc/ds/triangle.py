from cc import np
from cc.ds.point import Point


class Triangle:
    def __init__(self, p1: Point, p2: Point, p3: Point):
        """OOP representation of a 3D triangle comprised of 3 Points."""
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def vertices_as_array(self):
        """ TODO(Brendan): doc"""
        return np.array([self.p1.x, self.p1.y, self.p1.z,
                         self.p2.x, self.p2.y, self.p2.z,
                         self.p3.x, self.p3.y, self.p3.z], dtype=np.float32)

    def colors_as_array(self):
        """ TODO(Brendan): doc"""
        return np.array([self.p1.color.r, self.p1.color.g, self.p1.color.b,
                         self.p2.color.r, self.p2.color.g, self.p2.color.b,
                         self.p3.color.r, self.p3.color.g, self.p3.color.b], dtype=np.float32)
