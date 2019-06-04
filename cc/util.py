""" Utility functions. """
from cc import logging


def clamp(x: float, low: float, high: float):
    """ Clamp x in [low, high]. """
    if x < low:
        return low
    if x > high:
        return high
    return x


def clamp_rgba(x: float):
    """Ensures the float value given is within [0.0, 1.0], logging a warning if clamped. """
    low, high = [0.0, 1.0]
    if x < low or x > high:
        logging.warning('Before calling %s, clamping %s to valid rgba range.' % (name, x))
        return clamp(x)
    return x
