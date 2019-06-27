""" Quick-and-dirty logo generator using ccircle.
 TODO(Brendan): do this the right way using glReadPixels. (rn it's screenshot based).
"""
from enum import Enum

import cc.colors as colors
from cc.font import Font
from cc.text import Text
from cc.window import Window

# Maximize window.
win = Window()
win.toggle_maximized()


class BisectRetVal(Enum):
    LOWER, HIGHER, STOP = range(3)


def binary_search_text_size(text, comparator, lo: int = 0, high: int = 300):
    if lo < 0 or high < lo:
        raise ValueError('lo must be non-negative')
    while lo < high:
        mid = (lo + high) // 2
        if comparator(text, mid) == BisectRetVal.STOP:
            return mid
        elif comparator(text, mid) == BisectRetVal.HIGHER:
            lo = mid + 1
        else:
            high = mid
    return lo


def font_size_comparator(font_path):
    max_x, max_y = win.get_size()

    def parametrized_bisect_left_comparator(text, font_size):
        font = Font(font_path, font_size)
        x, y = font.text_size(text)
        if x < max_x:
            return BisectRetVal.HIGHER
        else:
            return BisectRetVal.LOWER

    return parametrized_bisect_left_comparator


def getLargestFont(font_path, text) -> Font:
    """ For given text, determine the largest font size that will fit the text on the current window. """
    max_font_size = binary_search_text_size(text, font_size_comparator(font_path))
    return Font(font_path, max_font_size)


# LOGO specifics.
LOGO_TEXT = 'MITHRID'
LOGO_BACKGROUND_COLOR = colors.WHITE
LOGO_COLOR = colors.CC_LIGHT_BLUE

# Load fonts and text just once.
aller_Lt_max = getLargestFont('cc_student/assets/fonts/Aller_Lt.ttf', LOGO_TEXT)
ralewayExtraBold_max = getLargestFont('cc_student/assets/fonts/Raleway-ExtraBold.ttf', LOGO_TEXT)
ralewaySemiBold_max = getLargestFont('cc_student/assets/fonts/Raleway-SemiBold.ttf', LOGO_TEXT)
mithrid_aller = Text(text=LOGO_TEXT, font=aller_Lt_max, color=LOGO_COLOR)
mithrid_reb = Text(text=LOGO_TEXT, font=ralewayExtraBold_max, color=LOGO_COLOR)
mithrid_rsb = Text(text=LOGO_TEXT, font=ralewaySemiBold_max, color=LOGO_COLOR)

while win.is_open():
    win.clear(LOGO_BACKGROUND_COLOR)

    # Misc window info.
    wx, wy = win.get_size()
    cx, cy = wx / 2, wy / 2

    # Draw logos.
    # text_heights + (4 * spacing) = wy
    spacing = (wy - (mithrid_aller.height + mithrid_reb.height + mithrid_rsb.height)) // 4
    y = spacing
    win.drawTextsCentered(texts=[mithrid_aller], y=y)
    y += mithrid_aller.height + spacing
    win.drawTextsCentered(texts=[mithrid_rsb], y=y)
    y += mithrid_rsb.height + spacing
    win.drawTextsCentered(texts=[mithrid_reb], y=y)

    win.update()
win.close()
