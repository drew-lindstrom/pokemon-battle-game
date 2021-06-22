from frame import Frame
import damage_calc


def choose_highest_damaging_attack(frame):
    """Returns a move index for user's highest damaging attack against the current target."""
    # TODO: Account for move lock.
    # TODO: Account for type immunity.
    highest_damage = -float("inf")
    move_number = 0
    include_crit = False
    include_random = False

    for n in range(len(frame.user.moves)):
        if (
            frame.user.moves[n].category == "Physical"
            or frame.user.moves[n].category == "Special"
        ) and frame.user.moves[n].pp > 0:
            frame.attack = frame.user.moves[n]
            damage = damage_calc.calc_damage(frame, include_crit, include_random)
            if damage > highest_damage:
                highest_damage = damage
                move_number = n

    frame.attack = frame.user.moves[move_number]
    return frame


def choose_next_pokemon(frame):
    for n in range(1, 6):
        if frame.attacking_team[n].status[0] != "Fainted":
            return n
