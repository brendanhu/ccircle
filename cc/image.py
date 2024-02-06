from typing import Tuple

import cv2
import numpy as np
from OpenGL.GL import glGetIntegerv, GL_MAX_TEXTURE_SIZE, glGenTextures, glBindTexture, GL_TEXTURE_2D, glTexImage2D, \
    GL_UNSIGNED_BYTE, GL_RGBA, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR, \
    glGenerateMipmap, glTexParameteri, glPixelStorei, GL_UNPACK_ALIGNMENT, \
    GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE, glTexParameterf
from OpenGL.raw.GL.VERSION.GL_2_0 import GL_MAX_TEXTURE_IMAGE_UNITS
from PIL import Image as pilImage
from PIL.Image import FLIP_TOP_BOTTOM
from PIL.Image import Image as PILImage
from numpy import fromstring, uint8, ndarray, float32, array

from cc.constant import LOGGER, RGBA
from cc._util import get_ccircle_image_path


class Image:
    _num_bound_textures = 0

    def __init__(self, texture_id: int, width: int, height: int):
        """ An RGB image bound to a 2D OpenGL texture.
            Should be created from a classmethod builder:
                @from_path or @from_numpy_array
        """
        self.id = texture_id
        self.width = width
        self.height = height

    def __eq__(self, other):
        """ Two textures are equal if they share the same OpenGL-assigned id."""
        return self.id == other.id

    @staticmethod
    def deform(img: PILImage) -> PILImage:
        """Deform this image using OpenCV. Specifically, this method will deform the image such that the
        bottom left corner of the image will be at the bottom_left_deformed coordinate, and the bottom right corner of
        the image will be at the bottom_right_deformed coordinate. This should create the desired genie effect by
        leaving the top of the image (including the width) unchanged, and creating a 'stretch' effect on the other 3
        sides of the rectangle.

        Returns:
            deformed_img: The deformed PIL Image object.
        """
        natural_points: ndarray = array(
            [[480, 48], [480 + 160, 48], [480 + 160, 48 + 342], [480, 48 + 340]],
            dtype=float32
        )
        deformed_points: ndarray = array(
            [[480, 48], [480+160, 48], [570, 455], [550, 455]],
            dtype=float32
        )
        new_width = 40
        new_height = 800

        # Apply the perspective transformation to the base image.
        base_img_point_array = np.array(img)
        M = cv2.getPerspectiveTransform(natural_points, deformed_points)
        warped_img = cv2.warpPerspective(base_img_point_array, M, (new_width, new_height))

        # Convert the numpy array back to a PIL image
        return pilImage.fromarray(warped_img)

    @classmethod
    def bind_from_path(cls, path: str, deform: bool = False):
        """ Create an image given a path relative to the ccircle directory. """
        resolved_path = get_ccircle_image_path(path)
        LOGGER.debug(f'Loading image from path: {resolved_path.name}')
        img = Image.__open_image(resolved_path)
        LOGGER.debug(f'Loaded {img.width}x{img.height} image.')
        if deform:
            img = cls.deform(img)
        LOGGER.debug(f'Binding {"deformed " if deform else ""}{resolved_path.name} image to OpenGL texture.')
        texture_id = Image._bind_to_texture(img)
        return cls(texture_id, img.width, img.height)

    @classmethod
    def from_numpy_array(cls, pixel_array: ndarray):
        """ Create a ccircle image from a numpy array.

        Returns:
            texture_id: the id of the texture loaded into OpenGL.
        """
        pillow_image: PILImage = pilImage.fromarray(pixel_array)
        texture_id = Image._bind_to_texture(pillow_image)
        return cls(texture_id, pillow_image.width, pillow_image.height)

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
    def exists_space_for_texture() -> bool:
        """ Check if there is space for another texture in OpenGL. """
        max_texture_units = glGetIntegerv(GL_MAX_TEXTURE_IMAGE_UNITS)
        num_loaded_textures = Image._num_bound_textures
        return num_loaded_textures < max_texture_units

    @staticmethod
    def _bind_to_texture(img: PILImage, deform_texture_coordinates=None) -> int:
        """ Convert img (BMP, IM, JPEG, PNG, etc.) to an OpenGL texture.

        * Verifies image dimensions and ensures there is space for another texture in OpenGL.
        * WIP(deform_texture_coordinates for genie_minimize); may not be the best way, but just getting it working...

        Args:
            img: a PIL Image object.
            deform_texture_coordinates: Optional function to deform texture coordinates.

        Returns:
            texture_id: the id of the texture loaded into OpenGL.
        """
        # Validate the image size/channels are supported.
        width, height = img.size
        max_dimension = Image.__max_texture_size()
        if width > max_dimension or height > max_dimension:
            raise RuntimeError('Image dimensions must be < %s.' % max_dimension)

        # Validate there is space for another texture in OpenGL.
        if not Image.exists_space_for_texture():
            raise RuntimeError(f"Can't load {img}. Maxed out at {Image.__max_texture_size()} textures.")

        # Deform texture coordinates if a deformation function is provided.
        if deform_texture_coordinates:
            img = deform_texture_coordinates(img)

        # Transpose the image and convert to RGBA.
        img_data = img.transpose(FLIP_TOP_BOTTOM).convert(RGBA)
        # We actually want bytes; unsure why PyTypeChecker is complaining, so disable it for the following statement.
        # noinspection PyTypeChecker
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

        Image._num_bound_textures += 1
        LOGGER.debug(f"{Image._num_bound_textures} texture{'s' if Image._num_bound_textures > 1 else ''} bound.\n")

        return texture_id
