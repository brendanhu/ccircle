from cc.image import Image
from cc.window import Window
from pyproject.scenario01.skeleton.cat import Cat
from pyproject.scenario01.skeleton.constant import Cell
from pyproject.scenario01.skeleton.constant import Layout
from pyproject.scenario01.solution import Solution


class World:
    def __init__(self):
        self.imageBG = Image('pyproject/scenario01/image/space.png')
        self.imageGoal = Image('pyproject/scenario01/image/pizza.png')

        self.load(Solution.getLevel())

    def __clear(self, size):
        """ Clear the world to be size x size empty cells. """
        self.size = size
        self.cells = [[Cell.Empty] * size for _ in range(size)]
        self.objects = []

    def addObject(self, obj):
        """ Add a new free-standing object to the world. """
        self.objects.append(obj)

    def draw(self, window: Window):
        """ Draw the world to a window. """
        size = window.get_size()
        ms = min(size) - 64
        ox = (size[0] - ms) / 2
        oy = (size[1] - ms) / 2
        b = 4
        cs = (ms - 2 * b) / self.size

        # Background
        window.drawImage(self.imageBG, 0, 0, size[0], size[1])

        # Floor: centered square of side length ms
        window.drawRect(ox, oy, ms, ms, 0.2, 0.2, 0.2)

        # Floor grid
        for i in range(1, self.size):
            px = ox + b + cs * i
            py = oy + b + cs * i
            window.drawRect(px, oy, 1, ms, 0.3, 0.3, 0.3)
            window.drawRect(ox, py, ms, 1, 0.3, 0.3, 0.3)

        # Border
        window.drawRect(ox, oy, ms, b, 1, 1, 1)
        window.drawRect(ox, oy, b, ms, 1, 1, 1)
        window.drawRect(size[0] - ox - b, oy, b, ms, 1, 1, 1)
        window.drawRect(ox, size[1] - oy - b, ms, b, 1, 1, 1)

        # Grid Objects
        for y in range(self.size):
            py = oy + b + y * cs
            for x in range(self.size):
                px = ox + b + x * cs
                cell = self.cells[x][y]
                if cell == Cell.Wall:
                    window.drawRect(px, py, cs, cs, 1.0, 0.0, 0.3)
                elif cell == Cell.Goal:
                    window.drawImage(self.imageGoal, px, py, cs, cs)

        # Free-Standing Objects
        for obj in self.objects:
            px = ox + b + cs * obj.x
            py = oy + b + cs * obj.y
            obj.draw(px, py, cs, window)

    def find(self, name):
        """ Return the object in the world with the given name """
        for obj in self.objects:
            if hasattr(obj, 'getName') and obj.getName() == name:
                return obj
        return None

    def getCell(self, x, y) -> Cell:
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return Cell.OutOfBounds
        return self.cells[x][y]

    def load(self, layout: Layout):
        """ Load a world from a string-based layout.
               [X, C] -> Main Character (a cat!)
               [W, |, +] -> Wall
               [P, !] -> Goal (a pizza!)
        """
        data = [x.strip() for x in layout.value.strip().split('\n')]
        self.__clear(len(data[0]))
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                if cell in ['W', '|', '+']:
                    self.cells[x][y] = Cell.Wall
                elif cell in ['X', 'C']:
                    self.addObject(Cat(x, y))
                elif cell in ['!', 'P']:
                    self.cells[x][y] = Cell.Goal
                else:
                    self.cells[x][y] = Cell.Empty

    def update(self, dt):
        """ Update the state of the world and the objects therein """
        for obj in self.objects:
            obj.update(dt)
