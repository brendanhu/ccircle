from enum import Enum


# Enum of valid vertex attributes.
class VertexAttribute(Enum):
    POSITION_IN = 'vin_position'
    COLOR_IN = 'vin_color'
    UV_IN = 'vin_tex_coord'


# Enum of valid vertex Uniforms.
class VertexUniform(Enum):
    TEX = 'tex'


# Enum of valid user-named variables passed between vertex and fragment shaders.
class IntraShaderVariable(Enum):
    RGBA = 'vout_color'
    UV = 'uv_tex_coord'


# XYZRGB,UV Vertex Shader. Note that the .format()ed string has escaped '{' and '}'
VERTEX_SHADER = """
#version 330

in vec3 {position_in};
in vec4 {color_in};
in vec2 {tex_in};
out vec4 {rgba};
out vec2 {uv};

void main(void) {{
    gl_Position = vec4({position_in}, 1.0);
    {rgba} = {color_in};
    {uv} = {tex_in};
}}
""".format(
    position_in=VertexAttribute.POSITION_IN.value,
    color_in=VertexAttribute.COLOR_IN.value,
    tex_in=VertexAttribute.UV_IN.value,
    rgba=IntraShaderVariable.RGBA.value,
    uv=IntraShaderVariable.UV.value,
)
# RGB Fragment shader.
FRAGMENT_SHADER = """
#version 330

in vec4 {rgba};
out vec4 fout_color;

void main(void) {{
    fout_color = {rgba};
}}
""".format(
    rgba=IntraShaderVariable.RGBA.value,
)
# UV Texture Fragment shader. Note that the .format()ed string has escaped '{' and '}'.
TEXTURE_FRAGMENT_SHADER = """
#version 330

in vec2 {uv};
out vec4 color;

uniform sampler2D {tex};

void main() {{
    color = texture({tex}, {uv});
}}
""".format(
    tex=VertexUniform.TEX.value,
    uv=IntraShaderVariable.UV.value,
)
