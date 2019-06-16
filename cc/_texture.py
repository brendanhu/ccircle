from pathlib import Path

from OpenGL.GL import glGetIntegerv, GL_MAX_TEXTURE_SIZE, GL_MAX_GEOMETRY_TEXTURE_IMAGE_UNITS, glGenTextures, \
    glBindTexture, GL_TEXTURE_2D, glTexImage2D, GL_UNSIGNED_BYTE, GL_RGBA, \
    GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, \
    GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR, glGenerateMipmap, glTexParameteri, GL_REPEAT, glPixelStorei, GL_UNPACK_ALIGNMENT
from PIL import Image
from numpy import array, int8

from cc.constant import LOGGER


class Texture:
    """ Load an image into a 2D texture. The file_path is relative to the ccircle directory."""
    def __init__(self, image_path: Path):
        self.id = Texture.__to_texture(image_path)
        pass

    @staticmethod
    def __max_texture_size():
        """ Get the max texture size (n x n) that this GPU supports. """
        n = glGetIntegerv(GL_MAX_TEXTURE_SIZE)
        return n

    @staticmethod
    def __max_geom_shader_texture_units():
        """ Get the max texture image units that this GPU supports. """
        return glGetIntegerv(GL_MAX_GEOMETRY_TEXTURE_IMAGE_UNITS)

    @staticmethod
    def __to_texture(path: Path):
        """ Convert img to OpenGL texture with trilinear filtering.

        Args:
            path: a pathlib.Path object--the path to the image.

        Returns:
            texture_id: the id of the texture loaded into OpenGL.

        Notes:
            PIL can open BMP, EPS, FIG, IM, JPEG, MSP, PCX, PNG, PPM, etc.
        """
        try:
            img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        except IOError as ex:
            LOGGER.critical('Failed to open image file at %s: %s' % (path, str(ex)))
            raise
        LOGGER.debug('%s (size, format) = (%s, %s)' % (path, img.size, img.format))
        num_channels = len(img.split())
        if num_channels != 4:
            raise RuntimeError('TODO(Brendan) Only 4-channel images supported.')

        img_data = array(list(img.getdata()), int8)
        width, height = img.size

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
        img.close()

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)

        return texture_id
