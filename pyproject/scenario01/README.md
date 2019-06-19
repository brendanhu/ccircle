GOAL: Fill in the code in Solution.py for the function 'moveTowardPizza' to ensure that the cat finds the pizza!

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

Use the following functions to instruct the cat:

    cat.turnLeft() -> None
        Instructs the cat to turn left / counter-clockwise
    cat.turnRight() -> None
        Instructs the cat to turn right / clockwise
    cat.walk() -> None
        Instructs the cat to walk in the direction it is facing

NOTE: You can only call cat.walk() ONCE per call to moveTowardPizza!!