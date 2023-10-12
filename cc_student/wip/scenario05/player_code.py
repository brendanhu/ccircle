""" Your solution goes in this file! See README.md for more information. """
from cc_student.wip.scenario05.skeleton.problem import Marketplace


class PlayerCode:
    def __init__(self):
        # If you want to keep track of any variables, you can initialize them here using self.variable_name = value
        pass

    @property
    def difficulty(self):
        """ Controls how difficult the simulation is:
               0.0 -> easiest
               0.5 -> moderate
               1.0 -> hardest
        """
        return 0.0

    @property
    def pause_time(self) -> float:
        """ Controls how fast the simulation runs; 0 = fastest. """
        return 0.1

    @property
    def seed(self) -> int:
        """ Use different numbers to get different random variations of the simulation. """
        return 1337

    def optimize(self, marketplace: Marketplace) -> None:
        """ Analyze the market for the current day and optimize freight fulfillment as you see fit.

            Try to make as much money as you can!

            This is a very basic and bad starter strategy: TODO.
        """
        pass
