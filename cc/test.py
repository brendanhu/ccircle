""" Run this for an adhoc test demonstrating current cc module functionality. """
import math

from cc.constant import *
from cc.ds.circle import Circle
from cc.ds.triangle import *
from cc.window import Window

# Create window.
win = Window()

while win.is_open():
    win.clear(GRAY)

    # Triangle on mouse.
    mouse = win.get_mouse_pos()
    cursor_tri = Triangle(
        NDCPoint(mouse.x, mouse.y, color=PURPLE),
        NDCPoint(mouse.x + .05, mouse.y - .1, color=PURPLE),
        NDCPoint(mouse.x - .05, mouse.y - .1, color=PURPLE),
    )

    # A stationary triangle.
    static_tri = Triangle(
        NDCPoint(-1.0, 1.0, color=BLUE),
        NDCPoint(-1.0, 0.0, color=GREEN),
        NDCPoint(-0.5, 0.5, color=PURPLE),
    )

    # A circle that changes size over time.
    radius = abs(0.2 * math.sin(win.get_time()))
    growing_circle = Circle(
        NDCPoint(0.0, 0.0, color=GREEN),
        color=BLUE,
        radius=radius,
    )

    # Specify everything to draw (in order).
    win.draw_triangle(static_tri)
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
