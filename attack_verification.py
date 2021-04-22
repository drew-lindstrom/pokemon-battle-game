from pokemon import Pokemon


def check_flinched(attacker, move_name):
    if "Flinched" in attacker.volatile_statuses:
        print(f"{attacker.name} flinched!")
        return True
    return False


def check_choice_item():
    if (
        "Choice Locked" in attacker.violatile_statuses
        and previous_move != None
        and previous_move != move_name
    ):
        print(f"{attacker.name} can only use {attacker.previous_move}")
        return True
    return False


def check_encored():
    if (
        "Encored" in attacker.violatile_statuses
        and previous_move != None
        and previous_move != move_name
    ):
        print(f"{attacker.name} can only use {attacker.previous_move}")
        return True
    return False


def check_taunted():
    if (
        "Taunted" in attacker.violatile_statuses
        and attacker.moves[n].category == "Status"
    ):
        print(f"{attacker.name} must use at attacking move while taunted.")
        return True
    return False


def check_disabled():
    if (
        "Disabled" in attacker.violatile_statuses
        and attacker.violatile_statuses["Disabled"][1] == move_name
    ):
        print(f"{attacker.name} is not able to use {move_name} while it is disabled.")
        return True
    return False


def pp_check():
    pass