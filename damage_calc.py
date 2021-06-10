import random
import time

from move import Move
from game_data import type_key, type_chart, modified_base_damage_list
from pokemon import Pokemon
from player import Player
from stat_calc import *


def roll_crit(frame, i=None):
    """Rolls to determine if a move lands a critical hit. Critical hits boost damage by 1.5 ignore the attacker's negative stat stages,
    the defender's positive stat stages, and Light Screen/Reflect/Auorar Veil. Burn is not ignored."""
    if i is None or i < 0 or i > 24:
        i = random.randint(1, 24)
    if i == 1:
        print("A critical hit!")
        print()
        frame.crit = True
        return 1.5
    else:
        return 1


def check_stab(frame):
    """Checks to see if the attacking move is the same type as the attacker. If so, attack power is boosted by 50%."""
    if frame.attack.type in frame.user.typing:
        return 1.5
    else:
        return 1


def check_type_effectiveness(frame):
    """Return the damage multiplier for how super effective the move is. type_chart is a matrix showing how each type matches up between each
    other. X-axis is the defending type, y-axis is the attacking type. Top left corner is (0, 0). Each type corresponds to a number on the
    x and y axis."""

    atk_id = type_key.get(frame.attack.type)
    def1_id = type_key.get(frame.target.typing[0])
    mult_1 = type_chart[atk_id][def1_id]
    try:
        def2_id = type_key.get(frame.target.typing[1])
        mult_2 = type_chart[atk_id][def2_id]
    except:
        mult_2 = 1

    modifier = mult_1 * mult_2

    if modifier > 1:
        print("It's super effective!")
    elif modifier < 1 and modifier > 0:
        print("It's not very effective...")
    elif modifier == 0:
        print("It had no effect...")

    return modifier


def check_burn(frame):
    """Returns damage modifer is user is burned and currently attacking with a physical move."""
    if frame.user.status[0] == "Burn" and frame.attack.category == "Physical":
        return 0.5
    return 1


def roll_random(i=None):
    if i is None or i < 85 or i > 100:
        i = random.randint(85, 100)
    return float(i) / 100


def check_attacking_and_defending_stats(frame):
    """Checks if the attack for the given frame is Physical or Special. If physical, returns Attack and Defense for stats used in damage calc.
    If special, returns Special Attack and Special Defense. If the attack is Psyshock, returns Special Attack and Defense."""
    if frame.attack.name == "Psyshock":
        attack_stat = calc_sp_attack(frame)
        defense_stat = calc_defense(frame)
    elif frame.attack.category == "Physical":
        attack_stat = calc_attack(frame)
        defense_stat = calc_defense(frame)
    elif frame.attack.category == "Special":
        attack_stat = calc_sp_attack(frame)
        defense_stat = calc_sp_defense(frame)

    return attack_stat, defense_stat


def activate_eruption(frame):
    """Returns base power for the move eruption based on the users hp."""
    return int(150 * frame.user.stat["hp"] / frame.user.stat["max_hp"])


def activate_knock_off(frame):
    """Returns knock off base power raised by 50% if target is holding an item. Target then loses held item."""
    if frame.target.item:
        print(f"{frame.target.name} lost their item!")
        print()

        frame.target.item = None
        return int(65 * 1.5)

    else:
        return 65


def calc_modified_base_damage(frame):
    """Returns base power for various moves that have varying base powers based on different parameters."""
    if frame.attack.name == "Eruption":
        return activate_eruption(frame)

    if frame.attack.name == "Knock Off" and frame.target.item:
        return activate_knock_off(frame)


def calc_modified_damage():
    pass


def calc_damage(frame, include_crit=True, include_random=True):
    """Returns damage from an attack for a given frame."""
    crit, random_mod = 1, 1

    if include_crit == True:
        crit = roll_crit(frame)
    if include_random == True:
        random_mod = roll_random()

    stab = check_stab(frame)
    typ = check_type_effectiveness(frame)
    burn = check_burn(frame)

    attack_stat, defense_stat = check_attacking_and_defending_stats(frame)

    if frame.attack.name in modified_base_damage_list:
        base_damage = calc_modified_base_damage
    else:
        base_damage = frame.attack.power

    damage = int(
        (
            int(
                (
                    (int(2 * frame.user.level / 5) + 2)
                    * int(base_damage)
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
        * random_mod
    )

    return damage
