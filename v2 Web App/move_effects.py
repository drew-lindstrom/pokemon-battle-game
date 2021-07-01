from player import Player
from pokemon import Pokemon
from move import Move
from terrain import Terrain
import gameText


def activateDefog(frame):
    """Using defog clears entry hazards from both sides of the field and lowers the opposing pokemon's evasion by 1."""
    frame.attackingTeam.clearHazards()
    frame.defendingTeam.clearHazards()
    gameText.output.append("The entry hazards were removed from the field!")
    gameText.output.append("")
    frame.target.updateStatModifier("evasion", -1)


def activateRoost(frame):
    """Activates effects of roost. Heals user by 50% of max hp and adds temporary grounded to vStatus for 1 turn."""
    frame.user.applyHeal(0.5)
    frame.user.vStatus["Temporary Grounded"] = [1]


def activateSlackOff(frame):
    """Activates effect of slack off. Heals user by 50% of max hp."""
    frame.user.applyHeal(0.5)


def setStealthRocks(frame):
    """Adds stealth rocks to the target player's side."""
    if frame.defendingTeam.stealthRocks == False:
        frame.defendingTeam.stealthRocks = True
        gameText.output.append("Stealth Rocks were placed on the opposing teams side!")
        gameText.output.append("")
