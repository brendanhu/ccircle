from cc._color import Color
from cc.font import Font
from cc.text import Text
from cc.window import Window


def lerp(x, y, t):
    return x + t * (y - x)


def panel(window, x, y, sx, sy, b, cInner, cOuter):
    window.drawRect(x, y, sx, sy, *cOuter)
    window.drawRect(x + b, y + b, sx - 2 * b, sy - 2 * b, *cInner)


def rect(window, x, y, sx, sy, r, g, b):
    window.drawRect(x, y, sx, sy, r, g, b)


def draw_text(window: Window, font_path: str, txt: str, x, y, font_pt=16, color=(1, 1, 1)):
    color = Color(color[0], color[1], color[2])
    font = Font(font_path, font_pt)
    text = Text(txt, font, color)
    window.drawText(text, x, y)


def accountPanel(window: Window, fMenu_path: str, fMono_path: str, account, wy, day):
    panel(window, 0, 0, 400, wy, 8, (0.15, 0.15, 0.15), (0.2, 0.2, 0.2))
    draw_text(window, fMenu_path, '- Account Info -', 64, 20, 30, (1, 1, 1))
    y = 80
    draw_text(window, fMenu_path, 'BALANCE', 32, y, 20)
    y += 25
    draw_text(window, fMono_path, '>', 64, y, 20)
    draw_text(window, fMono_path, '$%.2f' % account.getBalance(), 90, y, 20, (0.5, 1.0, 0.5))
    y += 25
    draw_text(window, fMono_path, '>', 64, y, 20)
    draw_text(window, fMono_path, '$%.2f PPD' % ((account.getBalance() - 1000) / day), 90, y, 20, (0.5, 1.0, 0.5))
    y += 25

    y += 15
    draw_text(window, fMenu_path, 'STOCKS', 32, y, 20)
    y += 25
    for sym, value in account._shares.items():
        draw_text(window, fMono_path, '>', 64, y, 20)
        draw_text(window, fMono_path, '%s : %d shares' % (sym, value), 90, y, 20, (0.5, 1.0, 0.5))
        y += 25
    y += 15

    draw_text(window, fMenu_path, 'LOG', 32, y, 20)
    y += 30

    for line in reversed(account._log):
        c = (0.9, 0.9, 0.9)
        if 'BUY' in line:
            c = (0.9, 0.5, 0.5)
        elif 'SELL' in line:
            c = (0.5, 0.9, 0.5)
        draw_text(window, fMono_path, line, 64, y, 12, c)
        y += 16
        if y > (wy - 16):
            break


def marketPanel(window, fMono, market, wx, wy, day):
    panel(window, 416, 0, wx - 416, wy, 8, (0.15, 0.15, 0.15), (0.2, 0.2, 0.2))
    draw_text(window, fMono, 'Market (Day: %d)' % day, 870, 20, 30, (1, 1, 1))

    spacing = 8
    h = (wy - 64 - (16 - spacing)) / len(market._stocks)
    h -= spacing
    y = 64
    for sym, stock in market._stocks.items():
        panel(window, 432, y, 96, h, 2, (0.2, 0.2, 0.2), (0.10, 0.10, 0.10))
        panel(window, 540, y, wx - 540 - 16, h, 2, (0.2, 0.2, 0.2), (0.1, 0.1, 0.1))
        draw_text(window, fMono, sym, 450, int(y) + 8, 32)
        draw_text(window, fMono, '$%.2f' % stock.price, 442, int(y) + 54, 20)

        if len(stock.history) > 1:
            wsz = 128
            history = stock.history
            if len(history) > wsz:
                history = history[-wsz:]
            x = 548
            w = (wx - 548 - 16) / wsz
            vMin = min(history)
            vMax = max(history)
            for val in history:
                if vMin == vMax:
                    vn = 0.5
                else:
                    vn = (val - vMin) / (vMax - vMin)
                r = lerp(1.0, 0.1, vn)
                g = lerp(0.0, 0.4, vn)
                b = lerp(0.4, 1.0, vn)
                rect(window, x, y + 4 + (h - 8) * (1.0 - vn), 8, (h - 8) * vn, r, g, b)
                x += w

        y += h + spacing
