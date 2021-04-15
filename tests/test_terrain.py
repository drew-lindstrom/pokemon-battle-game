from pokemon import Pokemon
from terrain import Terrain, terrain_move_damage_mod
import pytest


class Test_Terrain:
    def test_set_terrain(self):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        terrain = Terrain()
        terrain.set_terrain("Psychic Terrain", slowbro)
        assert terrain.current_terrain == "Psychic Terrain"
        assert terrain.terrain_counter == 5
        slowbro.item = "Terrain Extender"
        terrain.set_terrain("Grassy Terrain", slowbro)
        assert terrain.current_terrain == "Grassy Terrain"
        assert terrain.terrain_counter == 8

    def test_clear_terrain(self):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            "Heat Rock",
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        terrain = Terrain()
        terrain.set_terrain("Psychic Terrain", slowbro)
        terrain.clear_terrain()
        assert terrain.current_terrain == "Psychic Terrain"
        terrain.terrain_counter = 0
        terrain.clear_terrain()
        assert terrain.current_terrain == None

    def test_terrain_move_damage_mod(self):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Thunder", "Vine Whip", "Dragon Pulse", "Psychic"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        terrain = Terrain()
        terrain.current_terrain = "Electric Terrain"
        assert terrain_move_damage_mod(terrain, slowbro, 0) == 1.3
        assert terrain_move_damage_mod(terrain, slowbro, 1) == 1
        terrain.current_terrain = "Grassy Terrain"
        assert terrain_move_damage_mod(terrain, slowbro, 1) == 1.3
        assert terrain_move_damage_mod(terrain, slowbro, 2) == 1
        terrain.current_terrain = "Misty Terrain"
        assert terrain_move_damage_mod(terrain, slowbro, 2) == 0.5
        assert terrain_move_damage_mod(terrain, slowbro, 3) == 1
        terrain.current_terrain = "Psychic Terrain"
        assert terrain_move_damage_mod(terrain, slowbro, 3) == 1.3
        assert terrain_move_damage_mod(terrain, slowbro, 0) == 1