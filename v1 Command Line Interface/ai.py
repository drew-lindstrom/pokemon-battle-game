from frame import Frame
import ui
import util
from damage_calc import calcDamage


def chooseMove(frame):
    highestDamage, moveNumber = chooseHighestDamagingAttack(frame)

    # If AI doesn't have a damaging attack availble, it will switch to its next available pokemon.
    if moveNumber is None:
        chooseNextPokemon(frame)
        frame.attack = None
    else:
        frame.attack = frame.user.moves[moveNumber]

    return frame


def chooseHighestDamagingAttack(frame):
    highestDamage = -float("inf")
    moveNumber = None

    for n in range(len(frame.user.moves)):
        if checkIfDamagingAttack(frame, n) and checkIfNoTypeImmunity(frame, n):
            damage = calcDamage(
                frame, includeCrit=False, includeRandom=False, ghostCalc=True
            )
            highestDamage, moveNumber = setHighestDamageAndMoveNumber(
                highestDamage, damage, moveNumber, n
            )

    return highestDamage, moveNumber


def checkIfDamagingAttack(frame, n):
    moveCategory = frame.user.moves[n].category
    if (
        moveCategory == "Physical" or moveCategory == "Special"
    ) and ui.checkIfValidChoice(frame, n + 1):
        # ui.checkIfValidChoice subtracts 1 from the given int due to first attack being tied with '1' key.
        return True
    return False


def checkIfNoTypeImmunity(frame, n):
    frame.attack = frame.user.moves[n]
    if util.checkImmunity(frame):
        return True
    return False


def setHighestDamageAndMoveNumber(highestDamage, damage, moveNumber, n):
    if damage > highestDamage:
        highestDamage = damage
        moveNumber = n
    return highestDamage, moveNumber


def chooseNextPokemon(frame):
    for n in range(1, 6):
        if frame.attackingTeam[n].status[0] != "Fainted":
            frame.switchChoice = n
            break
