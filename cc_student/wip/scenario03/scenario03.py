""" Rush hour scenario! """
from cc.window import Window

window = Window()
window.show_cursor()

while window.is_open():
    # TODO(Brendan): Turn the image into a RushHour board.
    image_path = 'cc_student/scenario03/assets/worlds/world2.png',

    # Draw.
    window.update()

window.close()
exit(0)
