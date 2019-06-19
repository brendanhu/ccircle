""" Your solution goes in this file! See README.md for more information. """
from pyproject.scenario01.skeleton.cat import Cat
from pyproject.scenario01.skeleton.constant import Layout


class Solution:
    def __init__(self):
        # If you want to keep track of any variables, you can initialize them here using self.variable_name = value
        pass

    @staticmethod
    def getLevel() -> Layout:
        """ Choose your level here. """
        return Layout.EASY

    @staticmethod
    def getPauseTime() -> float:
        """ Smaller pause time = faster simulation. """
        return 0.01

    def moveTowardPizza(self, cat: Cat):
        """ Your code here! """
        pass
