import glfw

from cc._constant import LOGGER


class RegisterInputFunctionality:
    """Defines what (mouse, keyboard, etc.) input does to a glfwWindow via callbacks.
    Follows docs: https://www.glfw.org/docs/latest/input_guide.html

    Args:
        glfwWin: An initialized GLFW glfwWindow.
    """

    def __init__(self, glfwWin):
        # Register input callbacks.
        glfw.set_mouse_button_callback(glfwWin, _on_mouse_button)
        glfw.set_key_callback(glfwWin, _on_key)


def _on_mouse_button(glfwWin, button, action, mods):
    is_down = True if action == glfw.PRESS else False
    msg = 'down' if is_down else 'up'
    x, y = glfw.get_cursor_pos(glfwWin)
    LOGGER.debug('Mouse %s at (%d, %d).' % (msg, x, y))


def _on_key(glfwWin, key, code, action, mods):
    # Quit: ESCAPE, CMD+W (mac)
    if key == glfw.KEY_ESCAPE or \
            (key == glfw.KEY_W and __super_key_pressed(glfwWin)):
        glfw.set_window_should_close(glfwWin, glfw.TRUE)


def __super_key_pressed(glfwWin):
    """ True/False if the SUPER key is being pressed (CMD for mac). """
    left_cmd = glfw.get_key(glfwWin, glfw.KEY_LEFT_SUPER)
    right_cmd = glfw.get_key(glfwWin, glfw.KEY_RIGHT_SUPER)
    return glfw.PRESS in [left_cmd, right_cmd]
