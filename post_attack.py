from pokemon import Pokemon


def leftovers_check(pokemon):
    """Heals the user's HP at the end of the turn by 1/16 of it's max HP if holding leftovers."""
    if pokemon.item == "Leftovers":
        pokemon.heal(0.0625)
        print(f"{pokemon.name} healed some of it's HP with it's leftovers.")
