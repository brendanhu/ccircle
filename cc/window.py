""" User-facing window class that creates a window to draw on and interact with. """
import math

import glfw
from OpenGL.GL import GL_TRUE, glGenVertexArrays, glBindVertexArray, glBindBuffer, \
    GL_ARRAY_BUFFER, glClearColor, glClear, GL_COLOR_BUFFER_BIT

from cc._color import Color
from cc._constant import LOGGER
from cc._position import Position
from cc._shader import Shader
from cc._shader_source import FRAGMENT_SHADER, VERTEX_SHADER, TEXTURE_FRAGMENT_SHADER
from cc._triangle_vbo import TriangleVbo
from cc._vertex import Vertex
from cc._window_input import RegisterInputFunctionality
from cc.image import Image
from cc.shapes.circle import Circle
from cc.shapes.rectangle import Rectangle
from cc.shapes.triangle import Triangle


class Window:
    """ Window class powered by GLFW.
        Provides intuitive 'wrapper' function calls to circumvent confusing GLFW and GL nuances.

    Notes:
        Written for OpenGL 3.2+ (required for Mac: https://developer.apple.com/opengl/OpenGL-Capabilities-Tables.pdf)
            using examples from http://www.opengl-tutorial.org/.
        Per OpenGL Face Culling norms, vertices for front-facing shapes should be specified in counter-clockwise order.
    """

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

    def update(self):
        """ Draws triangles offered by draw_triangle() on the screen. """
        glBindVertexArray(self._vao_id)
        glClear(GL_COLOR_BUFFER_BIT)

        self._triangle_vbo.draw()
        self._textured_triangle_vbo.draw()

        Window.__clear_gl_array_buffer()
        glfw.swap_buffers(self.win)
        glfw.poll_events()

    def drawTri(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, color):
        """ Draw a triangle with corners (x1, y1), (x2, y2), and (x3, y3) and given color.

        Notes: Here only as a wrapper around __draw_tri() to reuse materials created with CCircle v0.9.8 (Win64).
        """
        v1 = Vertex(self.__pixel_to_position(x1, y1), color)
        v2 = Vertex(self.__pixel_to_position(x2, y2), color)
        v3 = Vertex(self.__pixel_to_position(x3, y3), color)
        tri = Triangle(v1, v2, v3)
        self.__draw_triangle(tri)

    def drawRect(self, x: int, y: int, width: int, height: int, color: Color):
        """ Draw a rectangle starting at (x, y) (the top-left corner) that is width pixels wide and height pixels tall
            with given color.

        Notes: Here only as a wrapper around __draw_rect() to reuse materials created with CCircle v0.9.8 (Win64).
        """
        self.__drawRect(x, y, width, height, color)

    def drawImage(self, image: Image, x: int, y: int, width: int, height: int):
        """ Draw the image window at the point (x, y) and with size width x height pixels.

        TODO(Brendan): The optional angle parameter can be used to draw the image with a rotation of angle degrees
            about its origin.
        """
        self.__drawRect(x, y, width, height, image=image)

    def __drawRect(self, x: int, y: int, width: int, height: int, color: Color = None, image: Image = None):
        """ Draw a rectangle with either a color or texture. """
        if image and color:
            raise RuntimeError('Only color OR texture allowed')
        top_left = self.__pixel_to_position(x, y)
        ndc_width = abs(self.__width_to_ndc(width))
        ndc_height = abs(self.__height_to_ndc(height))
        rect = Rectangle(top_left, ndc_width, ndc_height, color, image)
        self.__draw_rect(rect)

    def drawCircle(self, x: int, y: int, radius: int, center_color: Color, outer_color: Color = None):
        """ Draw a centered at (x, y) with radius radius (in pixels) and given color(s).
            The color of the circle is interpolated from center_color and outer_color, if different.

        Notes:
            The circle's radius is estimated based on the window's width.
            This assumes a 'standard' 4:3 aspect ratio for the window, otherwise the circle looks like an ellipse, oops.
        """
        if not outer_color:
            outer_color = center_color
        center = Vertex(self.__pixel_to_position(x, y), center_color)
        ndc_radius = self.__width_to_ndc(radius)
        circle = Circle(center, outer_color, ndc_radius)
        self.__draw_circle(circle)

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

    def get_mouse_pos(self) -> Position:
        """ Get the position of the mouse (pixels with respect to the top-left corner of the window). """
        mx, my = glfw.get_cursor_pos(self.win)
        return Position(mx, my)

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

    def clear(self, color: Color):
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

    def __gl_setup(self):
        """ GL Setup: VAO -> Shader -> VBO """
        self._vao_id = glGenVertexArrays(1)
        glBindVertexArray(self._vao_id)
        self._shader = Shader(fragment=FRAGMENT_SHADER, vertex=VERTEX_SHADER)
        self._triangle_vbo = TriangleVbo(self._shader)
        self._tex_shader = Shader(fragment=TEXTURE_FRAGMENT_SHADER, vertex=VERTEX_SHADER, is_for_textures=True)
        self._textured_triangle_vbo = TriangleVbo(self._tex_shader)

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

    def __draw_triangle(self, tri: Triangle):
        """ Offers the triangle to vbo and draws upon next update() call.

        Args:
            tri: triangles to draw.
        """
        if tri.image:
            self._textured_triangle_vbo.offer_triangle(tri)
        else:
            self._triangle_vbo.offer_triangle(tri)

    def __draw_rect(self, rect: Rectangle):
        """ Offers the rectangle's triangles to the vbo and draws upon next update() call.

        Args:
            rect: rect to draw.
        """
        if rect.t1.image:
            self._textured_triangle_vbo.offer_triangle(rect.t1)
            self._textured_triangle_vbo.offer_triangle(rect.t2)
        else:
            self._triangle_vbo.offer_triangle(rect.t1)
            self._triangle_vbo.offer_triangle(rect.t2)

    def __draw_circle(self, circle: Circle):
        """ Offers the circle (multiple triangles) to vbo and draws upon next update() call.

        Args:
            circle: the circle to draw.

        Notes:
            This is the old-school OpenGL way to draw a circle. Perhaps conceptually easier?
            Unsure about performance compared to GL_TRIANGLE_STRIP.
        """
        fv = circle.radius / 4.0
        fv = max(fv, 64)
        num_tris = int(fv)

        for i in range(num_tris):
            angle1 = math.tau * (i + 0) / fv
            angle2 = math.tau * (i + 1) / fv
            tri = Triangle(
                Vertex(
                    Position(circle.center.pos.x, circle.center.pos.y),
                    color=circle.center.color
                ),
                Vertex(
                    Position(circle.center.pos.x + circle.radius * math.cos(angle1),
                             circle.center.pos.y + circle.radius * math.sin(angle1)),
                    color=circle.color
                ),
                Vertex(
                    Position(circle.center.pos.x + circle.radius * math.cos(angle2),
                             circle.center.pos.y + circle.radius * math.sin(angle2)),
                    color=circle.color
                ),
            )
            self._triangle_vbo.offer_triangle(tri)

    def __set_active(self):
        glfw.make_context_current(self.win)

    def __validate_window(self):
        if not self.win:
            msg = "Error: GLFW failed to create a window."
            LOGGER.fatal(msg)
            self.close_all_windows()
            raise RuntimeError(msg)
        ctx_major = glfw.get_window_attrib(self.win, glfw.CONTEXT_VERSION_MAJOR)
        forward_compat = glfw.get_window_attrib(self.win, glfw.OPENGL_FORWARD_COMPAT)
        if ctx_major >= 3 and forward_compat:
            LOGGER.debug("Context is forward compatible, no old-school OpenGL (2.x commands) allowed!")
        self.__log_window_statistics()

    def __log_window_statistics(self):
        ctx_major = glfw.get_window_attrib(self.win, glfw.CONTEXT_VERSION_MAJOR)
        ctx_minor = glfw.get_window_attrib(self.win, glfw.CONTEXT_VERSION_MINOR)
        x1, y1 = self.get_top_left_corner()
        width, height = self.get_size()
        x2, y2 = (x1 + width, y1 + height)

        LOGGER.debug("OpenGL %d.%d Window" % (ctx_major, ctx_minor))
        LOGGER.debug('  Position:')
        LOGGER.debug('    Top-left: (%d, %d)' % (x1, y1))
        LOGGER.debug('    Size: (%d, %d)' % (width, height))
        LOGGER.debug('    Bottom right: (%d, %d)' % (x2, y2))
        LOGGER.debug('    frame size: ' + str(self.get_frame_size()))
        LOGGER.debug('    framebuffer size: ' + str(self.get_framebuffer_size()))

    @staticmethod
    def __clear_gl_array_buffer():
        """ Restore memory for GL_ARRAY_BUFFER. """
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def __pixel_to_position(self, x: int, y: int) -> Position:
        """ Convert a pixel (x, y) to NDC coordinates. """
        wx, wy = self.get_size()
        px = 2 * x / wx - 1
        py = 1 - 2 * y / wy
        converted = Position(px, py)
        return converted

    def __width_to_ndc(self, w) -> float:
        """ Fit a pixel width to ndc coords -> [0.0, 2.0]. """
        wx, _ = self.get_size()
        converted_w = w / (wx * 2)
        return converted_w

    def __height_to_ndc(self, h) -> float:
        """ Fit a pixel height to ndc coords -> [0.0, 2.0]. """
        _, wy = self.get_size()
        converted_h = h / (wy * 2)
        return converted_h
