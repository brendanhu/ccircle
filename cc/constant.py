""" Constants for the ccircle (cc) module. """
from cc.ds.color import Color

LOGGER_LEVEL = 'DEBUG'

# Colors.
RED_PACKED = [0.7, 0.0, 0.0]
GREEN_PACKED = [0.0, 0.7, 0.0]
BLUE_PACKED = [0.0, 0.0, 0.7]
PURPLE_PACKED = [0.6, 0.0, 0.7]
RED = Color(1.0, 0.0, 0.0)
GREEN = Color(0.0, 1.0, 0.0)
BLUE = Color(0.0, 0.0, 1.0)
GRAY = Color(0.1, 0.1, 0.1)

# Shaders.
VERTEX_SHADER = """
#version 330
in vec3 vin_position;
in vec3 vin_color;
out vec3 vout_color;
void main(void)
{
    vout_color = vin_color;
    gl_Position = vec4(vin_position, 1.0);
}
"""
FRAGMENT_SHADER = """
#version 330
in vec3 vout_color;
out vec4 fout_color;
void main(void)
{
    fout_color = vec4(vout_color, 1.0);
}
"""
