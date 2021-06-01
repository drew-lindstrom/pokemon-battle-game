from pokemon import Pokemon
from player import Player
import weather


def calc_attack(team, crit, cur_weather="Clear Skies"):
    """Calculates the attack stat of the given pokemon by calculating its modified attack stat and mulitplying it with any additional modifiers.
    If the given attack roled a critical hit, a negative attack stat_mod is ignored and calc_modified_stat is not called.
    Additional modifiers are still applied."""
    cur_pokemon = team.cur_pokemon
    additional_modifier = 1

    if cur_pokemon.item == "Choice Band":
        additional_modifier *= 1.5
    if cur_pokemon.status == "Burn":
        additional_modifier *= 0.5

    if crit == True and cur_pokemon.stat_mod["attack"] < 0:
        return int(cur_pokemon.stat["attack"] * additional_modifier)
    return int(cur_pokemon.calc_modified_stat("attack") * additional_modifier)


def calc_defense(team, crit, cur_weather="Clear Skies"):
    """Calculates the defense stat of the given pokemon by calculating its modified defense stat and mulitplying it with any additional modifiers.
    If the given attack roled a critical hit, a positive defense stat_mod is ignored and calc_modified_stat is not called.
    Additional modifiers are still applied."""
    cur_pokemon = team.cur_pokemon
    additional_modifier = 1

    if crit == True and cur_pokemon.stat_mod["defense"] > 0:
        return int(cur_pokemon.stat["defense"] * additional_modifier)
    return int(cur_pokemon.calc_modified_stat("defense") * additional_modifier)


def calc_sp_attack(team, crit, cur_weather="Clear Skies"):
    """Calculates the special attack stat of the given pokemon by calculating its modified sp_attack stat and mulitplying it with any additional modifiers.
    If the given attack roled a critical hit, a negative sp_attack stat_mod is ignored and calc_modified_stat is not called.
    Additional modifiers are still applied."""
    cur_pokemon = team.cur_pokemon
    additional_modifier = 1
    if cur_pokemon.item == "Choice Spec":
        additional_modifier *= 1.5
    if crit == True and cur_pokemon.stat_mod["sp_attack"] < 0:
        return int(cur_pokemon.stat["sp_attack"] * additional_modifier)
    return int(cur_pokemon.calc_modified_stat("sp_attack") * additional_modifier)


def calc_sp_defense(team, crit, cur_weather="Clear Skies"):
    """Calculates the special defense stat of the given pokemon by calculating its modified sp_defense stat and mulitplying it with any additional modifiers.
    If the given attack roled a critical hit, a positive sp_defense stat_mod is ignored and calc_modified_stat is not called.
    Additional modifiers are still applied."""
    cur_pokemon = team.cur_pokemon
    additional_modifier = 1
    additional_modifier *= weather.check_sandstorm_sp_def_boost(
        cur_weather, cur_pokemon
    )

    if crit == True and cur_pokemon.stat_mod["sp_defense"] > 0:
        return int(cur_pokemon.stat["sp_defense"] * additional_modifier)
    return int(cur_pokemon.calc_modified_stat("sp_defense") * additional_modifier)


def calc_speed(team, crit=False, cur_weather="Clear Skies"):
    """Calculates the speed stat of the given pokemon by calculating its modified speed stat and mulitplying it with any additional modifiers."""
    cur_pokemon = team.cur_pokemon
    additional_modifier = 1
    if cur_pokemon.item == "Choice Scarf":
        additional_modifier *= 1.5
    if cur_pokemon.status and cur_pokemon.status[0] == "Paralyzed":
        additional_modifier *= 0.5
    if cur_pokemon.ability == "Sand Rush" and cur_weather == "Sandstorm":
        additional_modifier *= 2

    return int(cur_pokemon.calc_modified_stat("speed") * additional_modifier)


# def calc_accuracy(team, crit=False, cur_weather="Clear Skies"):
#     """Calculates the accuracy percentage of the given pokemon by calculating its modified accuaracy and multiplying it with any additional modifiers."""
#     cur_pokemon = team.cur_pokemon
#     additional_modifier = 1
#     return int(cur_pokemon.calc_modified_stat("accuracy") * additional_modifier)


# def calc_evasion(team, crit=False, cur_weather="Clear Skies"):
#     """Calculates the evasion percentage of the give pokemon by calculating its modified evasion and multiplying it with any additional modifiers."""
#     cur_pokemon = team.cur_pokemon
#     additional_modifier = 1
#     return int(cur_pokemon.calc_modified_stat("evasion") * additional_modifier)
