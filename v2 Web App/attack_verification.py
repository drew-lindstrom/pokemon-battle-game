from pokemon import Pokemon
import gameText


def checkFlinched(attacker, moveName, n):
    if "Flinched" in attacker.vStatus:
        gameText.output.append(f"{attacker.name} flinched!")
        return True
    return False


def checkChoiceItem(attacker, moveName, n):
    if (
        "Choice Locked" in attacker.vStatus
        and attacker.prevMove != None
        and attacker.prevMove != moveName
    ):
        gameText.output.append(f"{attacker.name} can only use {attacker.prevMove}")
        return True
    return False


def checkEncored(attacker, moveName, n):
    if (
        "Encored" in attacker.vStatus
        and attacker.prevMove != None
        and attacker.prevMove != moveName
    ):
        gameText.output.append(f"{attacker.name} can only use {attacker.prevMove}")
        return True
    return False


def checkTaunted(attacker, moveName, n):
    if "Taunted" in attacker.vStatus and attacker.moves[n].category == "Status":
        gameText.output.append(
            f"{attacker.name} must use at attacking move while taunted."
        )
        return True
    return False


def checkDisabled(attacker, moveName, n):
    if "Disabled" in attacker.vStatus and attacker.vStatus["Disabled"][1] == moveName:
        gameText.output.append(
            f"{attacker.name} is not able to use {moveName} while it is disabled."
        )
        return True
    return False
