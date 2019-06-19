""" All shapes are made out of triangles :) """
from abc import ABC, abstractmethod

from cc.image import Image


class Shape(ABC):
    def __init__(self, image: Image = None):
        """ An abstract shape that can be drawn using triangles (with optional texture). """
        super().__init__()
        self.image = image

    @abstractmethod
    def to_triangles(self):
        """ Turn this shape into a list of triangles. To be implemented by subclasses.

        Returns:
            tris (List[Triangle]): all the triangles which, when drawn, produce this shape.
        """
        pass

    def is_textured(self) -> bool:
        """ Checks if this shape is textured (as opposed to RGBA colored). """
        return bool(self.image)
