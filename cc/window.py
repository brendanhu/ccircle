from cc import *
from cc.window_input import RegisterInputFunctionality


class Window:
    """ Window class powered by GLFW.
        Provides intuitive 'wrapper' function calls to circumvent confusing GLFW and GL nuances.

    Args:
        width (int, optional): Width in pixels of the GLFW window.
        height (int, optional): Height in pixels of the GLFW window.
        win_title (str, optional): The title of the window.
        fullscreen (bool, optional): if the window should be fullscreen.

    Notes:
        OpenGL 3.2+ required for Mac: https://developer.apple.com/opengl/OpenGL-Capabilities-Tables.pdf
        Per OpenGL Face Culling norms, vertices are specified in clockwise order.
    """

    def __init__(self, width=640, height=480, win_title="CC Window", fullscreen=False):
        """ Create window, set context and register input callbacks. """
        # GLFW hints for OpenGL Context, etc.
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.DEPTH_BITS, 24)
        glfw.window_hint(glfw.STENCIL_BITS, 8)
        glfw.window_hint(glfw.FOCUSED, True)
        if glfw.raw_mouse_motion_supported():
            glfw.set_input_mode(self.win, glfw.RAW_MOUSE_MOTION, glfw.TRUE)
        # Ignored off of osx.
        glfw.window_hint(glfw.COCOA_RETINA_FRAMEBUFFER, glfw.TRUE)

        # Create window.
        monitor = glfw.get_primary_monitor() if fullscreen else None
        self.win = glfw.create_window(width=width, height=height, title=win_title, monitor=monitor, share=None)
        self.__validate_window()

        # OpenGL hints.
        gl.glEnable(gl.GL_POINT_SMOOTH)
        gl.glEnable(gl.GL_LINE_SMOOTH)
        gl.glHint(gl.GL_POINT_SMOOTH_HINT, gl.GL_NICEST)
        gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
        gl.glPointSize(2.0)
        gl.glLineWidth(1.0)

        # Set swap interval for vsync, input callbacks, and set active.
        self.__set_active()
        glfw.swap_interval(1)
        RegisterInputFunctionality(self.win)

    def isOpen(self):
        """ Returns whether or not this window is open.

        Returns:
            True if open, False otherwise.
        """
        return not glfw.window_should_close(self.win)

    def get_top_left_corner(self):
        """ Gets the coordinates of the top left corner of the window.

        Returns:
            (top_left_x, top_left_y): The top left corner (x, y) tuple.
        """
        return tuple(glfw.get_window_pos(self.win))

    def get_size(self):
        """ Gets the size of the window.

        Returns:
            (width, height): A tuple of the (width, height) of the window.

        Notes:
            This is in screen coordinates and NOT pixels.
        """
        return tuple(glfw.get_window_size(self.win))

    def get_frame_size(self):
        """ Gets the size of the frame of the window.

        Returns:
            (a, b, c, d): The window's frame
        """
        return tuple(glfw.get_window_frame_size(self.win))

    def get_framebuffer_size(self):
        """ Gets the size of the framebuffer of the window.

        Returns:
            (width, height): A tuple of the (width, height) of the framebuffer.
        """
        return tuple(glfw.get_framebuffer_size(self.win))

    def get_mouse_pos(self):
        """ The coordinates of the mouse position with respect to the top-left corner of the window.

        Returns:
            (x, y): A tuple of the mouse position.
        """
        return tuple(glfw.get_cursor_pos(self.win))

    def clear(self, r, g, b):
        """ Clears the window with a certain color. """
        self.__set_active()
        gl.glClearColor(r, g, b, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    def close(self):
        """ Closes the window. """
        glfw.destroy_window(self.win)

    @staticmethod
    def getTime():
        """ Returns whether or not this window is open.

        Returns:
            time (double): the number of seconds this window has been open as a float.
        """
        return glfw.get_time()

    def draw_point(self, x, y, s=2.0, r=1.0, g=1.0, b=1.0, a=1.0):
        """ Draws a line from (x1, y1) to (x2, y2).

        Args:
            x (int): The x-coord of the point.
            y (int): The y-coord of the point.
            s (float): The size of the point.
            r (float, optional): The 'red' component of the circle's color.
            g (float, optional): The 'green' component of the circle's color.
            b (float, optional): The 'blue' component of the circle's color.
            a (float, optional): The alpha (transparency) component of the circle.
        """
        self.__set_active()
        gl.glPointSize(s)
        gl.glColor4f(r, g, b, a)
        gl.glBegin(gl.GL_POINTS)
        gl.glVertex2f(x, y)
        gl.glEnd()

    def draw_line(self, x1, y1, x2, y2, thickness=2.0, r=1.0, g=1.0, b=1.0, a=1.0):
        """ Draws a line from (x1, y1) to (x2, y2) that is thickness pixels thick with color (r, g, b, a).

        Args:
            x1 (int): The x-coord of the first point defining line segment.
            y1 (int): The y-coord of the first point defining line segment.
            x2 (int): The x-coord of the second point defining line segment.
            y2 (int): The y-coord of the second point defining line segment.
            thickness (int, optional): The line's thickness in pixels.
            r (float, optional): The 'red' component of the circle's color.
            g (float, optional): The 'green' component of the circle's color.
            b (float, optional): The 'blue' component of the circle's color.
            a (float, optional): The alpha (transparency) component of the circle.
        """
        self.__set_active()
        gl.glColor4f(r, g, b, a)
        gl.glLineWidth(thickness)
        gl.glBegin(gl.GL_LINES)
        gl.glVertex2f(x1, y1)
        gl.glVertex2f(x2, y2)
        gl.glEnd()

    def draw_rect(self, x1, y1, width, height, r=1.0, g=1.0, b=1.0, a=1.0):
        """ Draws a rectangle with top-left (x1, y1) and bottom-right (x2, y2) with color (r, g, b, a).

        Args:
            x1 (int): The x-coord of the top-left point of the rectangle.
            y1 (int): The y-coord of the top-left point of the rectangle.
            width (int): The width of the rectangle.
            height (int): The height of the rectangle.
            r (float, optional): The 'red' component of the circle's color.
            g (float, optional): The 'green' component of the circle's color.
            b (float, optional): The 'blue' component of the circle's color.
            a (float, optional): The alpha (transparency) component of the circle.
        """
        self.__set_active()
        gl.glColor4f(r, g, b, a)
        gl.glBegin(gl.GL_QUADS)
        gl.glVertex2f(x1, y1)
        gl.glVertex2f(x1 + width, y1)
        gl.glVertex2f(x1 + width, y1 + height)
        gl.glVertex2f(x1, y1 + height)
        gl.glEnd()

    def draw_tri(self, x1, y1, x2, y2, x3, y3, r=1.0, g=1.0, b=1.0, a=1.0):
        """ Draws a triangle with clockwise-specified coordinates (x1, y1), (x2, y2), (x3, y3) with color (r, g, b, a).

        Args:
            x1 (int): The x-coord of the first point (P1) of the triangle.
            y1 (int): The y-coord of the first point (P1) of the triangle.
            x2 (int): The x-coord of the point immediately clockwise of P1 of the triangle.
            y2 (int): The y-coord of the point immediately clockwise of P1 of the triangle.
            x3 (int): The x-coord of the point immediately clockwise of P2 of the triangle.
            y3 (int): The y-coord of the point immediately clockwise of P2 of the triangle.
            r (float, optional): The 'red' component of the circle's color.
            g (float, optional): The 'green' component of the circle's color.
            b (float, optional): The 'blue' component of the circle's color.
            a (float, optional): The alpha (transparency) component of the circle.
        """
        self.__set_active()
        gl.glColor4f(r, g, b, a)
        gl.glBegin(gl.GL_TRIANGLES)
        gl.glVertex2f(x1, y1)
        gl.glVertex2f(x2, y2)
        gl.glVertex2f(x3, y3)
        gl.glEnd()

    def draw_circle(self, x, y, radius, r=1.0, g=1.0, b=1.0, a=1.0):
        """ Draws a circle centered at (x, y) with color (r, g, b, a).

        Args:
            x (int): The x-coord of the center of the circle.
            y (int): The y-coord of the center of the circle.
            radius (int): The radius of the circle (in pixels).
            r (float, optional): The 'red' component of the circle's color.
            g (float, optional): The 'green' component of the circle's color.
            b (float, optional): The 'blue' component of the circle's color.
            a (float, optional): The alpha (transparency) component of the circle.
        """
        self.__set_active()
        fv = radius / 4.0
        fv = max(fv, 64)
        num_tris = int(fv)

        gl.glBegin(gl.GL_POLYGON)
        gl.glColor4f(r, g, b, a)
        for i in range(num_tris):
            angle1 = math.tau * (i + 0) / fv
            angle2 = math.tau * (i + 1) / fv
            gl.glVertex2f(x, y)
            gl.glVertex2f(x + radius * math.cos(angle1), y + radius * math.sin(angle1))
            gl.glVertex2f(x + radius * math.cos(angle2), y + radius * math.sin(angle2))
        gl.glEnd()

    def hide_cursor(self):
        glfw.set_input_mode(self.win, glfw.CURSOR, glfw.CURSOR_HIDDEN)

    def show_cursor(self):
        glfw.set_input_mode(self.win, glfw.CURSOR, glfw.CURSOR_NORMAL)

    def toggle_maximized(self):
        glfw.maximize_window(self.win)

    @staticmethod
    def close_all_windows():
        glfw.terminate()

    def __set_active(self):
        glfw.make_context_current(self.win)
        self.__set_viewport()

    def __set_viewport(self):
        """ TODO(Brendan): Rewrite this to be OpenGL 3.2 forward compatible. """
        (fbw, fbh) = self.get_framebuffer_size()
        gl.glViewport(0, 0, fbw, fbh)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glTranslated(-1.0, 1.0, 0.0)
        gl.glScaled(2.0 / fbw, -2.0 / fbh, 1.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    def __validate_window(self):
        if not self.win:
            msg = "Error: GLFW failed to create a window."
            logging.fatal(msg)
            self.close_all_windows()
            raise RuntimeError(msg)
        ctx_major = glfw.get_window_attrib(self.win, glfw.CONTEXT_VERSION_MAJOR)
        forward_compat = glfw.get_window_attrib(self.win, glfw.OPENGL_FORWARD_COMPAT)
        if ctx_major >= 3 and forward_compat:
            logging.warning("Context is forward compatible, you can't use OpenGL 2.x commands.")
        self.log_window_statistics()

    def log_window_statistics(self):
        ctx_major = glfw.get_window_attrib(self.win, glfw.CONTEXT_VERSION_MAJOR)
        ctx_minor = glfw.get_window_attrib(self.win, glfw.CONTEXT_VERSION_MINOR)
        x1, y1 = self.get_top_left_corner()
        width, height = self.get_size()
        x2, y2 = (x1 + width, y1 + height)

        logging.debug("OpenGL %d.%d Window" % (ctx_major, ctx_minor))
        logging.debug('  Top-left: (%d, %d)' % (x1, y1))
        logging.debug('  Size: (%d, %d)' % (width, height))
        logging.debug('  Bottom right: (%d, %d)' % (x2, y2))
        logging.debug('  frame size: ' + str(self.get_frame_size()))
        logging.debug('  framebuffer size: ' + str(self.get_framebuffer_size()))

    def update(self):
        glfw.swap_buffers(self.win)
        glfw.poll_events()
        gl.glClearColor(0, 0, 0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
