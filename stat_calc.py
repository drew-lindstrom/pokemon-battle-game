from pokemon import Pokemon

# TODO: If critical hit, ignores negative attack modifiers, positive defense modifiers, and defensive boosts from auroa veil, light screen, and reflect
# TODO: Add in light screen, reflect, and aurora veil
def calc_attack(cur_pokemon, stat, crit):
    """Calculates the attack stat of the given pokemon by calculating its modified attack stat and mulitplying it with any additional modifiers.
    If the given attack roled a critical hit, a negative attack stat_mod is ignored and calc_modified_stat is not called.
    Additional modifiers are still applied."""
    additional_modifier = 1

    if cur_pokemon.item == "Choice Band":
        additional_modifier *= 1.5
    if cur_pokemon.status == "Burn":
        additional_modifier *= 0.5

    if crit == True and cur_pokemon.stat_mod["attack"] < 0:
        return pokemon.stat["attack"] * additional_modifier
    return pokemon.calc_modified_stat["attack"] * additional_modifier


def calc_defense(attacker, stat, crit):
    additional_modifier = 1
    return pokemon.calc_modified_stat["defense"] * additional_modifier


def calc_sp_attack(attacker, stat, crit):
    additional_modifier = 1
    if pokemon.item == "Choice Spec":
        additional_modifier *= 1.5

    return pokemon.calc_modified_stat["sp_attack"] * additional_modifier


def calc_sp_defense(attacker, stat, crit):
    additional_modifier = 1

    return pokemon.calc_modified_stat["sp_defense"] * additional_modifier


def calc_speed(attacker, stat, crit):
    additional_modifier = 1
    if pokemon.item == "Choice Scarf":
        additional_modifier *= 1.5

    return pokemon.calc_modified_stat["speed"] * additional_modifier


def calc_accuracy(attacker, stat, crit):
    additional_modifier


def calc_evasion(attacker, stat, crit):
    pass