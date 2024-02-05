import cc_student.wip.scenario05.skeleton.problem as problem
import cc_student.wip.scenario05.player_code as solution
from cc.colors import DARK_GRAY
from cc.image import Image
from cc.window import Window
from cc_student.wip.scenario05.skeleton.util import draw_shipment_panel, draw_map_panel, calculate_window_split, \
    draw_carrier_panel

player_code = solution.PlayerCode()
marketplace = problem.create_marketplace()
window = Window(win_title='Scenario 5: Freight Marketplace Optimization')
window.toggle_maximized()
window_width, window_height = window.get_size()

font_menu_path = 'cc_student/assets/fonts/NovaFlat.ttf'
font_mono_path = 'cc_student/assets/fonts/FiraMono.ttf'

# Load the USA map image once.
# TODO - pivot to https://www.amazon.com/Educational-Playroom-Nursery-Bedroom-Classroom/dp/B07HQGK19C
us_map_image = Image.from_path('cc_student/wip/scenario05/assets/images/us_map_2.png')

day = 1
last = window.get_time() - player_code.pause_time
while window.is_open():
    # Set background color.
    window.clear(DARK_GRAY)

    # Draw the various panels, designating what percentage of the horizontal space they should fill.
    p1, p2, p3 = calculate_window_split(window, [15, 70, 15])
    draw_shipment_panel(window, p1, font_menu_path, font_mono_path, marketplace)
    draw_map_panel(window, p2, font_menu_path, marketplace, day, us_map_image)
    draw_carrier_panel(window, p3, font_menu_path, font_mono_path, marketplace)

    # Run the player's optimize() algorithm.
    now = window.get_time()
    if (now - last) >= player_code.pause_time:
        last = now
        player_code.optimize(marketplace)
        marketplace.update()
        day += 1

    # Update the window, drawing the new state of the world.
    window.update()
window.close()
exit(0)
