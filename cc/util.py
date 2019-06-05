""" Utility functions. """
from cc import logging, np, sys
from cc.ds.triangle import Triangle


# def nonempty_list_param(func):
#     """ Decorator verifying that a list parameter is non-empty. """
#     def temp(*args, **kwargs):
#         if not args:
#             logging.fatal('Function %s expected a non-empty list parameter.' % func.__name__)
#             sys.exit(1)
#         func(*args, **kwargs)
#
#     return temp

def clamp(x: float, low: float, high: float):
    """ Clamp x in [low, high]. """
    if x < low:
        return low
    if x > high:
        return high
    return x


def clamp_rgba(x: float):
    """Ensures the float value given is within [0.0, 1.0], logging a warning if clamped. """
    low, high = 0.0, 1.0
    if x < low or x > high:
        logging.warning('Clamping %s to valid rgba range.' % x)
        return clamp(x, low, high)
    return x


def vertices_as_array(tri: Triangle):
    """ Convert a triangle's vertex data to a numpy array of single-precision floats.

    Args:
        tri: The triangle.

    Returns:
        vertices (ndarray): the triangle's vertices as a numpy array of single-precision floats:
            [p1x, p1y, p1z, p2x, p2y, p2z, p3x, p3y, p3z]

    Notes:
        This is mostly useful due to the way we've chosen to store each vertex attribute in a separate VBO.
            For more information, see :func:cc.window.prepare_triangles
    """
    return np.array([tri.p1.x, tri.p1.y, tri.p1.z,
                     tri.p2.x, tri.p2.y, tri.p2.z,
                     tri.p3.x, tri.p3.y, tri.p3.z], dtype=np.float32)


def extract_vertices_as_single_vbo_ready_array(*tris: Triangle):
    verts_uncollapsed = list(map(lambda tri: vertices_as_array(tri), tris))
    return np.concatenate(verts_uncollapsed)


def colors_as_array(tri: Triangle):
    """ Convert a triangle's color data to a numpy array of single-precision floats.

    Returns:
        vertices (ndarray): the triangle's vertices as a numpy array of single-precision floats:
            [p1r, p1g, p1b, p2r, p2g, p2b, p3r, p3g, p3b]

    Notes:
        This is mostly useful due to the way we've chosen to store each vertex attribute in a separate VBO.
            For more information, see :func:cc.window.prepare_triangles
    """
    return np.array([tri.p1.color.r, tri.p1.color.g, tri.p1.color.b,
                     tri.p2.color.r, tri.p2.color.g, tri.p2.color.b,
                     tri.p3.color.r, tri.p3.color.g, tri.p3.color.b], dtype=np.float32)


def extract_colors_as_single_vbo_ready_array(*tris: Triangle):
    colors_uncollapsed = list(map(lambda tri: colors_as_array(tri), tris))
    return np.concatenate(colors_uncollapsed)
