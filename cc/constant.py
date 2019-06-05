""" Constants for the ccircle (cc) module. """
from cc.ds.color import Color
from enum import Enum

LOGGER_LEVEL = 'DEBUG'

RED = Color(1.0, 0.0, 0.0)
GREEN = Color(0.0, 1.0, 0.0)
BLUE = Color(0.0, 0.0, 1.0)
PURPLE = Color(0.6, 0.0, 0.7)
GRAY = Color(0.1, 0.1, 0.1)


# Enum of valid vertex attributes.
class VertexAttribute(Enum):
    POSITION_IN = 'vin_position'
    COLOR_IN = 'vin_color'


# Vertex Shader. Note that the .format()ed string has escaped '{' and '}'
VERTEX_SHADER = """
#version 330

in vec3 {position_in};
in vec3 {color_in};
out vec3 vout_color;

void main(void)
{{
    gl_Position = vec4({position_in}, 1.0);
    vout_color = {color_in};
}}
""".format(
    position_in=VertexAttribute.POSITION_IN.name,
    color_in=VertexAttribute.COLOR_IN.name
)
# Fragment shader.
FRAGMENT_SHADER = """
#version 330

in vec3 vout_color;
out vec4 fout_color;

void main(void)
{
    fout_color = vec4(vout_color, 1.0);
}
"""
