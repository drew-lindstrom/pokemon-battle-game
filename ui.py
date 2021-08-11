from player import Player
import stat_calc
import gameText


def callAppropriateFunctionBasedOnChoice(
    frame, choice, inputList=[], printTextBool=False
):
    if choice >= 1 and choice <= 4:
        if checkIfValidChoice(frame, choice, printTextBool):
            frame.attack = frame.user.moves[choice - 1]
            return True

    elif choice >= 5 and choice <= 9:
        if checkIfSwitchChoiceHasFainted(frame, choice):
            frame.switchChoice = choice - 4
            return True
    return False


def checkIfValidChoice(frame, choice, printTextBool=False):
    if checkIfChoiceHasEnoughPP(
        frame, choice, printTextBool
    ) and checkIfUserHasMoveLock(frame, choice, printTextBool):
        return True
    return False


def checkIfChoiceHasEnoughPP(frame, choice, printTextBool=False):
    if frame.user.moves[choice - 1].pp <= 0:
        if printTextBool:
            gameText.output.append(
                f"{frame.user.moves[choice - 1].name} is out of PP.")
            gameText.output.append("")
        return False
    return True


def checkIfUserHasMoveLock(frame, choice, printTextBool=False):
    if "Move Lock" in frame.user.vStatus and (
        frame.user.prevMove != None
        and frame.user.prevMove != frame.user.moves[choice - 1].name
    ):
        if printTextBool:
            gameText.output.append(
                f"{frame.user.name} must use {frame.user.prevMove}.")
            gameText.output.append("")
        return False
    return True


def checkIfSwitchChoiceHasFainted(frame, switchChoice):
    switchChoice = switchChoice - 4

    if frame.attackingTeam[switchChoice].status[0] == "Fainted":
        gameText.output.append(
            f"{frame.attackingTeam[switchChoice].name} has fainted and can't switch in."
        )
        gameText.output.append("")
        return False
    return True
