""" Utility functions. """
from cc import np
from cc.ds.point import NDCPoint
from cc.ds.triangle import Triangle


def clamp(x: float, low: float, high: float, fail_on_error: bool = False):
    """ Clamp x in [low, high].

    Args:
        x: the value to clamp.
        low: the lowest allowable value.
        high: the highest allowable value.
        fail_on_error: If true, throws a RuntimeException instead of clamping an out-of-range value.
    """
    if x < low:
        if fail_on_error:
            raise RuntimeError('Value %.4f not within allowable range [%.4f, %.4f]' % (x, low, high))
        return low
    if x > high:
        return high
    return x


def clamp_ndc(x: float, fail_on_error: bool = False):
    """Ensures the float value given is within [-1.0, 1.0]. """
    return clamp(x, -1.0, 1.0, fail_on_error)


def clamp_rgba(x: float, fail_on_error: bool = False):
    """Ensures the float value given is within [0.0, 1.0]. """
    return clamp(x, 0.0, 1.0, fail_on_error)


def validate_point_for_render(p: NDCPoint):
    """ Validates that an NDCPoint is valid:
        - 3-axes of vert within [-1.0, 1.0]
        - color rgba within [0.0, 1.0]
    """
    map(lambda a: clamp_ndc(a, True), [p.x, p.y, p.z])
    map(lambda a: clamp_rgba(a, True), [p.color.r, p.color.g, p.color.b])


def validate_tri(tri: Triangle):
    """ Validates that a triangle is valid:
        - verts within [-1.0, 1.0]
        - colors within [0.0, 1.0]
    """
    if not tri:
        raise RuntimeError("Empty triangles not allowed.")
    map(lambda p: validate_point_for_render(p), [tri.p1, tri.p2, tri.p3])


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
