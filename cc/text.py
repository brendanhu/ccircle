import PIL.Image as PILImage
from PIL import ImageDraw
from numpy import *

from cc.color import Color
from cc._constant import RGBA
from cc.colors import CLEAR
from cc.font import Font
from cc.image import Image


class Text(Image):
    """ Text <-> image bound to a 2D OpenGL texture; uses PIL's ImageDraw to render text in given font to Image.
        For example usage, see cc_hello.py.
    """

    # noinspection PyMissingConstructor
    def __init__(self, text: str, font: Font, color: Color, background_color: Color = CLEAR):
        """ Render text to a texture; multi-line text not (yet) supported.

        TODO(Brendan):
            keep track of fonts in separate class so we don't have to pass in path here.
            support multi-line text.
        """
        if '\n' in text:
            raise RuntimeError('Drawing multi-line text not supported.')
        self.img = self._render_text(font, text, color, background_color)
        self.id = Image.bind_to_texture(self.img)

    @property
    def height(self):
        """ The height of the rendered text in pixels. """
        return self._height

    @property
    def width(self):
        """ The width of the rendered text in pixels. """
        return self._width

    def _render_text(self, font: Font, text: str, color: Color, background_color: Color) -> PILImage:
        """ Render single-line text to image.

        Arguments:
            font: font
            text: text
            color: text color

        Returns:
            img: the PIL Image object of the rendered text.
        """
        # Create blank RGBA image.
        size_tuple = font.text_size(text)
        init_color_tuple = background_color.to255Tuple()
        img = PILImage.new(RGBA, size_tuple, init_color_tuple)

        # Render text on image.
        draw = ImageDraw.Draw(img)
        color_tuple = color.to255Tuple()
        draw.text((0, 0), text, color_tuple, font=font.ttf_font)

        self._width, self._height = size_tuple
        return img
