""" Run this for an adhoc test demonstrating current cc module functionality. """
from cc.constant import *
from cc.ds.triangle import *
from cc.window import Window
from cc import logging, np

# Create window.
win = Window()
# Misc window info.
x, y = win.get_top_left_corner()
wx, wy = win.get_size()
half_wx = wx / 2.0
half_wy = wy / 2.0
wx_offset_normalized = 0.04
wy_offset_normalized = 0.1

while win.isOpen():
    win.clear(GRAY)

    # Create triangle on mouse by projecting pixels onto 2x2 GL grid.
    mx, my = win.get_mouse_pos()
    px = 2 * mx / wx - 1
    py = 1 - 2 * my / wy
    tri = Triangle(
        Point(px, py, 0.0, RED),
        Point(px + wx_offset_normalized, py - wy_offset_normalized, 0.0, GREEN),
        Point(px - wx_offset_normalized, py - wy_offset_normalized, 0.0, BLUE),
    )
    win.create_tri_vbos(tri)

    # TODO(Brendan) Draw another triangle.

    # # Draw a growing circle.
    # cx = x + (wx / 2)
    # cy = y + (wy / 2)
    # circle_grow_rate = 10
    # radius = int(circle_grow_rate * win.getTime())
    # win.draw_circle(cx, cy, radius, *BLUE_PACKED)


    win.draw()
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
#
# # Draw a small triangle on the mouse pos.
# mx, my = win.get_mouse_pos()
# win.draw_tri(
#     mx, my,
#     mx + 15, my + 20,
#     mx - 15, my + 20,
#     *PURPLE_PACKED
# )
