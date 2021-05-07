from pokemon import Pokemon


class Terrain:
    def __init__(self, terrain=None, counter=0):
        self.current_terrain = terrain
        self.counter = counter

    def set_terrain(self, terrain_name, pokemon):
        """Sets current_terrain to the specified terrain and terrain_counter to 5 turns (or 8 turns if pokemon is holding Terrain Extender)."""
        if self.current_terrain is None:
            self.current_terrain = terrain_name
            print(f"{terrain_name} has been activated!")
            if pokemon.item == "Terrain Extender":
                self.counter = 7
            else:
                self.counter = 4

    def decrement_terrain(self):
        """Decrements the terrain counter by one at the end of each turn. If the counter equals 0, clear_terrain() is called."""
        if self.current_terrain is not None:
            if self.counter == 0:
                print(f"The {self.current_terrain.lower()} subsided.")
                self.clear_terrain()
            else:
                self.counter -= 1

    def clear_terrain(self):
        """Resets terrain to None and resets counter to 0."""
        self.current_terrain = None
        self.counter = 0


# TODO: Electric terrian prevents pokemon from being afflicted by Sleep or Yawn
# TODO: Grassy terrain restores affected pkoemon by 1/16 of max HP
# TODO: Grassy terrain: unless a pokemon is in a semi-vulnerable state of dig or dive, power of bulldoze, earthquake, and magnitude is halved (even if the user is not grounded)
# TODO: Misty terrain prevents non-volatile status conditions and confusion
# TODO: Psychic terrain immunizes affected pokemon from opponents' moves with increased priority (including moves boosted by Prankster, Gale Wings, and Triage).


def check_damage_mod_from_terrain(terrain, pokemon, n):
    if (
        (
            terrain.current_terrain == "Electric Terrain"
            and pokemon.moves[n].type == "Electric"
        )
        or (
            terrain.current_terrain == "Grassy Terrain"
            and pokemon.moves[n].type == "Grass"
        )
        or (
            terrain.current_terrain == "Psychic Terrain"
            and pokemon.moves[n].type == "Psychic"
        )
    ):
        return 1.3
    if terrain.current_terrain == "Misty Terrain" and pokemon.moves[n].type == "Dragon":
        return 0.5
    else:
        return 1


def heal_from_grassy_terrain(terrain, pokemon):
    """If the current terrain is Grassy Terrain and the pokemon is grounded, heals for 1/16 max HP at the end of the turn."""
    if terrain.current_terrain == "Grassy Terrain" and pokemon.grounded == True:
        pokemon.heal(0.0625)