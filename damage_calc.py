from random import randint
import time

from move import Move
from game_data import type_key, type_chart
from pokemon import Pokemon


def next_turn(pokemon_1, action_1, pokemon_2, action_2):
    pass


def crit_check():
    """Rolls to determine if a move lands a critical hit. Critical hits boost damage by 1.5 ignore the attacker's negative stat stages,
    the defender's positive stat stages, and Light Screen/Reflect/Auorar Veil. Burn is not ignored."""
    # TO DO: add special moves/itesms/abilities.
    crit = randint(1, 24)
    if crit == 1:
        print("A critical hit!")
        return 1.5
    else:
        return 1


def accuracy_check(attacker, n, defender):
    """Rolls to determine if a move lands or misses."""
    num = 3
    den = 3
    modifier = attacker.stat_mods[5] - defender.stat_mods[6]

    if modifier > 6:
        modifier = 6
    elif modifier < -6:
        modifier = -6
    if modifier > 0:
        num = num + modifier
    elif modifier < 0:
        den = den + (modifier * -1)

    accuracy = int(attacker.moves[n].accuracy) * int(num / den)
    check = randint(1, 100)
    if check <= accuracy:
        return True
    else:
        return False


def evasion_check(attacker, n, defender):
    pass


def weather_check():
    pass


def stab_check(attacker, n):
    """Checks to see if the attacking move is the same type as the attacker. If so, attack power is boosted by 50%."""
    if (
        attacker.typing[0] == attacker.moves[n].type
        or attacker.typing[1] == attacker.moves[n].type
    ):
        return 1.5
    else:
        return 1


def type_effectiveness_check(attacker, n, defender):
    """Return the damage multiplier for how super effective the move is. type_chart is a matrix showing how each type matches up between each
    other. X-axis is the defending type, y-axis is the attacking type. Top left corner is (0, 0). Each type corresponds to a number on the
    x and y axis."""

    atk_id = type_key.get(attacker.moves[n].type)
    def1_id = type_key.get(defender.typing[0])
    mult_1 = type_chart[atk_id][def1_id]
    try:
        def2_id = type_key.get(defender.typing[1])
        mult_2 = type_chart[atk_id][def2_id]
    except:
        mult_2 = 1

    return mult_1 * mult_2


def burn_check(attacker, n):
    """Checks to see if the attacker is currently burned. If so and the attack is physical, damage is reduced by 50%."""
    if attacker.status == "Burn" and attacker.moves[n].category == "Physical":
        return 0.5
    else:
        return 1


def sleep_check():
    pass


def frozen_check():
    pass


def pp_check():
    pass


def random():

    pass


def attack(attacker, n, defender):
    """Determines if a move hits and how much damage is dealt."""
    #  TO DO: Critical hit ignore thes attacker's negative stat stages, the defender's positive stat stages, and Light Screen/Reflect/Auorar Veil.
    # TO DO: Added in stat modifiers and create a damage calc function.
    # print(f'{attacker.name} used {attacker.moves[n]["name"]}!')
    print(f"{attacker.name} used {attacker.moves[n].name}!")
    if accuracy_check(attacker, n, defender):
        crit = crit_check()
        stab = stab_check(attacker, n)
        typ = type_effectiveness_check(attacker, n, defender)
        burn = burn_check(attacker, n)

        if attacker.moves[n].category == "Physical":
            attack_stat = attacker.attack
            defense_stat = defender.defense
        elif attacker.moves[n].category == "Special":
            attack_stat = attacker.sp_attack
            defense_stat = defender.sp_defense

        damage = int(
            (
                int(
                    (
                        (int(2 * attacker.level / 5) + 2)
                        * int(attacker.moves[n].power)
                        * (attack_stat / defense_stat)
                    )
                    / 50
                )
                + 2
            )
            * crit
            * stab
            * typ
            * burn
        )

        defender.hp -= damage

        if typ > 1:
            print("It's super effective!")
        elif typ < 1 and typ > 0:
            print("It's not very effective...")
        elif typ == 0:
            print("It had no effect...")

    else:
        if attacker.name.endswith("s"):
            print(f"{attacker.name}' attack missed!")
        else:
            print(f"{attacker.name}'s attack missed!")

    attacker.moves[n].pp = int(attacker.moves[n].pp) - 1

    if defender.hp <= 0:
        defender.hp = 0
        defender.status = "Fainted"
        print(f"{defender.name} fainted!")
    # How to force a switch?

    print()