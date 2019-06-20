from pathlib import Path

from PIL import ImageFont
from PIL.ImageFont import FreeTypeFont

from cc._util import get_ccircle_image_path


class Font:
    """ A font that must be instantiated with a size.

    Notes:
        To save some work, keeps a cache of (font_path, pt) to instantiated fonts. Absolutely not best practice :)
    """
    font_cache = dict()

    def __init__(self, font_path: str, pt: int):
        """
        Params:
            font_path: the path to the font, relative to the ccircle directory.
            pt: the size of the font in points.
        """
        self.pt = pt
        self.ttf_font = self._get_or_load_font(font_path, pt)

    def text_size(self, text):
        """ Return the width and height, in pixels, of the text if it were to be drawn with this font."""
        return self.ttf_font.getsize(text)

    def _get_or_load_font(self, font_path: str, pt: int):
        """ Load the font from path ttf_font, checking the font_cache first. """
        resolved_path = get_ccircle_image_path(font_path)
        resolved_path_str = str(resolved_path)
        cache_key = (resolved_path_str, pt)
        font = self.font_cache.get(cache_key)
        if not font:
            new_font = Font._load_ttf_font(resolved_path, pt)
            self.font_cache[cache_key] = new_font
            font = new_font
        return font

    @staticmethod
    def _load_ttf_font(resolved_path: Path, pt) -> FreeTypeFont:
        """ Load TrueType font--of a given size--from path relative to ccircle.

        Arguments:
            font_path: resolved path to the (*.ttf) font
            pt: size of characters (in points).

        Returns:
            font (FreeTypeFont): the font.
        """
        return ImageFont.truetype(str(resolved_path), pt)
