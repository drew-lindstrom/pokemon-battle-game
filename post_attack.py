from pokemon import Pokemon
from game_data import (
    stat_alt_attacks,
    status_inflicting_attacks,
    v_status_inflicting_attacks,
)
import random


def apply_stat_alt_attack(attacker, defender, attack_name, i=None):
    """If the current attack is in the stat_alt_attack dictionary, rolls to see if the attack successfully
    alters a certain stat/stats of the user or target. Function then calls the update_stat_modifier method to alter the approriate stat."""
    if attack_name in stat_alt_attacks:
        cur_move = stat_alt_attacks[attack_name]
        if i is None:
            i = random.randint(1, 100)

        if i <= cur_move[1]:
            if cur_move[0] == "user":
                effected_pokemon = attacker
            else:
                effected_pokemon = defender
            pos = 2
            while pos < len(cur_move):
                effected_pokemon.update_stat_modifier(cur_move[pos], cur_move[pos + 1])
                pos += 2


def apply_status_inflicting_attack(attacker, defender, attack_name, i=None):
    """If the current attack is in the status_inflicting_attack dictionary, rolls to see if the attack successfully
    applies the status to the user or target. Function then calls the set_status method to update the pokemon's status."""
    if attack_name in status_inflicting_attacks:
        cur_move = status_inflicting_attacks[attack_name]
        if i is None:
            i = random.randint(1, 100)

        if i <= cur_move[1]:
            if cur_move[0] == "user":
                effected_pokemon = attacker
            else:
                effected_pokemon = defender
            effected_pokemon.set_status(cur_move[2])


def apply_v_status_inflicting_attack(attacker, defender, attack_name, i=None):
    """If the current attack is in the v_status_inflicting_attack dictionary, rolls to see if the attack successfully
    applies the volatile status to the user or target. Function then calls the set_v_status method to update the pokemon's status."""
    if attack_name in v_status_inflicting_attacks:
        cur_move = v_status_inflicting_attacks[attack_name]
        if i is None:
            i = random.randint(1, 100)

        if i <= cur_move[1]:
            if cur_move[0] == "user":
                effected_pokemon = attacker
            else:
                effected_pokemon = defender
            effected_pokemon.set_v_status(cur_move[2])


def apply_leftovers(pokemon):
    """Heals the user's HP at the end of the turn by 1/16 of it's max HP if holding leftovers."""
    if (
        pokemon.item == "Leftovers"
        and pokemon.stat["hp"] != pokemon.stat["max_hp"]
        and pokemon.status[0] != "Fainted"
    ):
        pokemon.heal(0.0625)
        print(f"{pokemon.name} healed some of it's HP with it's leftovers.")
        print()


def apply_burn(pokemon):
    """Damages a burned pokemon by 1/16 of its max HP. Fire type pokemon cannot be burned."""
    if pokemon.status[0] == "Burned":
        print(f"{pokemon.name} was damaged by its burn!")
        print()
        pokemon.apply_damage_percentage(0.0625)


def apply_bad_poison(pokemon):
    """Damages a baldy poison pokemon with increasingly higher damage at the end of every turn. Initially deals 1/16 of max HP
    but adds an addition 1/16 damage (up until 15 * floor(max hp/16)) every turn the pokemon is in. If the pokemon switches out,
    the damage resets to the original 1/16 of max HP."""
    if pokemon.status[0] == "Badly Poisoned":
        print(f"{pokemon.name} was hurt by the poison!")
        print()
        pokemon.apply_damage_percentage(0.0625 * (15 - pokemon.status[1]))


# TODO: Recoil
def apply_recoil(pokemon):
    pass
