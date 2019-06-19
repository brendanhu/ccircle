""" The main file to be run to display the scenario. """
from cc.window import Window
from pyproject.scenario01.skeleton.handler import Handler

window = Window(win_title="Scenario 1: Space Cat Pizza Party!")
window.toggle_maximized()
window.hide_cursor()

handler = Handler(window)

while window.is_open():
    handler.update()
    window.update()
