""" Run this for an adhoc test demonstrating current cc module functionality. """
from cc.constant import *
from cc.window import Window
from cc import logging

win = Window()

while win.isOpen():
    # Clear the window.
    win.clear(*GRAY_PACKED)

    # Mouse and window information.
    mx, my = win.get_mouse_pos()
    x, y = win.get_top_left_corner()
    wx, wy = win.get_size()
    ten_percent_x = wx / 10
    ten_percent_y = wy / 10

    # Draw a growing circle.
    cx = x + (wx / 2)
    cy = y + (wy / 2)
    circle_grow_rate = 10
    radius = int(circle_grow_rate * win.getTime())
    win.draw_circle(cx, cy, radius, *BLUE_PACKED)

    # Draw a stupid-big point.
    right_side = x + wx - ten_percent_x
    win.draw_point(right_side, cy, 100.0, *RED_PACKED)

    # Draw a line.
    win.draw_line(right_side, cy, right_side, cy + wy, 3.0, *GREEN_PACKED)

    # Draw a rectangle.
    ry = y + wy - ten_percent_y
    win.draw_rect(x, y, ten_percent_x, ten_percent_y, *RED_PACKED)

    # Draw a small triangle on the mouse pos.
    win.draw_tri(
        mx, my,
        mx + 15, my + 20,
        mx - 15, my + 20,
        *PURPLE_PACKED
    )

    # Update window with new scene.
    win.update()
win.close()
