""" Constants for the ccircle (cc) module. """
MODULE_NAME = 'cc'

# Configure Logging.
import logging

LOGGER_LEVEL = 'INFO'
LOGGER = logging.getLogger(MODULE_NAME)
maybe_level = logging.getLevelName(LOGGER_LEVEL)
maybe_level = maybe_level if maybe_level else 'INFO'
LOGGER.setLevel(maybe_level)
logging.basicConfig(level='INFO')

RGBA = 'RGBA'
