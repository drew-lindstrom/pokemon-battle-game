from player import Player
import stat_calc
import gameText


def printPokemonOnField(frame1, frame2):
    frameOrder = [frame1, frame2]

    for frame in frameOrder:
        gameText.output += f"{frame.user.name} - HP: {frame.user.stat['hp']}/{frame.user.stat['maxHp']}, Status: {frame.user.status[0]}\n"
        gameText.output += f"Attack: {stat_calc.calcAttack(frame)}/{frame.user.stat['attack']}   Defense: {stat_calc.calcDefense(frame, 'user')}/{frame.user.stat['defense']}   Special Attack: {stat_calc.calcSpAttack(frame)}/{frame.user.stat['spAttack']}\n"
        gameText.output += f"Special Defense: {stat_calc.calcSpDefense(frame, 'user')}/{frame.user.stat['spDefense']}   Speed: {stat_calc.calcSpeed(frame)}/{frame.user.stat['speed']}\n\n"


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


def callGetSwitchFunction(frame, inputList=[]):
    if len(inputList) > 0:
        getSwitch(frame, inputList)
    getSwitch(frame)


def printUserStats(frame):
    frame.user.showStats()


def printOptions(frame):
    gameText.output += f"What will {frame.user.name} do?\n"
    for n in range(len(frame.user.moves)):
        gameText.output += f"({n}) {frame.user.moves[n].name} - {frame.user.moves[n].pp}/{frame.user.moves[n].maxPp} PP\n"
    for n in range(1, len(frame.attackingTeam)):
        gameText.output += f"({n+3}) {frame.attackingTeam[n].name} - {frame.attackingTeam[n].stat['hp']}/{frame.attackingTeam[n].stat['maxHp']} HP, Status: {frame.attackingTeam[n].status[0]}\n"


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
