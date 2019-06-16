from enum import Enum


# Enum of valid vertex attributes.
class VertexAttribute(Enum):
    POSITION_IN = 'vin_position'
    COLOR_IN = 'vin_color'
    TEX_IN = 'vin_tex_coord'


# Enum of valid user-named variables passed between vertex and fragment shaders.
class IntraShaderVariable(Enum):
    RGB = 'vout_color'
    UV = 'uv_tex_coord'


# XYZRGB,UV Vertex Shader. Note that the .format()ed string has escaped '{' and '}'
VERTEX_SHADER = """
#version 330

in vec3 {position_in};
in vec3 {color_in};
in vec2 {tex_in};
out vec3 {rgb};
out vec2 {uv};

void main(void) {{
    gl_Position = vec4({position_in}, 1.0);
    {rgb} = {color_in};
    {uv} = {tex_in};
}}
""".format(
    position_in=VertexAttribute.POSITION_IN.value,
    color_in=VertexAttribute.COLOR_IN.value,
    tex_in=VertexAttribute.TEX_IN.value,
    rgb=IntraShaderVariable.RGB.value,
    uv=IntraShaderVariable.UV.value,
)
# RGB Fragment shader.
FRAGMENT_SHADER = """
#version 330

in vec3 {rgb};
out vec4 fout_color;

void main(void) {{
    fout_color = vec4({rgb}, 1.0);
}}
""".format(
   rgb=IntraShaderVariable.RGB.value,
)
# UV Texture Fragment shader. Note that the .format()ed string has escaped '{' and '}'.
TEXTURE_FRAGMENT_SHADER = """
#version 330

in vec2 {uv};
out vec4 color;

uniform sampler2D tex;

void main() {{
    color = texture(tex, {uv});
}}
""".format(
    uv=IntraShaderVariable.UV.value,
)
