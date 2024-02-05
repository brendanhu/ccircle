""" Let's create the Genie effect minimization animation. """
import math

import cc.colors as colors
from cc.color import Color
from cc.constant import LOGGER
from cc.font import Font
from cc.image import Image
from cc.text import Text
from cc.window import Window

# Create window.
win = Window()
win.hide_cursor()

# Load any images, fonts, or static text just once.
LOGGER.debug("\n\nLoading images...")
bliss_img = Image.from_path('cc_student/assets/images/bliss.jpeg')
start_button_img = Image.from_path('cc_student/assets/images/windows_xp_desktop_start_button.png')
rainbow_img = Image.from_path('cc_student/assets/images/rainbow.png')
LOGGER.debug("\n\nLoading fonts...")
nova_flat_13 = Font('cc_student/assets/fonts/NovaFlat.ttf', 13)


class GenieWindow:
    """ The window to Genie minimize. At a given point in animation it has a top-left corner (x, y), width and height.

    Once the window is fully minimized (i.e. in 'goal' state), it 'transforms' into a widget on the taskbar.
    """

    def __init__(self, minimized_title_text: Text, initial_x: int, initial_y: int, initial_width: int, initial_height: int):
        """ Create the non-minimized window. """
        self._minimized_title_text = minimized_title_text
        self.x = initial_x
        self.y = initial_y
        self.width = initial_width
        self.height = initial_height
        # Set non-nonsensical goal.
        self._goal_x: int = -1
        self._goal_y: int = -1
        self._goal_width: int = -1
        self._goal_height: int = -1
        self._goal_color: Color = colors.WHITE

    def move(self, x: int, y: int, width: int, height: int):
        """ Move the window to be at the given place and size. """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def set_minimized_goal(self, x: int, y: int, width: int, height: int, goal_color: Color):
        """ Sets the 'goal' condition of minimization, where the window turns into a widget on the start bar. """
        self._goal_x = x
        self._goal_y = y
        self._goal_width = width
        self._goal_height = height
        self._goal_color = goal_color

    def move_to_final_minimized_state(self, ):
        """ Sets the window to be minimized. """
        self.x = self._goal_x
        self.y = self._goal_y
        self.width = self._goal_width
        self.height = self._goal_height

    def is_minimized(self) -> bool:
        """ Returns True if the window is in the minimized state. """
        return self.x == self._goal_x and self.y == self._goal_y and self.width == self._goal_width and self.height == self._goal_height

    def draw(self, win: Window):
        if self.is_minimized():
            # Draw the minimized window THEN the title on top.
            win.drawRect(
                x=mw._goal_x,
                y=mw._goal_y,
                width=mw._goal_width,
                height=mw._goal_height,
                color=mw._goal_color
            )
            win.draw_text(
                text=self._minimized_title_text,
                x=mw._goal_x,
                y=mw._goal_y,
            )
        else:
            # Mid-minimization animation.
            win.draw_image(
                image=rainbow_img,
                x=mw.x,
                y=mw.y,
                width=mw.width,
                height=mw.height,
            )


def to_parametric_cubic(t, start: int, start_tangent: int, end: int, end_tangent: int) -> int:
    """
    Define the cubic parametric function to animate not_minimized_window_details -> minimized_window_details.
    To animate an "S" curve, we'll use a cubic parametric function that, given time t, returns a point (x, y) on the
    curve. Assuming time is normalized to [0, 1], the curve starts at the first point, x0, when t is 0 and ends at the
    second point, x2, when t is 1.
    The curve is defined by four control points:
        - x0: the start point,
        - x1: the start tangent (the direction and speed at which the curve leaves the start point)
        - x2: the end point,
        - x3: the end tangent (the direction and speed at which the curve arrives at the end point)

    Thus, the S curve is defined by the following parametric function:
    x(t) = (1 - t)^3 * x0 + 3 * (1 - t)^2 * t * x1 + 3 * (1 - t) * t^2 * x2 + t^3 * x3
    y(t) = (1 - t)^3 * y0 + 3 * (1 - t)^2 * t * y1 + 3 * (1 - t) * t^2 * y2 + t^3 * y3
    where (x0, y0) is the start point, (x1, y1) is the start tangent, (x2, y2) is the end tangent, and (x3, y3) is
    the end point.
    """
    return int(
        (1 - t) ** 3 * start
        + 3 * (1 - t) ** 2 * t * start_tangent
        + 3 * (1 - t) * t ** 2 * end
        + t ** 3 * end_tangent
    )


