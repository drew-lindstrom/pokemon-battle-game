from pokemon import Pokemon
from terrain import Terrain, check_damage_mod_from_terrain
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
        assert terrain.counter == 4
        slowbro.item = "Terrain Extender"
        terrain.set_terrain("Grassy Terrain", slowbro)
        assert terrain.current_terrain == "Psychic Terrain"
        assert terrain.counter == 4
        terrain = Terrain()
        terrain.set_terrain("Grassy Terrain", slowbro)
        assert terrain.current_terrain == "Grassy Terrain"
        assert terrain.counter == 7

    def test_decrement_terrain(self):
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
        assert terrain.current_terrain == "Psychic Terrain"
        assert terrain.counter == 4
        terrain.decrement_terrain()
        assert terrain.counter == 3
        terrain.counter = 0
        terrain.decrement_terrain()
        assert terrain.current_terrain is None
        assert terrain.counter == 0

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
        assert terrain.current_terrain == "Psychic Terrain"
        terrain.clear_terrain()
        terrain.terrain_counter = 0
        terrain.clear_terrain()
        assert terrain.current_terrain == None

    def test_check_damage_mod_from_terrain(self):
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
        assert check_damage_mod_from_terrain(terrain, slowbro, 0) == 1.3
        assert check_damage_mod_from_terrain(terrain, slowbro, 1) == 1
        terrain.current_terrain = "Grassy Terrain"
        assert check_damage_mod_from_terrain(terrain, slowbro, 1) == 1.3
        assert check_damage_mod_from_terrain(terrain, slowbro, 2) == 1
        terrain.current_terrain = "Misty Terrain"
        assert check_damage_mod_from_terrain(terrain, slowbro, 2) == 0.5
        assert check_damage_mod_from_terrain(terrain, slowbro, 3) == 1
        terrain.current_terrain = "Psychic Terrain"
        assert check_damage_mod_from_terrain(terrain, slowbro, 3) == 1.3
        assert check_damage_mod_from_terrain(terrain, slowbro, 0) == 1