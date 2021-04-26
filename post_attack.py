from pokemon import Pokemon


def apply_leftovers(pokemon):
    """Heals the user's HP at the end of the turn by 1/16 of it's max HP if holding leftovers."""
    if pokemon.item == "Leftovers":
        pokemon.heal(0.0625)
        print(f"{pokemon.name} healed some of it's HP with it's leftovers.")


def apply_burn(pokemon):
    """Damages a burned pokemon by 1/16 of its max HP. Fire type pokemon cannot be burned."""
    if pokemon.status[0] == "Burned":
        print(f"{pokemon.name} was damaged by its burn!")
        pokemon.damage(0.0625)


def apply_bad_poison(pokemon):
    """Damages a baldy poison pokemon with increasingly higher damage at the end of every turn. Initially deals 1/16 of max HP
    but adds an addition 1/16 damage (up until 15 * floor(max hp/16)) every turn the pokemon is in. If the pokemon switches out,
    the damage resets to the original 1/16 of max HP."""
    if pokemon.status[0] == "Baldly Poisoned":
        print(f"{pokemon.name} was hurt by the poison!")
        if pokemon.status[1] >= 14:
            pokemon.damage(0.0625 * 15)
        else:
            pokemon.damage(0.0625 * (pokemon.status[1] + 1))