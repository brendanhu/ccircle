""" Run this for an adhoc test demonstrating current cc module functionality. """
from cc.constant import *
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


    # Specify everything to draw and update.
    win.draw_triangle(static_tri)
    win.draw_triangle(cursor_tri)
    win.update()
win.close()

# TODO(Brendan): implement below.
# # Draw a growing circle.
# cx = x + (wx / 2)
# cy = y + (wy / 2)
# circle_grow_rate = 10
# radius = int(circle_grow_rate * win.getTime())
# win.draw_circle(cx, cy, radius, *BLUE_PACKED)

# # Draw a stupid-big point.
# right_side = x + wx - ten_percent_x
# win.draw_point(right_side, cy, 100.0, *RED_PACKED)

# # Draw a line.
# win.draw_line(right_side, cy, right_side, cy + wy, 3.0, *GREEN_PACKED)

# # Draw a rectangle.
# ry = y + wy - ten_percent_y
# win.draw_rect(x, y, ten_percent_x, ten_percent_y, *RED_PACKED)
