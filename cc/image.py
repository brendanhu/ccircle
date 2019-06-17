from pathlib import Path

from OpenGL.GL import glGetIntegerv, GL_MAX_TEXTURE_SIZE, glGenTextures, glBindTexture, GL_TEXTURE_2D, glTexImage2D, \
    GL_UNSIGNED_BYTE, GL_RGBA, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR, \
    glGenerateMipmap, glTexParameteri, GL_RGBA8, GL_RGB, GL_RED
from PIL import Image as pilImage
from numpy import array, int8

from cc._constant import LOGGER
from cc._util import get_ccircle_image_path


class Image:
    """ Load an image into a 2D OpenGL texture using PIL. """

    def __init__(self, path: str):
        """ Create an image given a path relative to the ccircle directory. """
        resolved_path = get_ccircle_image_path(path)
        self.id = Image.__to_texture(resolved_path)
        pass

    def __eq__(self, other):
        """ Two textures are equal if they share the same OpenGL-assigned id."""
        return self.id == other.id

    @staticmethod
    def __max_texture_size():
        """ Get the max texture size (n x n) that this GPU supports. """
        n = glGetIntegerv(GL_MAX_TEXTURE_SIZE)
        return n

    @staticmethod
    def __to_texture(path: Path):
        """ Convert img (BMP, IM, JPEG, PNG, etc.) to an OpenGL texture (with trilinear filtering).

        Args:
            path: a pathlib.Path object--the path to the image.

        Returns:
            texture_id: the id of the texture loaded into OpenGL.

        Notes:
            Verifies image dimensions and ensures there is space for another texture in OpenGL.
        """
        try:
            img = pilImage.open(path).transpose(pilImage.FLIP_TOP_BOTTOM)
        except IOError as ex:
            LOGGER.critical('Failed to open image file at %s: %s' % (path, str(ex)))
            raise
        LOGGER.debug('%s (size, format) = (%s, %s)' % (path, img.size, img.format))

        # Verify the image size/channels are supported.
        num_channels = len(img.split())
        if num_channels == 2:
            raise RuntimeError('2 channel images not supported.')
        width, height = img.size
        max_dimension = Image.__max_texture_size()
        if width > max_dimension or height > max_dimension:
            raise RuntimeError('Image dimensions must be < %s.' % max_dimension)

        # Extract image rgb.
        img_data = array(list(img.getdata()), int8)
        img.close()

        # Bind the image data to an OpenGL texture.
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA8,
            width,
            height,
            0,
            (
                GL_RGBA if num_channels == 4 else
                GL_RGB if num_channels == 3 else
                GL_RED
            ),
            GL_UNSIGNED_BYTE,
            img_data
        )

        # Trilinear filtering.
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)

        return texture_id
