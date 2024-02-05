""" Run this to demonstrate the cc module's functionality.
    Demonstrates possibility of arbitrarily complex scenes through a 'simple' scene of texture-on-color-on-texture,
    and an fps counter.

    TODO(Brendan): this is growing out of control! Split into multiple files.
"""
import math

import cc.colors as colors
from cc.font import Font
from cc.image import Image
from cc.text import Text
from cc.window import Window

# Create window.
win = Window()
win.hide_cursor()

# Load any images or fonts just once.
rainbow_img = Image.from_path('cc_student/assets/images/rainbow.png')
hazard_img = Image.from_path('cc_student/assets/images/hazard.png')
pizza_img = Image.from_path('cc_student/assets/images/pizza.png')
nova_flat_26 = Font('cc_student/assets/fonts/NovaFlat.ttf', 26)
aller_Lt_70 = Font('cc_student/assets/fonts/Aller_Lt.ttf', 70)
ralewayExtraBold_70 = Font('cc_student/assets/fonts/Raleway-ExtraBold.ttf', 70)
ralewaySemiBold_70 = Font('cc_student/assets/fonts/Raleway-SemiBold.ttf', 70)

# Load static text just once.
coding_aller = Text(text=f'CODING ', font=aller_Lt_70, color=colors.CC_DARK_BLUE)
coding_reb = Text(text=f'CODING ', font=ralewayExtraBold_70, color=colors.CC_DARK_BLUE)
coding_rsb = Text(text=f'CODING ', font=ralewaySemiBold_70, color=colors.CC_DARK_BLUE)
circle_aller = Text(text=f'CIRCLE', font=aller_Lt_70, color=colors.CC_LIGHT_BLUE)
circle_reb = Text(text=f'CIRCLE', font=ralewayExtraBold_70, color=colors.CC_LIGHT_BLUE)
circle_rsb = Text(text=f'CIRCLE', font=ralewaySemiBold_70, color=colors.CC_LIGHT_BLUE)

last_update_and_fps = [0.0, 0.0]
last_frame_time = win.get_time()

while win.is_open():
    win.clear(colors.WHITE)

    # Misc window info.
    wx, wy = win.get_size()
    cx, cy = wx / 2, wy / 2
    wx_fifth = wx // 5
    wy_fifth = wy // 5
    wx_twentieth = wx // 20
    wy_twentieth = wy // 20

    # Layer 1: Rainbow backdrop on bottom half the screen.
    win.draw_image(
        image=rainbow_img,
        x=0,
        y=cy,
        width=wx,
        height=wy,
    )

    # Layer 2: Bottom-left: Static pizza.
    win.draw_image(
        image=pizza_img,
        x=wx_fifth,
        y=cy + wy_fifth,
        width=wx_fifth,
        height=wy_fifth,
    )

    # Layer 3: Semi-transparent gray box.
    gray_box_border = wx_twentieth
    win.drawRect(
        x=gray_box_border,
        y=cy + gray_box_border,
        width=wx - (2 * gray_box_border),
        height=cy - (2 * gray_box_border),
        color=colors.GRAY_SEMI_TRANSPARENT,
    )

    # Layer 4: Bottom-right: A circle that changes size over time.
    max_radius = wx_fifth
    radius = int(abs(max_radius * math.sin(win.get_time())))
    win.draw_circle(
        x=cx + wx_fifth,
        y=cy + wx_fifth,
        radius=radius,
        center_color=colors.BLUE20,
        outer_color=colors.RED,
    )

    # Top layer: Hazard triangle that moves with the mouse (cursor).
    mouse_pos = win.get_mouse_pos()
    mx, my = int(mouse_pos.x), int(mouse_pos.y)
    win.draw_image(
        image=hazard_img,
        x=mx - (wx_twentieth / 2),
        y=my,
        width=wx_twentieth,
        height=wy_twentieth,
    )

    # Last: Draw text.
    # FPS counter = 1/(time since last frame).
    cur_time = win.get_time()
    update_frequency_seconds = 0.25
    if int(cur_time) > 0 and (cur_time - last_update_and_fps[0] > update_frequency_seconds):
        dt = cur_time - last_frame_time
        last_update_and_fps[1] = 1 / dt
        last_update_and_fps[0] = cur_time
    fps_text = Text(
        text=f'FPS: {last_update_and_fps[1]:3.0f}',
        font=nova_flat_26,
        color=colors.DARK_GRAY
    )
    win.draw_text(
        text=fps_text,
        x=wx - fps_text.width - gray_box_border,
        y=wy - fps_text.height - gray_box_border
    )
    last_frame_time = cur_time
    # 'Coding Circle' 3 times (centered) on the top half.
    spacing = 10
    start_y = cy - (coding_aller.height + coding_rsb.height + coding_reb.height) - (4 * spacing)
    y = start_y
    win.draw_texts_centered(texts=[coding_aller, circle_aller], y=y)
    y += coding_aller.height + spacing
    win.draw_texts_centered(texts=[coding_rsb, circle_rsb], y=y)
    y += coding_rsb.height + spacing
    win.draw_texts_centered(texts=[coding_reb, circle_reb], y=y)

    # Draw!
    win.update()
win.close()
exit(0)
