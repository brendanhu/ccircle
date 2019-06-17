""" Run this for an adhoc test to demonstrate cc module functionality. """
import math

import cc.colors as colors
from cc.image import Image
from cc.window import Window

# Create window.
win = Window()


# Load any images just once.
rainbow_img = Image('pyproject/02_ccircle_hello/rainbow.png')

while win.is_open():
    win.clear(colors.DARK_GRAY)

    # Misc window info.
    wx, wy = win.get_size()
    cx, cy = wx / 2, wy / 2
    wx_fifth = int(wx / 5)
    wy_fifth = int(wy / 5)
    wx_twentieth = int(wx / 20)
    wy_twentieth = int(wy / 20)

    # Static rectangle background.
    border = 10
    win.drawRect(
        x=border,
        y=border,
        width=wx - (2 * border),
        height=wy - (2 * border),
        r=colors.GRAY.r, g=colors.GRAY.g, b=colors.GRAY.b,
    )

    # Static rainbow image on right.
    win.drawImage(
        rainbow_img,
        x=cx + wx_twentieth,
        y=wy_twentieth,
        width=wx_fifth,
        height=wy_fifth,
    )

    # A circle that changes size over time.
    max_radius = wx_fifth
    radius = int(abs(max_radius * math.sin(win.get_time())))
    win.drawCircle(
        x=cx,
        y=cy,
        radius=radius,
        center_color=colors.BLUE20,
        outer_color=colors.RED,
    )

    # Triangle that moves with the mouse (cursor).
    mouse_pos = win.get_mouse_pos()
    mx, my = mouse_pos.x, mouse_pos.y
    win.drawTri(
        x1=mx, y1=my,
        x2=mx + wx_twentieth, y2=my + wy_twentieth,
        x3=mx - wx_twentieth, y3=my + wy_twentieth,
        r=colors.PURPLE.r, g=colors.PURPLE.g, b=colors.PURPLE.b,
    )

    # Draw!
    win.update()
win.close()