# Define the Genie window prior to animation.
wx, wy = win.get_size()
genie_window_start_width = wy // 3
genie_window_start_x = wx - genie_window_start_width
genie_window_start_y = wy // 10
genie_window_start_height = wy // 1.4
mw = GenieWindow(
    minimized_title_text=Text('Smol', font=nova_flat_13, color=colors.BLUE20),
    initial_x=genie_window_start_x,
    initial_y=genie_window_start_y,
    initial_width=genie_window_start_width,
    initial_height=genie_window_start_height
)
taskbar_height = wy // 20
start_button_width = wx // 8


def genie_attempt_1_simple_parametric_interpolation() -> (int, int, int, int):
    """ Attempt 1: Minimize the window using simple (parametric) linear interpolation.
    Looks pretty good with animation of 0.15 seconds. """
    # Determine X with simple parametric interpolation.
    x_para: float = genie_window_start_x + (genie_window_end_x - genie_window_start_x) * t_normalized
    # Determine Y with simple parametric interpolation.
    y_para: float = genie_window_start_y + (genie_window_end_y - genie_window_start_y) * t_normalized
    # Squeeze the width parametrically as it approaches the minimized state.
    width_para: float = genie_window_start_width - (genie_window_start_width - genie_window_end_width) * t_normalized
    # Determine the height by ensuring it never touches the taskbar.
    height_para: float = genie_window_start_height - (
                genie_window_start_height - genie_window_end_height) * t_normalized
    return x_para, y_para, width_para, height_para


def genie_attempt_2_bezier() -> (int, int, int, int):
    """ Attempt 2: """
    """ Attempt 2: Use cubic Bezier curves for animation."""
    # Determine X with cubic Bezier interpolation.
    x_bezier: int = to_parametric_cubic(
        t_normalized,
        genie_window_start_x,
        genie_window_start_x + (genie_window_end_x - genie_window_start_x) // 3,
        genie_window_end_x - (genie_window_end_x - genie_window_start_x) // 3,
        genie_window_end_x
    )
    # Determine Y with cubic Bezier interpolation.
    y_bezier: int = to_parametric_cubic(
        t_normalized,
        genie_window_start_y,
        genie_window_start_y,
        genie_window_end_y,
        genie_window_end_y
    )
    # Squeeze the width with cubic Bezier interpolation.
    width_bezier: int = to_parametric_cubic(
        t_normalized,
        genie_window_start_width,
        genie_window_start_width,
        genie_window_end_width,
        genie_window_end_width
    )
    # Determine the height by ensuring it never touches the taskbar.
    height_bezier: int = to_parametric_cubic(
        t_normalized,
        genie_window_start_height,
        genie_window_start_height,
        genie_window_end_height,
        genie_window_end_height
    )
    return x_bezier, y_bezier, width_bezier, height_bezier


def draw_static_assets():
    global start_button_width
    # Create default windows XP background with a task bar at the bottom; guessing at 1/20th of the screen height.
    # Load background image 'Bliss' on top.
    win.draw_image(
        image=bliss_img,
        x=0,
        y=0,
        width=wx,
        height=wy,
    )
    # Draw the task bar on bottom.
    win.drawRect(
        x=0,
        y=wy - taskbar_height,
        width=wx,
        height=taskbar_height,
        color=colors.CC_DARK_BLUE,
    )
    # Load 'Start' button image on leftmost part of taskbar.
    win.draw_image(
        image=start_button_img,
        x=0,
        y=wy - taskbar_height,
        width=start_button_width,
        height=taskbar_height,
    )


while win.is_open():
    win.clear(colors.WHITE)

    draw_static_assets()

    # Perform Genie Effect animation.
    genie_window_end_x = start_button_width
    genie_window_end_y = wy - taskbar_height
    genie_window_end_width = start_button_width // 2
    genie_window_end_height = taskbar_height
    mw.set_minimized_goal(
        genie_window_end_x,
        genie_window_end_y,
        genie_window_end_width,
        genie_window_end_height,
        goal_color=colors.CC_LIGHT_BLUE,
    )

    animation_duration = 0.5
    animation_start_time = 1.0
    t_normalized = (win.get_time() - animation_start_time) / animation_duration
    if t_normalized > 1.0:
        # Ensure the window is minimized.
        if not mw.is_minimized():
            mw.move_to_final_minimized_state()
    elif win.get_time() >= animation_start_time:
        # The window is minimizing - apply genie effect!
        x, y, width, height = genie_attempt_2_bezier()

        # Move the window to the new position.
        mw.move(int(x), int(y), int(width), int(height))
        LOGGER.info(f"  Genie window min-minimization. Moving to: x={mw.x}, y={mw.y}, width={mw.width}, height={mw.height}")

        # TODO Next Attempt: After looking at te real genie effect, I noticed that I can't mimic the horizontal squish
        # by rendering a simple rectangle. Instead, will need to squish using a (non-linear) transformation on texture
        # coordinates.

    # Draw the window.
    mw.draw(win)

    # Draw!
    win.update()
win.close()
exit(0)
