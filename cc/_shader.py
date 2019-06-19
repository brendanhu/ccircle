from OpenGL.GL import glCreateProgram, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glAttachShader, glDeleteShader, \
    glLinkProgram, glGetProgramiv, GL_LINK_STATUS, GL_TRUE, glGetProgramInfoLog, glDeleteProgram, \
    glGetAttribLocation, glCreateShader, glShaderSource, glCompileShader, glGetShaderiv, glGetShaderInfoLog, \
    GL_COMPILE_STATUS, glGetUniformLocation

from cc._shader_source import VertexAttribute, VertexUniform


class Shader:
    """ Basic graphics Shader. """

    def __init__(self, vertex: str, fragment: str):
        """
        Args:
            vertex: String containing shader source code for the vertex shader.
            fragment: String containing shader source code for the fragment shader.
        """
        self.program_id = glCreateProgram()
        vs_id = Shader.add_shader(vertex, GL_VERTEX_SHADER)
        frag_id = Shader.add_shader(fragment, GL_FRAGMENT_SHADER)

        glAttachShader(self.program_id, vs_id)
        glAttachShader(self.program_id, frag_id)
        glDeleteShader(vs_id)
        glDeleteShader(frag_id)
        glLinkProgram(self.program_id)

        if glGetProgramiv(self.program_id, GL_LINK_STATUS) != GL_TRUE:
            info = glGetProgramInfoLog(self.program_id)
            glDeleteProgram(self.program_id)
            raise RuntimeError('Error linking program: %s' % info)

    def attribute_index(self, vertex_attribute: VertexAttribute):
        """ Get index of the vertex attribute for impending glVertexAttribPointer(index) call.

        Args:
            vertex_attribute: the attribute of which we're retrieving the index.

        Returns:
            location (int): Integer describing location (index) of the attribute.
        """
        return glGetAttribLocation(self.program_id, vertex_attribute.value)

    def uniform_index(self, vertex_uniform: VertexUniform):
        return glGetUniformLocation(self.program_id, vertex_uniform.value)

    @staticmethod
    def add_shader(source, shader_type):
        """ Compile GLSL shader.

        Args:
            source (str): String containing shader source code
            shader_type : valid OpenGL shader type; the type of shader to compile

        Returns:
            shader_id (int): shader_id upon successful compilation.
        """
        shader_id = None
        try:
            shader_id = glCreateShader(shader_type)
            glShaderSource(shader_id, source)
            glCompileShader(shader_id)
            if glGetShaderiv(shader_id, GL_COMPILE_STATUS) != GL_TRUE:
                info = glGetShaderInfoLog(shader_id)
                raise RuntimeError('Shader compilation failed: %s' % info)
            return shader_id
        except Exception:
            if shader_id:
                glDeleteShader(shader_id)
            raise
