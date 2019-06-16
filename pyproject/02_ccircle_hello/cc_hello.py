""" Run this for an adhoc test demonstrating current cc module functionality. """
import math

from cc import util
from cc._texture import Texture
from cc._uv import UV
from cc.colors import *
from cc.position import Position
from cc.shapes.circle import Circle
from cc.shapes.triangle import Triangle
from cc.vertex import Vertex
from cc.window import Window

# Create window.
win = Window()

# Create all textures just once.
hazard_texture = Texture(util.get_cc_image_path('../pyproject/02_ccircle_hello/hazard.png'))
rainbow_texture = Texture(util.get_cc_image_path('../pyproject/02_ccircle_hello/rainbow.png'))

while win.is_open():
    win.clear(DARK_GRAY)

    # 'Hazard' textured triangle below mouse (cursor).
    mouse = win.get_mouse_pos()
    hazard_cursor = Triangle(
        Vertex(Position(mouse.x, mouse.y), uv=UV(0.5, 1.0)),
        Vertex(Position(mouse.x + .05, mouse.y - .1), uv=UV(0.0, 0.0)),
        Vertex(Position(mouse.x - .05, mouse.y - .1), uv=UV(1.0, 0.0)),
        hazard_texture
    )

    # Static rainbow triangle on right.
    rainbow = Triangle(
        Vertex(Position(0.5, 0.5), uv=UV(0.5, 1.0)),
        Vertex(Position(0.35, 0.2), uv=UV(0.0, 0.0)),
        Vertex(Position(0.65, 0.2), uv=UV(1.0, 0.0)),
        rainbow_texture
    )

    # A circle that changes size over time.
    radius = abs(0.3 * math.sin(win.get_time()))
    growing_circle = Circle(
        Vertex(Position(0.0, 0.0), color=BLUE),
        color=GREEN,
        radius=radius,
    )

    # Specify what to draw (in order).
    win.draw_triangle(rainbow)
    win.draw_circle(growing_circle)
    win.draw_triangle(hazard_cursor)

    # Draw!
    win.update()
win.close()

# TODO(Brendan): implement below.
# # Draw a line.
# win.draw_line(right_side, cy, right_side, cy + wy, 3.0, *GREEN_PACKED)

# # Draw a rectangle.
# ry = y + wy - ten_percent_y
# win.draw_rect(x, y, ten_percent_x, ten_percent_y, *RED_PACKED)
