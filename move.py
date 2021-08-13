from game_data import movesDict
from copy import deepcopy
import gameText
import json


class Move:
    def __init__(self, name, type=None, category=None, power=None, accuracy=None, pp=None, maxPp=None):
        self.name = name
        self.type = movesDict[name][0]
        self.category = movesDict[name][1]
        self.pp = None

        power = movesDict[self.name][2]
        if power == None:
            power = 0
        self.power = int(power)

        accuracy = movesDict[self.name][3]
        if accuracy == None:
            accuracy = 0
        self.accuracy = int(accuracy)

        maxPp = int(movesDict[self.name][4])
        if maxPp <= 1:
            pass
        else:
            maxPp = int(maxPp * 1.6)
        self.maxPp = maxPp

        self.pp = self.maxPp

    def __repr__(self):
        return self.name

    def showStats(self):
        gameText.output.append(f"Move: {self.moveName}")
        gameText.output.append(f"Type: {self.type}")
        gameText.output.append(f"Category: {self.category}")
        gameText.output.append(f"Power: {self.power}")
        gameText.output.append(f"Accuracy: {self.accuracy}")
        gameText.output.append(f"PP: {self.pp}/{self.maxPp}")
        gameText.output.append("")

    def checkPp(self):
        if self.pp <= 0:
            gameText.output.append(f"{self.name} is out of PP!")
            gameText.output.append("")
            return False
        return True

    def decrementPp(self):
        self.pp -= 1

    @classmethod
    def deserializeAndUpdateMoveFromJson(cls, data):
        return cls(**data)
