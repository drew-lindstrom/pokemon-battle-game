from pokemon import Pokemon
from player import Player
from frame import Frame
import weather


def calc_attack(frame):
    """Calculates the attack stat of the given pokemon by calculating its modified attack stat and mulitplying it with any additional modifiers.
    If the given attack roled a critical hit, a negative attack stat_mod is ignored and calc_modified_stat is not called.
    Additional modifiers are still applied."""
    additional_modifier = 1

    if frame.user.item == "Choice Band":
        additional_modifier *= 1.5
    if frame.user.ability == "Blaze":
        additional_modifier *= check_blaze(frame)
    if frame.crit == True and frame.user.stat_mod["attack"] < 0:
        return int(frame.user.stat["attack"] * additional_modifier)
    return int(frame.user.calc_modified_stat("attack") * additional_modifier)


def calc_defense(frame):
    """Calculates the defense stat of the given pokemon by calculating its modified defense stat and mulitplying it with any additional modifiers.
    If the given attack roled a critical hit, a positive defense stat_mod is ignored and calc_modified_stat is not called.
    Additional modifiers are still applied."""
    additional_modifier = 1

    if frame.crit == True and frame.target.stat_mod["defense"] > 0:
        return int(frame.target.stat["defense"] * additional_modifier)
    return int(frame.target.calc_modified_stat("defense") * additional_modifier)


def calc_sp_attack(frame):
    """Calculates the special attack stat of the given pokemon by calculating its modified sp_attack stat and mulitplying it with any additional modifiers.
    If the given attack roled a critical hit, a negative sp_attack stat_mod is ignored and calc_modified_stat is not called.
    Additional modifiers are still applied."""
    additional_modifier = 1
    if frame.user.item == "Choice Spec":
        additional_modifier *= 1.5
    if frame.user.ability == "Blaze":
        additional_modifier *= check_blaze(frame)
    if frame.crit == True and frame.user.stat_mod["sp_attack"] < 0:
        return int(frame.user.stat["sp_attack"] * additional_modifier)
    return int(frame.user.calc_modified_stat("sp_attack") * additional_modifier)


def calc_sp_defense(frame):
    """Calculates the special defense stat of the given pokemon by calculating its modified sp_defense stat and mulitplying it with any additional modifiers.
    If the given attack roled a critical hit, a positive sp_defense stat_mod is ignored and calc_modified_stat is not called.
    Additional modifiers are still applied."""
    additional_modifier = 1
    additional_modifier *= weather.check_sandstorm_sp_def_boost(
        frame.weather, frame.user
    )

    if frame.crit == True and frame.target.stat_mod["sp_defense"] > 0:
        return int(frame.target.stat["sp_defense"] * additional_modifier)
    return int(frame.target.calc_modified_stat("sp_defense") * additional_modifier)


def calc_speed(frame):
    """Calculates the speed stat of the given pokemon by calculating its modified speed stat and mulitplying it with any additional modifiers."""
    additional_modifier = 1
    if frame.user.item == "Choice Scarf":
        additional_modifier *= 1.5
    if frame.user.status and frame.user.status[0] == "Paralyzed":
        additional_modifier *= 0.5
    if (
        frame.user.ability == "Sand Rush"
        and frame.weather.current_weather == "Sandstorm"
    ):
        additional_modifier *= 2

    return int(frame.user.calc_modified_stat("speed") * additional_modifier)


def check_blaze(frame):
    """Returns 1.5 is user is using a fire type move and user's hp is below 1/3 of their max hp."""
    if (
        frame.attack.type == "Fire"
        and frame.user.stat["hp"] < frame.user.stat["max_hp"] // 3
    ):
        return 1.5
    return 1


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
