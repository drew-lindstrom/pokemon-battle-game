import random
import time

from move import Move
from game_data import type_key, type_chart, modified_base_damage_list
from pokemon import Pokemon
from player import Player


def roll_crit(i=None):
    """Rolls to determine if a move lands a critical hit. Critical hits boost damage by 1.5 ignore the attacker's negative stat stages,
    the defender's positive stat stages, and Light Screen/Reflect/Auorar Veil. Burn is not ignored."""
    if i is None or i < 0 or i > 24:
        i = random.randint(1, 24)
    if i == 1:
        print("A critical hit!")
        return 1.5
    else:
        return 1


def check_stab(user, attack):
    """Checks to see if the attacking move is the same type as the attacker. If so, attack power is boosted by 50%."""
    if attack.type in user.typing:
        return 1.5
    else:
        return 1


def check_type_effectiveness(user, attack, target):
    """Return the damage multiplier for how super effective the move is. type_chart is a matrix showing how each type matches up between each
    other. X-axis is the defending type, y-axis is the attacking type. Top left corner is (0, 0). Each type corresponds to a number on the
    x and y axis."""

    atk_id = type_key.get(attack.type)
    def1_id = type_key.get(target.typing[0])
    mult_1 = type_chart[atk_id][def1_id]
    try:
        def2_id = type_key.get(target.typing[1])
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


def check_burn(user, attack):
    """Returns damage modifer is user is burned and currently attacking with a physical move."""
    if user.status[0] == "Burn" and attack.category == "Physical":
        return 0.5
    return 1


def roll_random(i=None):
    if i is None or i < 85 or i > 100:
        i = random.randint(85, 100)
    return float(random) / 100


def activate_eruption(frame):
    """Returns base power for the move eruption based on the users hp."""
    return int(150 * frame.user.stats["hp"] / frame.attacker.stats["max_hp"])


def calc_modified_base_damage(frame):
    """Returns base power for various moves that have varying base powers based on different parameters."""
    if frame.attack_name == "Eruption":
        return use_eruption(frame)


def calc_modified_damage():
    pass


def activate_defog(player1, player2):
    """Using defog clears entry hazards from both sides of the field and lowers the opposing pokemon's evasion by 1."""
    player.clear_hazards(player1)
    player.clear_hazards(player2)
    print("The entry hazards were removed from the field!")
    player2.cur_pokemon.update_stat_modifier("evasion", -1)


def calc_damage(frame):
    """Returns damage from an attack for a given frame."""
    #  TODO: Critical hit ignore thes attacker's negative stat stages, the defender's positive stat stages, and Light Screen/Reflect/Auorar Veil.
    # print(f'{attacker.name} used {attacker.moves[n]["name"]}!')
    print(f"{frame.user.name} used {frame.attack_name[0]}!")

    crit = roll_crit()
    stab = check_stab(frame.user, frame.attack)
    typ = check_type_effectiveness(frame.user, frame.attack, frame.target)
    burn = check_burn(frame.user, frame.attack)

    if frame.attack_name == "Psyshock":
        attack_stat = frame.user.stat["sp_attack"]
        defense_stat = frame.user.stat["defense"]
    elif frame.attack.category == "Physical":
        attack_stat = frame.user.stat["attack"]
        defense_stat = frame.target.stat["defense"]
    elif frame.attack.category == "Special":
        attack_stat = frame.user.stat["sp_attack"]
        defense_stat = frame.target.stat["sp_defense"]

    if frame.attack_name in modified_base_damage_list:
        # TODO: Implement modified_base_damage_list
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
    )

    return damage
