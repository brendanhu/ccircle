from cc._vertex import Vertex


class VertexCacheReturn:
    """ The return value from VertexCache#lookup().
        Gives the index of the vertex and whether it has already been seen (added to vbo already).
    """
    def __init__(self, index: int, seen: bool):
        self.index = index
        self.seen = seen


class VertexCache:
    """ A 'cache' that tracks unique vertices for a shape. Used to prevent duplicate vertices from being sent to GPU.

    XXX(Brendan): this abstraction could do something cool.
    """

    def __init__(self):
        self.index = 0
        self.map = dict()

    def clear(self):
        self.index = 0
        self.map = dict()

    def incr_index(self):
        """ Return the current self.index and then increment it. """
        idx = self.index
        self.index += 1
        return idx

    def lookup(self, vertex: Vertex) -> VertexCacheReturn:
        """ Get an index from the buffer (map) for this vertex:
            If we already have it, return the corresponding index.
            Otherwise generate another index, add this vertex to the buffer map, and return the new index.

        Returns:
            (VertexCacheReturn): the index of the vertex and whether it has already been seen.
        """
        cur = self.map.get(vertex)
        if cur:
            return VertexCacheReturn(cur, True)
        index = self.incr_index()
        self.map[vertex] = index
        return VertexCacheReturn(index, False)
