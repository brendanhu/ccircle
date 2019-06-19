from cc.image import Image
from cc.window import Window
from pyproject.scenario01.skeleton.constant import Direction


class Cat:
    NAME = 'pusheen'

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tx = x
        self.ty = y
        self.images_by_direction = {
            Direction.NORTH: Image('pyproject/scenario01/image/cat_n.png'),
            Direction.EAST: Image('pyproject/scenario01/image/cat_e.png'),
            Direction.SOUTH: Image('pyproject/scenario01/image/cat_s.png'),
            Direction.WEST: Image('pyproject/scenario01/image/cat_w.png'),
        }
        self.direction = Direction.WEST

    def draw(self, x, y, s, window: Window):
        image = self.images_by_direction.get(self.direction)
        window.drawImage(image, x, y, s, s)

    @staticmethod
    def getName():
        return Cat.NAME

    def update(self, dt):
        pass
