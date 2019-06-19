import ctypes
from typing import List, Generator

from OpenGL.GL import GL_ELEMENT_ARRAY_BUFFER, glVertexAttribPointer, GL_FLOAT, GL_FALSE, glDrawElements, \
    GL_TRIANGLES, \
    glEnableVertexAttribArray, glGenBuffers, \
    glBindBuffer, GL_ARRAY_BUFFER, glBufferData, GL_STATIC_DRAW, GL_UNSIGNED_SHORT, glDisableVertexAttribArray, \
    glActiveTexture, GL_TEXTURE0, glBindTexture, GL_TEXTURE_2D, glUseProgram
from numpy import concatenate, array, uint16

from cc._shader import Shader
from cc._shader_source import VertexAttribute, VertexUniform, FRAGMENT_SHADER, VERTEX_SHADER, TEXTURE_FRAGMENT_SHADER
from cc._vertex_cache import VertexCache
from cc.shapes.shape import Shape
from cc.shapes.triangle import Triangle


class TriangleVbo:
    """ A class to track triangles sent to an (indexed) OpenGL VBO. """

    def __init__(self):
        # Compile and link shaders.
        self.shader = Shader(fragment=FRAGMENT_SHADER, vertex=VERTEX_SHADER)
        self.tex_shader = Shader(fragment=TEXTURE_FRAGMENT_SHADER, vertex=VERTEX_SHADER)

        # Vertex Attributes + Uniforms.
        self.position_attr_idx = self.shader.attribute_index(VertexAttribute.POSITION_IN)
        self.colors_attr_idx = self.shader.attribute_index(VertexAttribute.COLOR_IN)
        self.uv_attr_idx = self.shader.attribute_index(VertexAttribute.UV_IN)
        self.tex_uniform_idx = self.shader.uniform_index(VertexUniform.TEX)

        # Create the OpenGL VBOs (1 for vertex/color, 1 for indices), empty at first.
        self.vertex_vbo, self.indices_vbo = glGenBuffers(2)
        self.vertex_cache = VertexCache()
        self.shapes = []
        self.vertices = []
        self.indices = []

    def offer_shape(self, shape: Shape):
        """ Offer a triangle to this vbo, and let it sort out uniqueness of its vertices.

        Notes:
            All vertices should be of the same type, colored or textured.
        """
        self.shapes.append(shape)

    def add_triangle_indices(self, tri: Triangle):
        """ Add all vertices in triangle to indexed VBO:
            1) Lookup the index
            2) Shove in indices
            3) Store ONLY NEW vertices
        """
        for v in [tri.v1, tri.v2, tri.v3]:
            ret = self.vertex_cache.lookup(v)
            self.indices.append(ret.index)
            if not ret.seen:
                self.vertices.append(v)

    def draw(self):
        """ Draw some triangles. """
        for shape in self.shapes:
            self.__draw(shape)
        self.shapes.clear()

    def __draw(self, shape: Shape):
        """ Draw a shape (texture or colored):
                TODO(Brendan)
        """
        if not shape:
            return

        # Set variables based on texture or colored shape.
        texture = shape.image
        attr2_idx = self.uv_attr_idx if texture else self.colors_attr_idx
        attr_num_floats = 2 if texture else 4
        vertex_bytes = 20 if texture else 28
        shader = self.tex_shader if texture else self.shader

        # Use appropriate shader to use.
        glUseProgram(shader.program_id)

        # Enable the 2 vertex attrib arrays.
        glEnableVertexAttribArray(self.position_attr_idx)
        glEnableVertexAttribArray(attr2_idx)

        # VBO <- data.
        for tri in shape.to_triangles():
            self.add_triangle_indices(tri)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
        data_array = concatenate([v.as_array() for v in self.vertices])
        glBufferData(GL_ARRAY_BUFFER, data_array, GL_STATIC_DRAW)
        glVertexAttribPointer(self.position_attr_idx, 3, GL_FLOAT, GL_FALSE, vertex_bytes, ctypes.c_void_p(0))
        glVertexAttribPointer(attr2_idx, attr_num_floats, GL_FLOAT, GL_FALSE, vertex_bytes, ctypes.c_void_p(12))

        # Index buffer <- indices.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indices_vbo)
        indices = array([self.indices], dtype=uint16)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

        # Draw (Window <- GPU).
        if texture:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, texture.id)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_SHORT, ctypes.c_void_p(0))

        # Cleanup.
        glDisableVertexAttribArray(self.position_attr_idx)
        glDisableVertexAttribArray(attr2_idx)
        self.indices.clear()
        self.vertices.clear()
        self.vertex_cache.clear()

    @staticmethod
    def chunk_on_same_texture(tris: List[Triangle]) -> Generator[List[Triangle], List[Triangle], None]:
        """ Split the list into chunks (multiple lists) of triangles for a draw() call.

        Returns:
            draw_list (List[List[Triangle]]): a list where each element is all contiguous triangles sharing the same
            texture.
        """
        if len(tris) <= 1:
            yield [tris]

        idx = 0
        cur_tex = tris[0].image
        for i in range(1, len(tris)):
            other_tex = tris[i].image
            if cur_tex != other_tex:
                cur_tex = other_tex
                old_idx = idx
                idx = i
                yield tris[old_idx: idx]
        yield tris[idx: len(tris)]
