from cc import gl
from cc.constant import VertexAttribute


class Shader:
    """ Our graphics Shader. """
    def __init__(self, vertex, fragment):
        """
        Args:
            vertex (str): String containing shader source code for the vertex shader
            fragment (str): String containing shader source code for the fragment shader
        """
        self.program_id = gl.glCreateProgram()
        vs_id = Shader.add_shader(vertex, gl.GL_VERTEX_SHADER)
        frag_id = Shader.add_shader(fragment, gl.GL_FRAGMENT_SHADER)

        gl.glAttachShader(self.program_id, vs_id)
        gl.glAttachShader(self.program_id, frag_id)
        gl.glDeleteShader(vs_id)
        gl.glDeleteShader(frag_id)
        gl.glLinkProgram(self.program_id)
        gl.glUseProgram(self.program_id)

        if gl.glGetProgramiv(self.program_id, gl.GL_LINK_STATUS) != gl.GL_TRUE:
            info = gl.glGetProgramInfoLog(self.program_id)
            gl.glDeleteProgram(self.program_id)
            raise RuntimeError('Error linking program: %s' % info)

    def attribute_index(self, vertex_attribute: VertexAttribute):
        """ Get index of the vertex attribute for impending glVertexAttribPointer(index) call.

        Args:
            vertex_attribute: the attribute of which we're retrieving the index.

        Returns:
            location (int): Integer describing location (index) of the attribute.
        """
        return gl.glGetAttribLocation(self.program_id, vertex_attribute.name)

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
            shader_id = gl.glCreateShader(shader_type)
            gl.glShaderSource(shader_id, source)
            gl.glCompileShader(shader_id)
            if gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS) != gl.GL_TRUE:
                info = gl.glGetShaderInfoLog(shader_id)
                raise RuntimeError('Shader compilation failed: %s' % info)
            return shader_id
        except Exception:
            if shader_id:
                gl.glDeleteShader(shader_id)
            raise
