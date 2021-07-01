from game_data import movesDict
from copy import deepcopy


class Move:
    def __init__(self, name):
        self.name = name
        self.type = movesDict[name][0]
        self.category = movesDict[name][1]
        self.pp = None

    def __repr__(self):
        return self.name

    @property
    def power(self):
        power = movesDict[self.name][2]
        if power == None:
            return 0
        return int(power)

    @property
    def accuracy(self):
        accuracy = movesDict[self.name][3]
        if accuracy == None:
            return 0
        return int(accuracy)

    @property
    def maxPp(self):
        maxPp = int(movesDict[self.name][4])
        if maxPp <= 1:
            return maxPp
        return int(maxPp * 1.6)

    @property
    def pp(self):
        return self._pp

    @pp.setter
    def pp(self, n):
        if n == None or n > self.maxPp:
            self.pp = self.maxPp
        elif n <= 0:
            self._pp = 0
        else:
            self._pp = n

    def showStats(self):

        print(f"Move: {self.name}")
        print(f"Type: {self.type}")
        print(f"Category: {self.category}")
        print(f"Power: {self.power}")
        print(f"Accuracy: {self.accuracy}")
        print(f"PP: {self.pp}/{self.maxPp}")
        print()

    def checkPp(self):
        """Returns True if a move has enough PP to be used (above 0 PP). Returns False otherwise.
        move.pp (int) -> Boolean
        Ex: move.pp == 0, return False.
        Ex: move.pp == 3, return True."""
        if self.pp <= 0:
            print(f"{self.name} is out of PP!")
            return False
        return True

    def decrementPp(self):
        """Decrements a move's pp by one at the end of the turn."""
        self.pp -= 1