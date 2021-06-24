from player import Player
import stat_calc


def printPokemonOnField(frame1, frame2):
    frameOrder = [frame1, frame2]

    for frame in frameOrder:
        print(
            f"{frame.user.name} - HP: {frame.user.stat['hp']}/{frame.user.stat['maxHp']}, Status: {frame.user.status[0]}"
        )
        print(
            f"Attack: {stat_calc.calcAttack(frame)}/{frame.user.stat['attack']}   Defense: {stat_calc.calcDefense(frame, 'user')}/{frame.user.stat['defense']}   Special Attack: {stat_calc.calcSpAttack(frame)}/{frame.user.stat['spAttack']}"
        )
        print(
            f"Special Defense: {stat_calc.calcSpDefense(frame, 'user')}/{frame.user.stat['spDefense']}   Speed: {stat_calc.calcSpeed(frame)}/{frame.user.stat['speed']}"
        )
        print()


def getChoice(frame, inputList=[], printTextBool=False):
    choice = None

    while choice is None and choice not in range(1, 7):
        printOptions(frame.attackingTeam)
        choice = getNextChoice(frame, inputList)

        if callAppropriateFunctionBasedOnChoice(
            frame, choice, inputList, printTextBool
        ):
            return frame
        choice = None


def getNextChoice(frame, inputList=[]):
    if len(inputList) == 0:
        choice = input()
    else:
        choice = inputList.pop(0)
    print()

    try:
        return int(choice)
    except Exception:
        return 0


def callAppropriateFunctionBasedOnChoice(
    frame, choice, inputList=[], printTextBool=False
):
    if choice >= 1 and choice <= 4:
        if checkIfValidChoice(frame, choice, printTextBool):
            return True

    elif choice == 5:
        callGetSwitchFunction(frame, inputList)
        return True

    elif choice == 6:
        printUserStats(frame)
    return False


def checkIfValidChoice(frame, choice, printTextBool=False):
    if checkIfChoiceHasEnoughPP(
        frame, choice, printTextBool
    ) and checkIfUserHasMoveLock(frame, choice, printTextBool):
        frame.attack = frame.user.moves[choice - 1]
        return True
    return False


def checkIfChoiceHasEnoughPP(frame, choice, printTextBool=False):
    if frame.user.moves[choice - 1].pp <= 0:
        if printTextBool:
            print(f"{frame.user.moves[choice - 1].name} is out of PP.")
            print()
        return False
    return True


def checkIfUserHasMoveLock(frame, choice, printTextBool=False):
    if "Move Lock" in frame.user.vStatus and (
        frame.user.prevMove != None
        and frame.user.prevMove != frame.user.moves[choice - 1].name
    ):
        if printTextBool:
            print(f"{frame.user.name} must use {frame.user.prevMove}.")
            print()
        return False
    return True


def callGetSwitchFunction(frame, inputList=[]):
    if len(inputList) > 0:
        getSwitch(frame, inputList)
    getSwitch(frame)


def printUserStats(frame):
    frame.user.showStats()


def printOptions(team):
    print(f"What will {team.curPokemon.name} do?")
    print()
    for n in range(len(team.curPokemon.moves)):
        print(
            f"({n+1}) {team.curPokemon.moves[n].name} - {team.curPokemon.moves[n].pp}/{team.curPokemon.moves[n].maxPP} PP"
        )
    print()
    print("(5) Switch Pokemon")
    print("(6) Details")
    print()


def getSwitch(frame, inputList=[]):
    teamList = []
    switchChoice = ""

    for n in range(1, len(frame.attackingTeam)):
        teamList.append(n)

    while switchChoice not in teamList:
        printSwitchChoices(frame)
        switchChoice = getNextSwitchChoice(frame, inputList)
        switchChoice = checkIfSwitchChoiceHasFainted(frame, switchChoice)

    frame.switchChoice = switchChoice


def printSwitchChoices(frame):
    print(f"Switch {frame.user.name} with...?")
    for n in range(1, len(frame.attackingTeam)):
        print(
            f"({n}) {frame.attackingTeam[n].name} - {frame.attackingTeam[n].stat['hp']}/{frame.attackingTeam[n].stat['maxHp']} HP, Status: {frame.attackingTeam[n].status[0]}"
        )
    print()


def getNextSwitchChoice(frame, inputList=[]):
    if len(inputList) == 0:
        switchChoice = input()
    else:
        switchChoice = inputList.pop(0)

    try:
        return int(switchChoice)
    except Exception:
        return 0


def checkIfSwitchChoiceHasFainted(frame, switchChoice):
    try:
        if frame.attackingTeam[switchChoice].status[0] == "Fainted":
            print(
                f"{frame.attackingTeam[switchChoice].name} has fainted and cannot be switched in!"
            )
            switchChoice = 0
        print()
    except Exception:
        switchChoice = 0
    return switchChoice


def clearScreen():
    for n in range(17):
        print()
