""" Run this for an adhoc test demonstrating current cc module functionality. """
from cc.constant import *
from cc.ds.triangle import *
from cc.window import Window

# Create window.
win = Window()
# Misc window info.
x, y = win.get_top_left_corner()
wx, wy = win.get_size()
half_wx = wx / 2.0
half_wy = wy / 2.0
wx_offset_normalized = 0.04
wy_offset_normalized = 0.1

while win.is_open():
    win.clear(GRAY)

    # Create triangle on mouse by projecting pixels onto 2x2 GL grid.
    # TODO(Brendan): pull into window.py so user deals with pixels instead of [-1, 1]?
    mx, my = win.get_mouse_pos()
    px = 2 * mx / wx - 1
    py = 1 - 2 * my / wy
    cursor_tri = Triangle(
        NDCPoint(px, py, 0.0, RED),
        NDCPoint(px + wx_offset_normalized, py - wy_offset_normalized, 0.0, GREEN),
        NDCPoint(px - wx_offset_normalized, py - wy_offset_normalized, 0.0, BLUE),
    )

    tri2 = Triangle(
        NDCPoint(-1.0, 1.0, 0.0, BLUE),
        NDCPoint(-1.0, 0.0, 0.0, GREEN),
        NDCPoint(-0.5, 0.5, 0.0, PURPLE),
    )

    win.draw_triangles(cursor_tri, tri2)

    # # Draw a growing circle.
    # cx = x + (wx / 2)
    # cy = y + (wy / 2)
    # circle_grow_rate = 10
    # radius = int(circle_grow_rate * win.getTime())
    # win.draw_circle(cx, cy, radius, *BLUE_PACKED)
win.close()

# # Draw a stupid-big point.
# right_side = x + wx - ten_percent_x
# win.draw_point(right_side, cy, 100.0, *RED_PACKED)
#
# # Draw a line.
# win.draw_line(right_side, cy, right_side, cy + wy, 3.0, *GREEN_PACKED)
#
# # Draw a rectangle.
# ry = y + wy - ten_percent_y
# win.draw_rect(x, y, ten_percent_x, ten_percent_y, *RED_PACKED)
