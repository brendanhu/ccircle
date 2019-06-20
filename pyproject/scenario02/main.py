import pyproject.scenario02.problem as problem
import pyproject.scenario02.solution as solution
from cc.colors import DARK_GRAY
from cc.window import Window
from pyproject.scenario02.util import accountPanel, marketPanel

trader = solution.StockTrader()
account, market = problem.create(trader)

window = Window(1600, 900, 'Scenario 2: Beating the Stock Market')
window.toggle_maximized()
window.hide_cursor()
wx, wy = window.get_size()

fMenu_path = 'pyproject/res/NovaFlat.ttf'
fMono_path = 'pyproject/res/FiraMono.ttf'

day = 1
last = window.get_time() - trader.getPauseTime()
while window.is_open():
    window.clear(DARK_GRAY)

    accountPanel(window, fMenu_path, fMono_path, account, wy, day)
    marketPanel(window, fMenu_path, market, wx, wy, day)

    now = window.get_time()
    if (now - last) >= trader.getPauseTime():
        last = now
        trader.trade(account, market)
        market._update()
        day += 1
    window.update()
