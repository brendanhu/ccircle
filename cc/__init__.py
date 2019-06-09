""" CCircle (cc) module init. """
import logging

from cc.constant import LOGGER_LEVEL

# Set logger level from the constants file, defaulting to INFO.
maybe_level = logging.getLevelName(LOGGER_LEVEL)
maybe_level = maybe_level if maybe_level else 'INFO'
logging.basicConfig(level=maybe_level)
