from cc.point import NDCPoint


class Triangle:
    """ An NDC-compatible triangle comprised of 3 NDCPoints. """
    def __init__(self, p1: NDCPoint, p2: NDCPoint, p3: NDCPoint):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
