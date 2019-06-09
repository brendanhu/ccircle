import ctypes
import math

import glfw
import numpy as np
from OpenGL.GL import GL_TRUE, glGenVertexArrays, glBindVertexArray, glEnableVertexAttribArray, glGenBuffers, \
    glEnable, GL_PROGRAM_POINT_SIZE, glBindBuffer, GL_ARRAY_BUFFER, glBufferData, glVertexAttribPointer, GL_FLOAT, \
    GL_FALSE, GL_STATIC_DRAW, glClear, GL_COLOR_BUFFER_BIT, glDrawArrays, GL_TRIANGLES, \
    glClearColor, GL_ELEMENT_ARRAY_BUFFER, glDrawElements
from OpenGL.arrays import ArrayDatatype, vbo
from OpenGL.raw.GL.ARB.vertex_buffer_object import GL_STREAM_DRAW_ARB

import cc.util as util
from cc import *
from cc import color
from cc._constant import *
from cc._shader import Shader
from cc.point import NDCPoint
from cc.shapes.circle import Circle
from cc.shapes.triangle import Triangle
from cc.util import validate_tri
from cc.window_input import RegisterInputFunctionality


class Window:
    """ Window class powered by GLFW.
        Provides intuitive 'wrapper' function calls to circumvent confusing GLFW and GL nuances.

    Notes:
        Written for OpenGL 3.2+ (required for Mac: https://developer.apple.com/opengl/OpenGL-Capabilities-Tables.pdf)
            using examples from http://www.opengl-tutorial.org/.
        Per OpenGL Face Culling norms, vertices for front-facing shapes should be specified in counter-clockwise order.
    """
    tri_buffer = []

    def __init__(self, width: int = 1280, height: int = 960, win_title: str = "CC Window", fullscreen: bool = False):
        """ Create window, set context and register input callbacks.

        Args:
            width (optional): Width in pixels of the GLFW window.
            height (optional): Height in pixels of the GLFW window.
            win_title (optional): The title of the window.
            fullscreen (optional): if the window should be fullscreen.
        """
        self.__glfw_setup(fullscreen, height, width, win_title)
        self.__gl_setup()

    def __glfw_setup(self, fullscreen, height, width, win_title):
        """ Create window, attach to this instance, make active, register input callbacks.

        Notes:
            Initializes self.win
        """
        if not glfw.init():
            raise RuntimeError('Could not initialize GLFW')
        self.__set_glfw_hints()
        monitor = glfw.get_primary_monitor() if fullscreen else None
        self.win = glfw.create_window(width=width, height=height, title=win_title, monitor=monitor, share=None)
        self.__validate_window()
        self.__set_active()
        RegisterInputFunctionality(self.win)

    def __gl_setup(self):
        """ GL Setup: VAO -> Vertex Attribute Locations via Shader's Linker; VBOs

        Notes:
            Initializes self.vao_id
            Initializes self.shader
            Initializes self.position_attr_idx
            Initializes self.self.colors_attr_idx
            Initializes self.verts_vbo_id
            Initializes self.colors_vbo_id
        """
        self.vao_id = glGenVertexArrays(1)

        glBindVertexArray(self.vao_id)
        self.shader = Shader(fragment=FRAGMENT_SHADER, vertex=VERTEX_SHADER)
        self.position_attr_idx = self.shader.attribute_index(VertexAttribute.POSITION_IN)
        self.colors_attr_idx = self.shader.attribute_index(VertexAttribute.COLOR_IN)
        glEnableVertexAttribArray(self.position_attr_idx)
        glEnableVertexAttribArray(self.colors_attr_idx)
        glBindVertexArray(0)

        self.verts_vbo_id = glGenBuffers(1)

        glEnable(GL_PROGRAM_POINT_SIZE)

    @staticmethod
    def __set_glfw_hints():
        """ Set GLFW hints for OpenGL 3.2+, etc.; hints like COCOA_RETINA_FRAMEBUFFER are ignored off of OSX. """
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.SAMPLES, 4)
        glfw.window_hint(glfw.DEPTH_BITS, 24)
        glfw.window_hint(glfw.STENCIL_BITS, 8)
        glfw.window_hint(glfw.FOCUSED, True)
        glfw.window_hint(glfw.COCOA_RETINA_FRAMEBUFFER, glfw.TRUE)

    def __prepare_triangles(self) -> int:
        """ Prepares triangles from tri_buffer in order, placing their data in vbos and specifying format.

        Returns:
            num_triangles: the number of triangles prepared.
        """
        # data_array <- tri_buffer
        if not self.tri_buffer:
            return 0
        num_triangles = len(self.tri_buffer)
        data_array = np.concatenate([util.as_interleaved_data_array(tri) for tri in self.tri_buffer])
        self.tri_buffer = []

        # VBO <- data
        glBindVertexArray(self.vao_id)
        glBindBuffer(GL_ARRAY_BUFFER, self.verts_vbo_id)
        glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(data_array), data_array, GL_STATIC_DRAW)
        # TODO(Brendan): magic stride -_-
        glVertexAttribPointer(self.position_attr_idx, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glVertexAttribPointer(self.colors_attr_idx, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

        return num_triangles

    def update(self):
        """ Draws triangles offered by draw_triangle() on the screen. """
        num_triangles = self.__prepare_triangles()

        # Draw
        glClear(GL_COLOR_BUFFER_BIT)
        if num_triangles:
            glDrawArrays(GL_TRIANGLES, 0, 3 * num_triangles)

        Window.clear_gl_array_buffer()
        glfw.swap_buffers(self.win)
        glfw.poll_events()

    def draw_triangle(self, tri: Triangle):
        """ Validates triangle and draws upon next update() call.

        Args:
            tri: triangles to draw.
        """
        validate_tri(tri)
        self.tri_buffer.append(tri)

    def draw_circle(self, circle: Circle):
        """ Validates circle (TODO(Brendan)) and draws upon next update() call.

        Args:
            circle: the circle to draw.

        Notes:
            This is the old-school OpenGL--less efficien--way to draw a circle. Perhaps conceptually easier?
                XXX(Brendan): use indexed drawing / GL_TRIANGLE_FAN.
        """
        fv = circle.radius / 4.0
        fv = max(fv, 64)
        num_tris = int(fv)

        for i in range(num_tris):
            angle1 = math.tau * (i + 0) / fv
            angle2 = math.tau * (i + 1) / fv
            tri = Triangle(
                NDCPoint(
                    circle.center.x,
                    circle.center.y,
                    color=circle.center.color
                ),
                NDCPoint(
                    circle.center.x + circle.radius * math.cos(angle1),
                    circle.center.y + circle.radius * math.sin(angle1),
                    color=circle.color
                ),
                NDCPoint(
                    circle.center.x + circle.radius * math.cos(angle2),
                    circle.center.y + circle.radius * math.sin(angle2),
                    color=circle.color
                ),
            )
            self.tri_buffer.append(tri)

    def is_open(self) -> bool:
        """ Returns whether or not this window is open. """
        return not glfw.window_should_close(self.win)

    def get_top_left_corner(self) -> tuple:
        """ Gets the coordinates of the top left corner of the window.

        Returns:
            (top_left_x, top_left_y): The top left corner (x, y) tuple.
        """
        return tuple(glfw.get_window_pos(self.win))

    def get_size(self) -> tuple:
        """ Gets the width x height (in pixels) of the window.

        Returns:
            (width, height): A tuple of the (width, height) of the window.

        Notes:
            This is in screen coordinates and NOT pixels.
        """
        return tuple(glfw.get_window_size(self.win))

    def get_frame_size(self) -> tuple:
        """ Gets the size of the frame of the window.

        Returns:
            (a, b, c, d): The window's frame
        """
        return tuple(glfw.get_window_frame_size(self.win))

    def get_framebuffer_size(self) -> tuple:
        """ Gets the size of the framebuffer of the window.

        Returns:
            (width, height): A tuple of the (width, height) of the framebuffer.
        """
        return tuple(glfw.get_framebuffer_size(self.win))

    def get_mouse_pos(self) -> NDCPoint:
        """ Compute the NDC Point of the mouse position.
            Automatically translates the glfw.get_cursor_pos() results
                (pixels with respect to the top-left corner of the window) into NDC.

        Returns:
            mouse_point (NDCPoint): (px, py, 0)--the current mouse position.

        Notes:
            Note the z is always 0... for now. This will change once projection matrix is added.
        """
        mx, my = glfw.get_cursor_pos(self.win)
        wx, wy = self.get_size()
        px = 2 * mx / wx - 1
        py = 1 - 2 * my / wy

        mouse_point = NDCPoint(px, py)
        return mouse_point

    def clear(self, color: color):
        """ Clears the window with a certain color. """
        self.__set_active()
        glClearColor(color.r, color.b, color.g, color.a)

    def close(self):
        """ Closes the window. """
        glfw.destroy_window(self.win)

    def hide_cursor(self):
        glfw.set_input_mode(self.win, glfw.CURSOR, glfw.CURSOR_HIDDEN)

    def show_cursor(self):
        glfw.set_input_mode(self.win, glfw.CURSOR, glfw.CURSOR_NORMAL)

    def toggle_maximized(self):
        glfw.maximize_window(self.win)

    def __set_active(self):
        glfw.make_context_current(self.win)

    def __validate_window(self):
        if not self.win:
            msg = "Error: GLFW failed to create a window."
            logging.fatal(msg)
            self.close_all_windows()
            raise RuntimeError(msg)
        ctx_major = glfw.get_window_attrib(self.win, glfw.CONTEXT_VERSION_MAJOR)
        forward_compat = glfw.get_window_attrib(self.win, glfw.OPENGL_FORWARD_COMPAT)
        if ctx_major >= 3 and forward_compat:
            logging.warning("Context is forward compatible, no old-school OpenGL (2.x commands) allowed!")
        self.log_window_statistics()

    def log_window_statistics(self):
        ctx_major = glfw.get_window_attrib(self.win, glfw.CONTEXT_VERSION_MAJOR)
        ctx_minor = glfw.get_window_attrib(self.win, glfw.CONTEXT_VERSION_MINOR)
        x1, y1 = self.get_top_left_corner()
        width, height = self.get_size()
        x2, y2 = (x1 + width, y1 + height)

        logging.debug("OpenGL %d.%d Window" % (ctx_major, ctx_minor))
        logging.debug('  Position:')
        logging.debug('    Top-left: (%d, %d)' % (x1, y1))
        logging.debug('    Size: (%d, %d)' % (width, height))
        logging.debug('    Bottom right: (%d, %d)' % (x2, y2))
        logging.debug('    frame size: ' + str(self.get_frame_size()))
        logging.debug('    framebuffer size: ' + str(self.get_framebuffer_size()))

    @staticmethod
    def close_all_windows():
        glfw.terminate()

    @staticmethod
    def get_time() -> float:
        """ Get # of ms the window has the open.

        Returns:
            time (float): the number of seconds this window has been open as a float.
        """
        return glfw.get_time()

    @staticmethod
    def clear_gl_array_buffer():
        """ Restore memory for GL_ARRAY_BUFFER. """
        # glDisableVertexAttribArray(0)
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
