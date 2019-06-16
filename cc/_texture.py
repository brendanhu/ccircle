from pathlib import Path

from OpenGL.GL import glGetIntegerv, GL_MAX_TEXTURE_SIZE, glGenTextures, glBindTexture, GL_TEXTURE_2D, glTexImage2D, \
    GL_UNSIGNED_BYTE, GL_RGBA, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, \
    GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR, glGenerateMipmap, glTexParameteri, GL_REPEAT
from PIL import Image
from numpy import array, int8

from cc.constant import LOGGER


class Texture:
    """ Load an image into a 2D texture. """
    def __init__(self, image_path: Path):
        self.id = Texture.__to_texture(image_path)
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
            img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        except IOError as ex:
            LOGGER.critical('Failed to open image file at %s: %s' % (path, str(ex)))
            raise
        LOGGER.debug('%s (size, format) = (%s, %s)' % (path, img.size, img.format))

        # Verify the image size/channels are supported.
        num_channels = len(img.split())
        if num_channels != 4:
            raise RuntimeError('TODO(Brendan) Only 4-channel images supported.')
        width, height = img.size
        max_dimension = Texture.__max_texture_size()
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
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            img_data
        )

        # Trilinear filtering.
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)

        return texture_id
