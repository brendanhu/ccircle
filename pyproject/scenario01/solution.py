""" Your solution goes in this file! """
from pyproject.scenario01 import worlds
from pyproject.scenario01.cat import Cat


class Solution:
    """
    GOAL: Fill in the code for this class's function 'moveTowardPizza' to ensure that the cat finds the pizza!

    Use the following functions to understand the cat's situation:

        cat.isBlocked() -> Bool
            returns True if the cat is facing a wall or the edge of the maze, False if the coast is clear
        cat.isFacingN() -> Bool
            True iff cat is facing north
        cat.isFacingS() -> Bool
            True iff cat is facing south
        cat.isFacingE() -> Bool
            True iff cat is facing east
        cat.isFacingW() -> Bool
            True iff cat is facing west
        cat.smellsPizza() -> Bool
            True iff the cat is right in front of the pizza (and is facing it)

        Just a refresher...:

                   /|\
                    |
                  North
                    |
        <-- West --- --- East --->
                    |
                    |
                  South
                    |
                   \|/

    Use the following functions to instruct the cat:

        cat.turnLeft() -> None
            Instructs the cat to turn left / counter-clockwise
        cat.turnRight() -> None
            Instructs the cat to turn right / clockwise
        cat.walk() -> None
            Instructs the cat to walk in the direction it is facing

    NOTE: You can only call cat.walk() ONCE per call to moveTowardPizza!!
    """
    def __init__(self):
        # If you want to keep track of any variables, you can initialize them here using self.var = value
        pass

    @staticmethod
    def getLevel() -> str:
        """ Choose your level here: 'worlds.easy()', 'worlds.medium()', or 'worlds.hard()'! """
        return worlds.easy()

    @staticmethod
    def getPauseTime() -> float:
        """ Smaller pause time = faster simulation. """
        return 0.01

    def moveTowardPizza(self, cat: Cat):
        """ Your code here! """
        pass
