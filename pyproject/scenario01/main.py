""" The main file to be run to display graphics. """
from cc.window import Window
from pyproject.scenario01 import cat
from pyproject.scenario01.solution import Solution

solver = Solution()
window = Window(win_title="Scenario 1: Space Cat Pizza Party!")
world = cat.World(layout=Solution.getLevel())
handler = cat.Handler(world, solver)

while window.is_open():
    handler._update()
    handler._draw(window)
    window.update()
