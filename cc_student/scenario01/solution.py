""" Your solution goes in this file! See README.md for more information. """
from cc_student.scenario01.skeleton.cat import Cat
from cc_student.scenario01.skeleton.constant import Layout


class Solution:
    def __init__(self):
        # If you want to keep track of any variables, you can initialize them here using self.variable_name = value
        pass

    @staticmethod
    def get_level() -> Layout:
        """ Choose your level here. """
        return Layout.EASY

    @staticmethod
    def get_pause_time() -> float:
        """ Smaller pause time = faster simulation. """
        return 0.01

    # noinspection PyMethodMayBeStatic
    def move_towards_pizza(self, cat: Cat):
        """ Your code here! """
        pass
