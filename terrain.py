from pokemon import Pokemon


class Terrain:
    def __init__(self, terrain=None, counter=None):
        self.current_terrain = terrain
        self.terrain_counter = counter

    def set_terrain(self, terrain, pokemon):
        """Sets current_terrain to the specified terrain and terrain_counter to 5 turns (or 8 turns if pokemon is holding Terrain Extender)."""
        assert terrain in (
            "Electric Terrain",
            "Grassy Terrain",
            "Misty Terrain",
            "Psychic Terrain",
        )
        self.current_terrain = terrain
        print(f"{terrain} has been activated!")
        if pokemon.item == "Terrain Extender":
            self.terrain_counter = 8
        else:
            self.terrain_counter = 5

    def clear_terrain(self):
        """Checks the terrain counter at the end of the turn and resets terrain_weather to None if 0."""
        # TODO does making terrain reset at 0 cause the terrain to last for 6/9 turns?
        if self.terrain_counter == 0:
            print(f"The {self.current_terrain} ended.")
            self.current_terrain = None


cur_terrain = Terrain()

# TODO: Terrain counterdowner
# TODO: What happens if pokemon uses terrain move with terrain is already present, does the counter reset?
# TODO: Remove weather function
# TODO: Terrain only effects pokemon on the ground, need to apply this.

# TODO: Electric terrian prevents pokemon from being afflicted by Sleep or Yawn
# TODO: Grassy terrain restores affected pkoemon by 1/16 of max HP
# TODO: Grassy terrain: unless a pokemon is in a semi-vulnerable state of dig or dive, power of bulldoze, earthquake, and magnitude is halved (even if the user is not grounded)
# TODO: Misty terrain prevents non-volatile status conditions and confusion
# TODO: Psychic terrain immunizes affected pokemon from opponents' moves with increased priority (including moves boosted by Prankster, Gale Wings, and Triage).


def terrain_move_damage_mod(terrain, pokemon, n):
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