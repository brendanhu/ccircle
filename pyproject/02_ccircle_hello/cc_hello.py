""" Run this for an adhoc test demonstrating current cc module functionality. """
import math

from cc.colors import *
from cc.position import Position
from cc.shapes.circle import Circle
from cc.shapes.triangle import Triangle
from cc.vertex import Vertex
from cc.window import Window

# Create window.
win = Window()

while win.is_open():
    win.clear(DARK_GRAY)

    # Triangle on mouse.
    mouse = win.get_mouse_pos()
    cursor_tri = Triangle(
        Vertex(Position(mouse.x, mouse.y), color=BLUE6),
        Vertex(Position(mouse.x + .05, mouse.y - .1), color=BLUE5),
        Vertex(Position(mouse.x - .05, mouse.y - .1), color=BLUE6),
    )

    # A circle that changes size over time.
    radius = abs(0.3 * math.sin(win.get_time()))
    growing_circle = Circle(
        Vertex(Position(0.0, 0.0), color=BLUE),
        color=GREEN,
        radius=radius,
    )

    # Specify what to draw in order.
    win.draw_circle(growing_circle)
    win.draw_triangle(cursor_tri)

    # Draw!
    win.update()
win.close()

# TODO(Brendan): implement below.
# # Draw a line.
# win.draw_line(right_side, cy, right_side, cy + wy, 3.0, *GREEN_PACKED)

# # Draw a rectangle.
# ry = y + wy - ten_percent_y
# win.draw_rect(x, y, ten_percent_x, ten_percent_y, *RED_PACKED)
