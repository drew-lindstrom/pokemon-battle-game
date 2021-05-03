from pokemon import Pokemon
from game_data import (
    stat_alt_attacks,
    status_inflicting_attacks,
    v_status_inflicting_attacks,
)
from frame import Frame
import random


def apply_stat_alt_attack(frame, i=None):
    """If the current attack is in the stat_alt_attack dictionary, rolls to see if the attack successfully
    alters a certain stat/stats of the user or target. Function then calls the update_stat_modifier method to alter the approriate stat."""
    if frame.attack in stat_alt_attacks:
        cur_move = stat_alt_attacks[attack]
        if i is None:
            i = random.randint(1, 100)

        if i <= cur_move[1]:
            if cur_move[0] == "user":
                effected_pokemon = attacker
            else:
                effected_pokemon = target
            pos = 2
            while pos < len(cur_move):
                effected_pokemon.update_stat_modifier(cur_move[pos], cur_move[pos + 1])
                pos += 2


def apply_status_inflicting_attack(frame, i=None):
    """If the current attack is in the status_inflicting_attack dictionary, rolls to see if the attack successfully
    applies the status to the user or target. Function then calls the set_status method to update the pokemon's status."""
    if frame.attack in status_inflicting_attacks:
        cur_move = status_inflicting_attacks[attack]
        if i is None:
            i = random.randint(1, 100)

        if i <= cur_move[1]:
            if cur_move[0] == "user":
                effected_pokemon = attacker
            else:
                effected_pokemon = defender
            effected_pokemon.set_status(cur_move[2])


def apply_v_status_inflicting_attack(frame, i=None):
    """If the current attack is in the v_status_inflicting_attack dictionary, rolls to see if the attack successfully
    applies the volatile status to the user or target. Function then calls the set_v_status method to update the pokemon's status."""
    if frame.attack in status_inflicting_attacks:
        cur_move = status_inflicting_attacks[attack]
        if i is None:
            i = random.randint(1, 100)

        if i <= cur_move[1]:
            if cur_move[0] == "user":
                effected_pokemon = frame.user
            else:
                effected_pokemon = frame.target
            effected_pokemon.set_v_status(cur_move[2])


def apply_leftovers(frame):
    """Heals the user's HP at the end of the turn by 1/16 of it's max HP if holding leftovers."""
    if frame.user.item == "Leftovers":
        frame.user.heal(0.0625)
        print(f"{frame.user.name} healed some of it's HP with it's leftovers.")


def apply_burn(frame):
    """Damages a burned pokemon by 1/16 of its max HP. Fire type pokemon cannot be burned."""
    if frame.user.status[0] == "Burned":
        print(f"{frame.user.name} was damaged by its burn!")
        frame.user.apply_damage_percentage(0.0625)


def apply_bad_poison(frame):
    """Damages a baldy poison pokemon with increasingly higher damage at the end of every turn. Initially deals 1/16 of max HP
    but adds an addition 1/16 damage (up until 15 * floor(max hp/16)) every turn the pokemon is in. If the pokemon switches out,
    the damage resets to the original 1/16 of max HP."""
    if frame.user.status[0] == "Badly Poisoned":
        print(f"{frame.user.name} was hurt by the poison!")
        frame.user.apply_damage_percentage(0.0625 * (15 - frame.user.status[1]))