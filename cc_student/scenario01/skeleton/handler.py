from cc.window import Window
from cc_student.scenario01.skeleton.cat import Cat
from cc_student.scenario01.skeleton.constant import Direction, Cell
from cc_student.scenario01.skeleton._world import World
from cc_student.scenario01.solution import Solution


class Handler:
    def __init__(self, window: Window):
        self.window = window
        self.world = World()
        self.cat = self.world.find(Cat.NAME)
        self._success = False
        self._failure = False
        self._moved = False
        self._lastMove = self.window.get_time()
        self._cb = Solution()

    def update(self):
        self._update()
        self.world.draw(self.window)
        wx, wy = self.window.get_size()
        if self._success:
            self.window.drawRect(0, 0, wx, wy, 0, 1, 0, 0.5)
        elif self._failure:
            self.window.drawRect(0, 0, wx, wy, 1, 0, 0, 0.5)

    def _getFacingCell(self):
        if Direction.NORTH == self.cat.direction:
            return self.cat.tx, self.cat.ty - 1
        if Direction.EAST == self.cat.direction:
            return self.cat.tx + 1, self.cat.ty
        if Direction.SOUTH == self.cat.direction:
            return self.cat.tx, self.cat.ty + 1
        if Direction.WEST == self.cat.direction:
            return self.cat.tx - 1, self.cat.ty
        return self.cat.tx, self.cat.ty

    def _update(self):
        now = self.window.get_time()
        elapsed = now - self._lastMove
        if elapsed > Solution.getPauseTime() and not self._failure and not self._success:
            self._lastMove = now
            self._moved = False
            self._cb.moveTowardPizza(self.cat)
            cell = self.world.getCell(self.cat.tx, self.cat.ty)
            if cell in [Cell.Wall, Cell.OutOfBounds]:
                self._failure = True
            if cell == Cell.Goal:
                self._success = True

    def hasPizza(self):
        return self.world.cells[self.cat.tx][self.cat.ty] == '!'

    def isBlocked(self):
        fx, fy = self._getFacingCell()
        result = self.world.getCell(fx, fy)
        return result in [Cell.Wall, Cell.OutOfBounds]

    def isFacingN(self):
        return self.cat.direction == Direction.NORTH

    def isFacingE(self):
        return self.cat.direction == Direction.EAST

    def isFacingS(self):
        return self.cat.direction == Direction.SOUTH

    def isFacingW(self):
        return self.cat.direction == Direction.WEST

    def smellsPizza(self):
        fx, fy = self._getFacingCell()
        result = self.world.getCell(fx, fy)
        return result == Cell.Goal

    def turnLeft(self):
        self.cat.direction = (self.cat.direction + 3) % 4

    def turnRight(self):
        self.cat.direction = (self.cat.direction + 1) % 4

    def walk(self):
        if not self._moved:
            self.cat.tx, self.cat.ty = self._getFacingCell()
            self.cat.x, self.cat.y = self.cat.tx, self.cat.ty
            self._moved = True
