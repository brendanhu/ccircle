""" Constants for the ccircle (cc) module. """
import logging

MODULE_NAME = 'cc'
LOGGER_LEVEL = 'INFO'

# Configure Logging.
LOGGER = logging.getLogger(MODULE_NAME)
maybe_level = logging.getLevelName(LOGGER_LEVEL)
maybe_level = maybe_level if maybe_level else 'INFO'
LOGGER.setLevel(maybe_level)
logging.basicConfig(level='INFO')
