from pokemon import Pokemon


def leftovers_check(pokemon):
    if pokemon.item == "Leftovers":
        pokemon.heal(0.0625)
        print(f"{pokemon.name} healed some of it's HP with it's leftovers.")
