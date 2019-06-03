""" Imports (python module dependencies) for the ccircle (cc) module. """
import glfw
if not glfw.init():
    raise RuntimeError('Could not initialize GLFW')
import OpenGL.GL as gl

import logging
import math

# This defines all imports available to the cc module.
__all__ = [
    'glfw',
    'gl',
    'logging',
    'math',
]

# Set logger level from the constants file, defaulting to INFO.
from cc.constant import *
maybe_level = logging.getLevelName(LOGGER_LEVEL)
maybe_level = maybe_level if maybe_level else 'INFO'
logging.basicConfig(level=maybe_level)