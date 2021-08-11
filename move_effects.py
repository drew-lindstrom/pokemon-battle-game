from player import Player
from pokemon import Pokemon
from move import Move
from terrain import Terrain
import gameText


def activateDefog(frame):
    frame.attackingTeam.clearHazards()
    frame.defendingTeam.clearHazards()
    gameText.output.append("The entry hazards were removed from the field!")
    gameText.output.append("")
    frame.target.updateStatModifier("evasion", -1)


def activateRoost(frame):
    frame.user.applyHeal(0.5)
    frame.user.vStatus["Temporary Grounded"] = [1]


def activateSlackOff(frame):
    frame.user.applyHeal(0.5)


def setStealthRocks(frame):
    if frame.defendingTeam.stealthRocks == False:
        frame.defendingTeam.stealthRocks = True
        gameText.output.append(
            "Stealth Rocks were placed on the opposing teams side!")
        gameText.output.append("")
