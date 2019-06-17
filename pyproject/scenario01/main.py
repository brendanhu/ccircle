from cc.window import Window
from pyproject.scenario01 import cat
from pyproject.scenario01 import solution

solver = solution.Solution()
window = Window(win_title="Scenario 1: Space Cat Pizza Party!", fullscreen=True)
world = cat.World(layout=solver.getLevel())
handler = cat.Handler(world, solver)

while window.is_open():
    handler._update()
    handler._draw(window)
    window.update()
