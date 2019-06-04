from cc import gl, glfw, logging


class RegisterInputFunctionality:
    """Defines what (mouse, keyboard, etc.) input does to a glfwWindow via callbacks.
    Follows docs: https://www.glfw.org/docs/latest/input_guide.html

    Args:
        glfwWin: An initialized GLFW glfwWindow.
    """

    def __init__(self, glfwWin):
        # Register input callbacks.
        glfw.set_window_size_callback(glfwWin, _on_resize)
        glfw.set_framebuffer_size_callback(glfwWin, _on_framebuffer_resize)
        glfw.set_mouse_button_callback(glfwWin, _on_mouse_button)
        glfw.set_key_callback(glfwWin, _on_key)


def _on_resize(glfwWin, width, height):
    gl.glViewport(0, 0, width, height)
    gl.glLoadIdentity()


def _on_framebuffer_resize(glfwWin, width, height):
    """ Change the GL viewport upon framebuffer resize."""
    fbw, fbh = glfw.get_framebuffer_size(glfwWin)
    gl.glViewport(0, 0, fbw, fbh)
    gl.glLoadIdentity()


def _on_mouse_button(glfwWin, button, action, mods):
    is_down = True if action == glfw.PRESS else False
    msg = 'down' if is_down else 'up'
    x, y = glfw.get_cursor_pos(glfwWin)
    logging.debug('Mouse %s at (%d, %d).' % (msg, x, y))


def _on_key(glfwWin, key, code, action, mods):
    # Quit: ESCAPE, CMD+W (mac)
    if key == glfw.KEY_ESCAPE or \
            (key == glfw.KEY_W and __super_key_pressed(glfwWin)):
        glfw.set_window_should_close(glfwWin, gl.GL_TRUE)


def __super_key_pressed(glfwWin):
    """ True/False if the SUPER key is being pressed (CMD for mac). """
    left_cmd = glfw.get_key(glfwWin, glfw.KEY_LEFT_SUPER)
    right_cmd = glfw.get_key(glfwWin, glfw.KEY_RIGHT_SUPER)
    return glfw.PRESS in [left_cmd, right_cmd]
