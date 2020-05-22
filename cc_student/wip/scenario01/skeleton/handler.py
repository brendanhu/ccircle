from cc.window import Window
from cc_student.wip.scenario01.skeleton.cat import Cat
from cc_student.wip.scenario01.skeleton.constant import Direction, Cell
from cc_student.wip.scenario01.skeleton._world import World
from cc_student.wip.scenario01.solution import Solution


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

    def _get_facing_cell(self):
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
        if elapsed > Solution.get_pause_time() and not self._failure and not self._success:
            self._lastMove = now
            self._moved = False
            self._cb.move_towards_pizza(self.cat)
            cell = self.world.get_cell(self.cat.tx, self.cat.ty)
            if cell in [Cell.Wall, Cell.OutOfBounds]:
                self._failure = True
            if cell == Cell.Goal:
                self._success = True

    def has_pizza(self):
        return self.world.cells[self.cat.tx][self.cat.ty] == '!'

    def is_blocked(self):
        fx, fy = self._get_facing_cell()
        result = self.world.get_cell(fx, fy)
        return result in [Cell.Wall, Cell.OutOfBounds]

    def is_facing_north(self):
        return self.cat.direction == Direction.NORTH

    def is_facing_east(self):
        return self.cat.direction == Direction.EAST

    def is_facing_south(self):
        return self.cat.direction == Direction.SOUTH

    def is_facing_west(self):
        return self.cat.direction == Direction.WEST

    def can_smell_pizza(self):
        fx, fy = self._get_facing_cell()
        result = self.world.get_cell(fx, fy)
        return result == Cell.Goal

    def turn_left(self):
        self.cat.direction = (self.cat.direction + 3) % 4

    def turn_right(self):
        self.cat.direction = (self.cat.direction + 1) % 4

    def walk(self):
        if not self._moved:
            self.cat.tx, self.cat.ty = self._get_facing_cell()
            self.cat.x, self.cat.y = self.cat.tx, self.cat.ty
            self._moved = True
