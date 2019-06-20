import PIL.Image as PILImage
from PIL import ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont
from numpy import *

from cc.image import Image


class Font(Image):
    """ A font <-> image bound to a 2D OpenGL texture; uses PIL's ImageDraw to render font to Image. """

    # noinspection PyMissingConstructor
    def __init__(self, font_path, text, color=None, font_size=10):
        """ TODO(Brendan): color """
        font = Font.load_ttf_font(font_path, font_size)
        self.img = self.__to_image(font, text, color, font_size)
        self.id = Image.bind_to_texture(self.img)

    @staticmethod
    def load_ttf_font(font_path, font_size=10) -> FreeTypeFont:
        """ Load TrueType font from file

        Arguments:
            font_path: path to the (*.ttf) font
            font_size: size of characters (in points).

        Returns:
            font (FreeTypeFont): the font.
        """
        return ImageFont.truetype(font_path, font_size)

    def __to_image(self, font: FreeTypeFont, text: str, color, font_size):
        """ Render text to image.

        Arguments:
            font: font
            text: text
            color: text color
            font_size: size of characters (in points).
        Returns:
            img: the PIL Image object of the rendered text
        """
        sz = font.getsize(text)[0], font_size
        img = PILImage.new("RGBA", sz, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text, color, font=font)

        self.width = sz[0]
        self.height = sz[1]
        return img
