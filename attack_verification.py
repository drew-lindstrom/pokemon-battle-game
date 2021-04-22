from pokemon import Pokemon


def check_flinched(attacker, move_name, n):
    if "Flinched" in attacker.volatile_statuses:
        print(f"{attacker.name} flinched!")
        return True
    return False


def check_choice_item(attacker, move_name, n):
    if (
        "Choice Locked" in attacker.volatile_statuses
        and attacker.prev_move != None
        and attacker.prev_move != move_name
    ):
        print(f"{attacker.name} can only use {attacker.prev_move}")
        return True
    return False


def check_encored(attacker, move_name, n):
    if (
        "Encored" in attacker.volatile_statuses
        and attacker.prev_move != None
        and attacker.prev_move != move_name
    ):
        print(f"{attacker.name} can only use {attacker.prev_move}")
        return True
    return False


def check_taunted(attacker, move_name, n):
    if (
        "Taunted" in attacker.volatile_statuses
        and attacker.moves[n].category == "Status"
    ):
        print(f"{attacker.name} must use at attacking move while taunted.")
        return True
    return False


def check_disabled(attacker, move_name, n):
    if (
        "Disabled" in attacker.volatile_statuses
        and attacker.volatile_statuses["Disabled"][1] == move_name
    ):
        print(f"{attacker.name} is not able to use {move_name} while it is disabled.")
        return True
    return False


def pp_check():
    pass