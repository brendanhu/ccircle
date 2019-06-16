import ctypes
from typing import List, Generator

from OpenGL.GL import GL_ELEMENT_ARRAY_BUFFER, glVertexAttribPointer, GL_FLOAT, GL_FALSE, glDrawElements, \
    GL_TRIANGLES, \
    glEnableVertexAttribArray, glGenBuffers, \
    glBindBuffer, GL_ARRAY_BUFFER, glBufferData, GL_STATIC_DRAW, GL_UNSIGNED_SHORT, glDisableVertexAttribArray, \
    glActiveTexture, GL_TEXTURE0, glBindTexture, GL_TEXTURE_2D, glUseProgram
from numpy import concatenate, array, uint16

from cc._shader import Shader
from cc._shader_source import VertexAttribute
from cc._vertex_cache import VertexCache
from cc.shapes.triangle import Triangle


class TriangleVbo:
    """ A class to track triangles sent to an (indexed) OpenGL VBO. """

    def __init__(self, shader: Shader):
        self.shader = shader

        # Vertex Attributes.
        self.position_attr_idx = shader.attribute_index(VertexAttribute.POSITION_IN)
        self.colors_attr_idx = shader.attribute_index(VertexAttribute.COLOR_IN)

        # Vertex Uniforms.
        if shader.is_for_textures:
            self.tex_attr_idx = shader.attribute_index(VertexAttribute.TEX_IN)

        # Create the OpenGL VBOs (1 for vertex/color, 1 for indices), empty at first.
        self.vertex_vbo, self.indices_vbo = glGenBuffers(2)
        self.vertex_cache = VertexCache()
        self.triangles = []
        self.vertices = []
        self.indices = []

    def offer_triangle(self, tri: Triangle):
        """ Offer a triangle to this vbo, and let it sort out uniqueness of its vertices.

        Notes:
            All vertices should be of the same type, colored or textured.
        """
        if not ((tri.v1.uv and tri.v2.uv and tri.v2.uv) or
                (tri.v1.color and tri.v2.color and tri.v3.color)):
            raise RuntimeError("Triangle's vertices must be all textured OR all colored.")
        self.triangles.append(tri)

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
        if not self.triangles:
            return

        glUseProgram(self.shader.program_id)
        if self.shader.is_for_textures:
            self.__draw_textured()
        else:
            self.__draw_colored()
        glUseProgram(0)

    def __draw_textured(self):
        """ Draw some textured triangles:
                1) Enable vertex attrib arrays.
                2) Fill indexed VBO with triangles' vertices (with dedup).
                3) Make draw call(s).
                4) Cleanup.

        Notes:
            There is a necessary draw() call per contiguous-triangles-using-same-texture:
                i.e. this is 3 draw() calls:
                    Triangle1(texture1)
                    Triangle2(texture2)
                    Triangle3(texture1)
                i.e. this is 2 draw() calls:
                    Triangle1(texture1)
                    Triangle3(texture1)
                    Triangle2(texture2)
            """
        # Enable vertex attrib arrays.
        glEnableVertexAttribArray(self.position_attr_idx)
        glEnableVertexAttribArray(self.tex_attr_idx)

        # VBO <- data.
        for draw_chunk in TriangleVbo.chunk_on_same_texture(self.triangles):
            texture = draw_chunk[0].texture
            for tri in draw_chunk:
                self.add_triangle_indices(tri)

            glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
            data_array = concatenate([v.as_array() for v in self.vertices])
            glBufferData(GL_ARRAY_BUFFER, data_array, GL_STATIC_DRAW)
            glVertexAttribPointer(self.position_attr_idx, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
            glVertexAttribPointer(self.tex_attr_idx, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))

            # Index buffer <- indices.
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indices_vbo)
            indices = array([self.indices], dtype=uint16)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

            # Draw (Window <- GPU).
            if self.shader.is_for_textures:
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, texture.id)
            glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_SHORT, ctypes.c_void_p(0))

            # Cleanup for this draw call.
            self.indices = []
            self.vertices = []
            self.vertex_cache.clear()

        # Cleanup after all textured triangles are drawn.
        self.triangles = []
        glDisableVertexAttribArray(self.position_attr_idx)
        glDisableVertexAttribArray(self.tex_attr_idx)

    def __draw_colored(self):
        """ Draw some colored triangles:
                1) Enable vertex attrib arrays.
                2) Fill indexed VBO with triangles' vertices (with dedup).
                3) Make single draw call.
                4) Cleanup.
        """
        # Enable vertex attrib arrays.
        glEnableVertexAttribArray(self.position_attr_idx)
        glEnableVertexAttribArray(self.colors_attr_idx)

        for tri in self.triangles:
            self.add_triangle_indices(tri)
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

        # Cleanup.
        glDisableVertexAttribArray(self.position_attr_idx)
        glDisableVertexAttribArray(self.colors_attr_idx)
        self.indices = []
        self.vertices = []
        self.triangles = []
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
        cur_tex = tris[0].texture
        for i in range(1, len(tris)):
            other_tex = tris[i].texture
            if cur_tex != other_tex:
                cur_tex = other_tex
                old_idx = idx
                idx = i
                yield tris[old_idx: idx]
        yield tris[idx: len(tris)]
