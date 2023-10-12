import random

from cc.color import Color
from cc.font import Font
from cc.image import Image
from cc.text import Text
from cc.window import Window
from cc_student.wip.scenario05.skeleton.problem import Marketplace

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def gen_reference_number():
    return (
            random.choice(letters)
            + random.choice(letters)
            + random.choice(letters)
            + '-'
            + random.choice(letters)
            + random.choice(letters)
            + random.choice(letters)
            + random.choice(letters)
    )


def lerp(x, y, t):
    return x + t * (y - x)


def panel(window: Window, x: int, y: int, width: int, height: int, border: int, color_inner: Color, color_outer: Color):
    window.drawRect(x, y, width, height, color_outer)
    window.drawRect(x + border, y + border, width - 2 * border, height - 2 * border, color_inner)


def rect(window, x, y, sx, sy, r, g, b):
    window.drawRect(x, y, sx, sy, r, g, b)


def draw_text(window: Window, font_path: str, txt: str, x, y, font_pt=16, color=(1, 1, 1)):
    color = Color(color[0], color[1], color[2])
    font = Font(font_path, font_pt)
    text = Text(txt, font, color)
    window.draw_text(text, x, y)


def draw_text_centered_on_window(window: Window, font_path: str, txt: str, y, font_pt=16, color=(1, 1, 1)):
    color = Color(color[0], color[1], color[2])
    font = Font(font_path, font_pt)
    text = Text(txt, font, color)
    window.draw_texts_centered(y, [text])


def draw_image(window: Window, image: Image, x: int, y: int, width: int, height: int) -> None:
    window.draw_image(image, x, y, width, height)


class Panel:
    """ Represents a panel in the window. The top-left of the window is (x, y)."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return f'Panel(x={self.x}, y={self.y}, width={self.width}, height={self.height})'

def calculate_window_split(window: Window, veritical_split_percents: list[int]) -> list[Panel]:
    """ Given a window and a list of `n` vertical percents to split into, return a list of `n` tuples representing the
    dimensions of the panel top-left corner of each panel along with the panels' widths and heights.

    For example, if percents = [25, 25, 50] and Window = 1000x2000, then the return value should be:
        [(0, 0, 250, 2000), (250, 0, 250, 2000), (500, 0, 500, 2000)]

    """
    # Validate that the percents sum to 100.
    if sum(veritical_split_percents) != 100:
        raise ValueError('percents must sum to 100')

    window_width, window_height = window.get_size()

    # Convert the percents to a list of widths.
    widths = []
    for percent in veritical_split_percents:
        widths.append(window_width * percent / 100)

    # Convert the widths to a list of (x, y, width) tuples.
    x = 0
    panels = []
    for panel_width in widths:
        panels.append(Panel(x, 0, panel_width, window_height))
        x += panel_width

    return panels


def draw_shipment_panel(window: Window, p: Panel, font_menu_path: str, font_mono_path: str,
                        marketplace: Marketplace):
    """ Draw the shipment panel."""
    border = 8
    panel(window, p.x, p.y, p.width, p.height, border, Color(0.15, 0.15, 0.15), Color(0.2, 0.2, 0.2))
    x = p.x + border + 8
    y = p.y + border
    y += border
    draw_text(window, font_menu_path, '- Shipment Panel -', x, y, 24, (1, 1, 1))
    y += 60
    x += 10
    draw_text(window, font_menu_path, 'SHIPMENTS', x, y, 20)
    y += 24
    x += 8
    for shipment_id in marketplace.shipment_ids:
        draw_text(window, font_mono_path, '>', x, y, 20)
        draw_text(window, font_mono_path, f'shipment {shipment_id}', x + 24, y, 20, (0.5, 1.0, 0.5))
        y += 25


def draw_map_panel(window: Window, p: Panel, mono_font_path: str, market: Marketplace, day: int, us_map_image: Image):
    """ Draw the map panel."""
    border = 8
    panel(window, p.x, p.y, p.width, p.height, border, Color(0.15, 0.15, 0.15), Color(0.2, 0.2, 0.2))
    y = p.y + (2*border)
    draw_text_centered_on_window(window, mono_font_path, f'- Map Panel (Day {day}) -', y, 24, (1, 1, 1))
    y += 30

    # Draw US map, centered with maximal width.
    # TODO: look into https://www.earthdatascience.org/courses/scientists-guide-to-plotting-data-in-python/plot-spatial-data/customize-raster-plots/interactive-maps/
    # or https://automating-gis-processes.github.io/CSC18/lessons/L5/interactive-map-bokeh.html
    image_border = 16
    maximal_image_width = p.width - (2 * border) - (2 * image_border)
    image_scale_factor = round(maximal_image_width / us_map_image.width, 2)
    image_width = us_map_image.width * image_scale_factor
    image_height = us_map_image.height * image_scale_factor
    x = p.x + border + image_border
    # Just determined y by eye.
    y += 120
    print(f"map: x={x}, y={y}, width={image_width}, height={image_height}")
    draw_image(window, us_map_image, x, y, image_width, image_height)


def draw_carrier_panel(window: Window, p: Panel, font_menu_path: str, font_mono_path: str, marketplace: Marketplace):
    """ Draw the carrier panel."""
    border = 8
    panel(window, p.x, p.y, p.width, p.height, border, Color(0.15, 0.15, 0.15), Color(0.2, 0.2, 0.2))
    x = p.x + border + 8
    y = p.y + border
    y += border
    draw_text(window, font_menu_path, '- Carrier Panel -', x, y, 24, (1, 1, 1))
    y += 60
    x += 10
    draw_text(window, font_menu_path, 'CARRIERS', x, y, 20)
    y += 24
    x += 8
    for carrier_id in marketplace.carrier_ids:
        draw_text(window, font_mono_path, '>', x, y, 20)
        draw_text(window, font_mono_path, f'carrier {carrier_id}', x + 24, y, 20, (0.5, 1.0, 0.5))
        y += 25
