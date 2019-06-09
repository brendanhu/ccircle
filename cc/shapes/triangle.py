from cc.vertex import Vertex


class Triangle:
    """ An NDC-compatible triangle comprised of 3 Vertices. """
    def __init__(self, p1: Vertex, p2: Vertex, p3: Vertex):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
