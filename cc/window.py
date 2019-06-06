import cc.util as util

from cc import *
from cc.ds.point import NDCPoint, GLPoint
from cc.ds.triangle import Triangle
from cc.constant import *
from cc.shader import Shader
from cc.util import validate_tri
from cc.window_input import RegisterInputFunctionality


class Window:
    point_buffer = []
    tri_buffer = []

    """ Window class powered by GLFW.
        Provides intuitive 'wrapper' function calls to circumvent confusing GLFW and GL nuances.

    Notes:
        Written for OpenGL 3.2+ (required for Mac: https://developer.apple.com/opengl/OpenGL-Capabilities-Tables.pdf)
            using examples from http://www.opengl-tutorial.org/.
        Per OpenGL Face Culling norms, vertices for front-facing shapes should be specified in counter-clockwise order.
    """

    def __init__(self, width: int = 640, height: int = 480, win_title: str = "CC Window", fullscreen: bool = False):
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
        self.vao_id = gl.glGenVertexArrays(1)

        gl.glBindVertexArray(self.vao_id)
        self.shader = Shader(fragment=FRAGMENT_SHADER, vertex=VERTEX_SHADER)
        self.position_attr_idx = self.shader.attribute_index(VertexAttribute.POSITION_IN)
        self.colors_attr_idx = self.shader.attribute_index(VertexAttribute.COLOR_IN)
        gl.glEnableVertexAttribArray(self.position_attr_idx)
        gl.glEnableVertexAttribArray(self.colors_attr_idx)
        gl.glBindVertexArray(0)

        self.verts_vbo_id, self.colors_vbo_id = gl.glGenBuffers(2)

        gl.glEnable(gl.GL_PROGRAM_POINT_SIZE)

    @staticmethod
    def __set_glfw_hints():
        """ Set GLFW hints for OpenGL 3.2+, etc.; hints like COCOA_RETINA_FRAMEBUFFER are ignored off of OSX. """
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
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

        Notes:
            Empties tri_buffer ASAP.
            Though inferior in performance to a single interleaved VBO, conceptually easier to grasp.
            For further explanation of what is happening here, see http://antongerdelan.net/opengl/vertexbuffers.html
        """
        if not self.tri_buffer:
            return 0
        verts = util.extract_vertices_as_single_vbo_ready_array(*self.tri_buffer)
        colors = util.extract_colors_as_single_vbo_ready_array(*self.tri_buffer)
        num_triangles = len(self.tri_buffer)
        self.tri_buffer = []

        gl.glBindVertexArray(self.vao_id)
        # VBO1: verts in shader's POSITION_IN VertexAttribute
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.verts_vbo_id)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, arrays.ArrayDatatype.arrayByteCount(verts), verts, gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(self.position_attr_idx, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
        # VBO2: colors in shader's COLOR_IN VertexAttribute
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.colors_vbo_id)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, arrays.ArrayDatatype.arrayByteCount(colors), colors, gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(self.colors_attr_idx, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

        return num_triangles

    def update(self):
        """ Draws triangles offered by draw_triangle() on the screen. """
        num_triangles = self.__prepare_triangles()

        # Draw
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        if num_triangles:
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3 * num_triangles)

        Window.clear_gl_array_buffer()
        glfw.swap_buffers(self.win)
        glfw.poll_events()

    def draw_point(self, p: GLPoint):
        """ Places the point in the point_buffer to draw upon next update() call.

        Args:
            p: the point to draw.
        """
        util.validate_point_for_render(p)
        self.point_buffer.append(p)

    def draw_triangle(self, tri: Triangle):
        """ Validates triangle and draws upon next update() call.

        Args:
            tri: triangles to draw.
        """
        validate_tri(tri)
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

    def clear(self, color: Color):
        """ Clears the window with a certain color. """
        self.__set_active()
        gl.glClearColor(*color.to_list())

    def close(self):
        """ Closes the window. """
        glfw.destroy_window(self.win)

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

        Notes:
            Uses vertex buffers per OpenGL 3.2+.
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
        # gl.glDisableVertexAttribArray(0)
        gl.glBindVertexArray(0)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
