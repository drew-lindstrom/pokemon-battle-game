from frame import Frame
import damage_calc


def choose_highest_damaging_attack(frame):
    """Returns a move index for user's highest damaging attack against the current target."""
    # TODO: Account for move lock.
    highest_damage = -float("inf")
    move_number = 0
    for n in range(len(frame.user.moves)):
        if (
            frame.user.moves[n].category == "Physical"
            or frame.user.moves[n].category == "Special"
        ) and frame.user.moves[n].pp > 0:
            frame.attack = frame.user.moves[n]
            damage = damage_calc.calc_damage(frame, False, False)
            if damage > highest_damage:
                highest_damage = damage
                move_number = n

    return move_number
