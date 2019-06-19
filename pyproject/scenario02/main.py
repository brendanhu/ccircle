import time

import pyproject.scenario02.problem as problem
import pyproject.scenario02.solution as solution
from cc.colors import DARK_GRAY
from cc.window import Window
from pyproject.scenario02.util import accountPanel, marketPanel

trader = solution.StockTrader()
account, market = problem.create(trader)

window = Window(1600, 900, 'Scenario 2: Beating the Stock Market')
wx, wy = window.get_size()

# TODO(Brendan): after fonts work.
fMenu = cc.Font('../res/NovaFlat.ttf')
fMono = cc.Font('../res/FiraMono.ttf')

day = 1
last = time.time() - trader.getPauseTime()
while window.is_open():
    window.clear(DARK_GRAY)

    accountPanel(window, fMenu, fMono, account, wy, day)
    marketPanel(window, fMenu, market, wx, wy, day)

    now = time.time()
    if (now - last) >= trader.getPauseTime():
        last = now
        trader.trade(account, market)
        market._update()
        day += 1
    window.update()
