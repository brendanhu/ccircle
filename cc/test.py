""" Run this for an adhoc test demonstrating current cc module functionality. """
from cc.constant import *
from cc.ds.triangle import *
from cc.window import Window

# Create window.
win = Window()
# Misc window info.
x, y = win.get_top_left_corner()

while win.is_open():
    win.clear(GRAY)

    # Create triangle on mouse.
    mouse = win.get_mouse_pos()
    cursor_tri = Triangle(
        NDCPoint(mouse.x, mouse.y, 0.0, PURPLE),
        NDCPoint(mouse.x + .05, mouse.y - .1, 0.0, PURPLE),
        NDCPoint(mouse.x - .05, mouse.y - .1, 0.0, PURPLE),
    )

    static_tri = Triangle(
        NDCPoint(-1.0, 1.0, 0.0, BLUE),
        NDCPoint(-1.0, 0.0, 0.0, GREEN),
        NDCPoint(-0.5, 0.5, 0.0, PURPLE),
    )

    win.draw_triangles(static_tri, cursor_tri)


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
