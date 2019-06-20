import ctypes

from OpenGL.GL import GL_ELEMENT_ARRAY_BUFFER, glVertexAttribPointer, GL_FLOAT, GL_FALSE, glDrawElements, \
    GL_TRIANGLES, \
    glEnableVertexAttribArray, glGenBuffers, \
    glBindBuffer, GL_ARRAY_BUFFER, glBufferData, GL_STATIC_DRAW, GL_UNSIGNED_SHORT, glDisableVertexAttribArray, \
    glActiveTexture, GL_TEXTURE0, glBindTexture, GL_TEXTURE_2D, glUseProgram
from numpy import concatenate, array, uint16

from cc._shader import Shader
from cc._shader_source import VertexAttribute, VertexUniform, FRAGMENT_SHADER, VERTEX_SHADER, TEXTURE_FRAGMENT_SHADER
from cc.shapes.shape import Shape


class IndexedVbo:
    """ A class to track shapes drawn through an indexed OpenGL VBO. """

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
        self.shapes = []

    def offer_shape(self, shape: Shape):
        """ Offer a triangle to this vbo, and let it sort out uniqueness of its vertices. """
        self.shapes.append(shape)

    def draw(self):
        """ Draw some triangles. """
        for shape in self.shapes:
            self.__draw(shape)
        self.shapes.clear()

    def __draw(self, shape: Shape):
        """ Draw a shape (texture or colored) with the indexed VBO.
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

        # Decompose the shape into vertices and indices for VBO and Index Buffer.
        vertices, indices = shape.to_indexed_vertices()

        # VBO <- vertices.
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
        data_array = concatenate([v.as_array() for v in vertices])
        glBufferData(GL_ARRAY_BUFFER, data_array, GL_STATIC_DRAW)
        glVertexAttribPointer(self.position_attr_idx, 3, GL_FLOAT, GL_FALSE, vertex_bytes, ctypes.c_void_p(0))
        glVertexAttribPointer(attr2_idx, attr_num_floats, GL_FLOAT, GL_FALSE, vertex_bytes, ctypes.c_void_p(12))

        # Index buffer <- indices.
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indices_vbo)
        indices_arr = array(indices, dtype=uint16)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_arr, GL_STATIC_DRAW)

        # Draw (Window <- GPU).
        if texture:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, texture.id)
        glDrawElements(GL_TRIANGLES, len(indices_arr), GL_UNSIGNED_SHORT, ctypes.c_void_p(0))

        # Cleanup.
        glDisableVertexAttribArray(self.position_attr_idx)
        glDisableVertexAttribArray(attr2_idx)
