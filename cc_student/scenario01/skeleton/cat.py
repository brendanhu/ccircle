from cc.image import Image
from cc.window import Window
from cc_student.scenario01.skeleton.constant import Direction


class Cat:
    NAME = 'pusheen'

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tx = x
        self.ty = y
        self.images_by_direction = {
            Direction.NORTH: Image('cc_student/scenario01/assets/images/cat_n.png'),
            Direction.EAST: Image('cc_student/scenario01/assets/images/cat_e.png'),
            Direction.SOUTH: Image('cc_student/scenario01/assets/images/cat_s.png'),
            Direction.WEST: Image('cc_student/scenario01/assets/images/cat_w.png'),
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
