from OpenGL.GL import glGetIntegerv, GL_MAX_TEXTURE_SIZE, glGenTextures, glBindTexture, GL_TEXTURE_2D, glTexImage2D, \
    GL_UNSIGNED_BYTE, GL_RGBA, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR, \
    glGenerateMipmap, glTexParameteri, glPixelStorei, GL_UNPACK_ALIGNMENT, \
    GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE, glTexParameterf
from PIL import Image as pilImage
from PIL.Image import FLIP_TOP_BOTTOM
from PIL.Image import Image as PILImage
from numpy import fromstring, uint8

from cc._constant import LOGGER, RGBA
from cc._util import get_ccircle_image_path


class Image:
    """ An image bound to a 2D OpenGL texture. """

    def __init__(self, path: str):
        """ Create an image given a path relative to the ccircle directory. """
        resolved_path = get_ccircle_image_path(path)
        img = Image.__open_image(resolved_path)
        LOGGER.debug('Loading image: %s' % resolved_path.name)
        self.id = Image.bind_to_texture(img)
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
    def __open_image(path) -> PILImage:
        """ Lazily open the file given by the path as a PIL Image."""
        try:
            return pilImage.open(path)
        except IOError as ex:
            LOGGER.critical('Failed to open image file at %s: %s' % (path, str(ex)))
            raise

    @staticmethod
    def bind_to_texture(img: PILImage):
        """ Convert img (BMP, IM, JPEG, PNG, etc.) to an OpenGL texture.

        Args:
            img: a PIL Image object.

        Returns:
            texture_id: the id of the texture loaded into OpenGL.

        Notes:
            Verifies image dimensions and (TODO(Brendan)) ensures there is space for another texture in OpenGL.
        """
        # Verify the image size/channels are supported.
        width, height = img.size
        max_dimension = Image.__max_texture_size()
        if width > max_dimension or height > max_dimension:
            raise RuntimeError('Image dimensions must be < %s.' % max_dimension)

        # Transpose the image and convert to RGBA.
        img_data = img.transpose(FLIP_TOP_BOTTOM).convert(RGBA)
        img_data = fromstring(img_data.tobytes(), uint8)

        # Bind the image data to an OpenGL texture.
        texture_id = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
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

        # Stretch texture; mipmaps for minification; clamp.
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glGenerateMipmap(GL_TEXTURE_2D)

        img.close()

        return texture_id
