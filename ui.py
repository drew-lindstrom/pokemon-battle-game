from player import Player
import stat_calc


def printPokemonOnField(frame1, frame2):
    frame_order = [frame1, frame2]

    for frame in frame_order:
        print(
            f"{frame.user.name} - HP: {frame.user.stat['hp']}/{frame.user.stat['max_hp']}, Status: {frame.user.status[0]}"
        )
        print(
            f"Attack: {stat_calc.calc_attack(frame)}/{frame.user.stat['attack']}   Defense: {stat_calc.calc_defense(frame, 'user')}/{frame.user.stat['defense']}   Special Attack: {stat_calc.calc_sp_attack(frame)}/{frame.user.stat['sp_attack']}"
        )
        print(
            f"Special Defense: {stat_calc.calc_sp_defense(frame, 'user')}/{frame.user.stat['sp_defense']}   Speed: {stat_calc.calc_speed(frame)}/{frame.user.stat['speed']}"
        )
        print()


def getChoice(frame, inputList=[], printTextBool=False):
    choice = None

    while choice is None and choice not in range(1, 7):
        printOptions(frame.attacking_team)
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
    if "Move Lock" in frame.user.v_status and (
        frame.user.prev_move != None
        and frame.user.prev_move != frame.user.moves[choice - 1].name
    ):
        if printTextBool:
            print(f"{frame.user.name} must use {frame.user.prev_move}.")
            print()
        return False
    return True


def callGetSwitchFunction(frame, inputList=[]):
    if len(inputList) > 0:
        getSwitch(frame, inputList)
    getSwitch(frame)


def printUserStats(frame):
    frame.user.show_stats()


def printOptions(team):
    print(f"What will {team.cur_pokemon.name} do?")
    print()
    for n in range(len(team.cur_pokemon.moves)):
        print(
            f"({n+1}) {team.cur_pokemon.moves[n].name} - {team.cur_pokemon.moves[n].pp}/{team.cur_pokemon.moves[n].max_pp} PP"
        )
    print()
    print("(5) Switch Pokemon")
    print("(6) Details")
    print()


def getSwitch(frame, inputList=[]):
    teamList = []
    switchChoice = ""

    for n in range(1, len(frame.attacking_team)):
        teamList.append(n)

    while switchChoice not in teamList:
        printSwitchChoices(frame)
        switchChoice = getNextSwitchChoice(frame, inputList)
        switchChoice = checkIfSwitchChoiceHasFainted(frame, switchChoice)

    frame.switch_choice = switchChoice


def printSwitchChoices(frame):
    print(f"Switch {frame.user.name} with...?")
    for n in range(1, len(frame.attacking_team)):
        print(
            f"({n}) {frame.attacking_team[n].name} - {frame.attacking_team[n].stat['hp']}/{frame.attacking_team[n].stat['max_hp']} HP, Status: {frame.attacking_team[n].status[0]}"
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
        if frame.attacking_team[switchChoice].status[0] == "Fainted":
            print(
                f"{frame.attacking_team[switchChoice].name} has fainted and cannot be switched in!"
            )
            switchChoice = 0
        print()
    except Exception:
        switchChoice = 0
    return switchChoice


def clearScreen():
    for n in range(17):
        print()
