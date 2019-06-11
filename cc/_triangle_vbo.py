import ctypes

from OpenGL.GL import GL_ELEMENT_ARRAY_BUFFER, glVertexAttribPointer, GL_FLOAT, GL_FALSE, glDrawElements, \
    GL_TRIANGLES, \
    glClear, GL_COLOR_BUFFER_BIT, glEnableVertexAttribArray, glBindVertexArray, glGenBuffers, \
    glBindBuffer, GL_ARRAY_BUFFER, glBufferData, GL_STATIC_DRAW, GL_UNSIGNED_SHORT
from numpy import concatenate, array, uint16

from cc._shader import Shader
from cc._shader_source import VertexAttribute
from cc._vertex_cache import VertexCache
from cc.shapes.triangle import Triangle
from cc.vertex import Vertex


class TriangleVbo:
    """ A class to track triangles sent to an (indexed) OpenGL VBO. """

    def __init__(self, shader: Shader):
        self.position_attr_idx = shader.attribute_index(VertexAttribute.POSITION_IN)
        self.colors_attr_idx = shader.attribute_index(VertexAttribute.COLOR_IN)
        glEnableVertexAttribArray(self.position_attr_idx)
        glEnableVertexAttribArray(self.colors_attr_idx)
        glBindVertexArray(0)

        # Create the OpenGL VBOs (1 for vertex/color, 1 for indices), empty at first.
        self.vertex_vbo, self.indices_vbo = glGenBuffers(2)
        self.vertex_cache = VertexCache()
        self.vertices = []
        self.indices = []

    def offer_triangle(self, tri: Triangle):
        """ Offer a triangle to this vbo, and let it sort out uniqueness of its vertices. """
        self.add_vertex(tri.v1)
        self.add_vertex(tri.v2)
        self.add_vertex(tri.v3)

    def add_vertex(self, v: Vertex):
        """ Lookup the index, shove in indices, and store ONLY NEW vertices."""
        ret = self.vertex_cache.lookup(v)
        self.indices.append(ret.index)
        if not ret.seen:
            self.vertices.append(v)

    def draw(self):
        """ Draw some triangles.

        TODO(Brendan): bad magic numbers.
        """
        if not self.vertices:
            return

        # VBO <- data.
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
        data_array = concatenate([v.as_array() for v in self.vertices])
        glBufferData(GL_ARRAY_BUFFER, data_array, GL_STATIC_DRAW)
        glVertexAttribPointer(self.position_attr_idx, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glVertexAttribPointer(self.colors_attr_idx, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

        # Index buffer <- indices.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indices_vbo)
        indices = array([self.indices], dtype=uint16)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        # Draw (Window <- GPU).
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_SHORT, ctypes.c_void_p(0))

        # Reset local vars.
        self.indices = []
        self.vertices = []
        self.vertex_cache.clear()
