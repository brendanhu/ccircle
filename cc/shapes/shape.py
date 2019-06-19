""" All shapes are made out of triangles :) """
from abc import ABC, abstractmethod
from typing import Tuple, List

from cc._vertex import Vertex
from cc._vertex_cache import VertexCache
from cc.image import Image


class Shape(ABC):
    def __init__(self, image: Image = None):
        """ An abstract shape that can be drawn using triangles (with optional texture). """
        super().__init__()
        self.image = image

    @abstractmethod
    def to_triangles(self):
        """ Turn this shape into a list of triangles. To be implemented by subclasses.

        Returns:
            tris (List[Triangle]): all the triangles which, when drawn, produce this shape.
        """
        pass

    def is_textured(self) -> bool:
        """ Checks if this shape is textured (as opposed to RGBA colored). """
        return bool(self.image)

    def to_indexed_vertices(self) -> Tuple[List[Vertex], List[int]]:
        """ Decompose this shape into triangles and determine unique vertices (and corresponding indices).
                These vertices and indices are needed to draw this shape with an indexed VBO (index buffer).
            The VertexCache is used to determine vertex uniqueness.

        Returns:
            vertices, indices: the lists describing the decomposition of this shape into triangles with unique vertices.
        """
        indices = []
        vertices = []
        vertex_cache = VertexCache()

        for tri in self.to_triangles():
            for v in [tri.v1, tri.v2, tri.v3]:
                ret = vertex_cache.lookup(v)
                indices.append(ret.index)
                if not ret.seen:
                    vertices.append(v)

        return vertices, indices
