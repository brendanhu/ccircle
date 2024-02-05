""" Constants for the ccircle (cc) module. """
import logging

MODULE_NAME = 'ccircle'
VERSION = '0.1'
REQUIREMENTS_FILE = 'requirements.txt'

# Configure logging.
LOGGER_LEVEL = 'DEBUG'
LOGGER = logging.getLogger(MODULE_NAME)
maybe_level = logging.getLevelName(LOGGER_LEVEL)
maybe_level = maybe_level if maybe_level else 'INFO'
LOGGER.setLevel(maybe_level)
logging.basicConfig(level='INFO')

RGBA = 'RGBA'
