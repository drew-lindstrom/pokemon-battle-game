from pokemon import Pokemon
from terrain import Terrain, check_damage_mod_from_terrain, heal_from_grassy_terrain
import pytest


class Test_Terrain:
    @pytest.fixture
    def test_pokemon(self):
        test_pokemon = Pokemon(
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

        return test_pokemon

    def test_set_terrain(self, test_pokemon):
        slowbro = test_pokemon
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

    def test_decrement_terrain(self, test_pokemon):
        slowbro = test_pokemon
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

    def test_clear_terrain(self, test_pokemon):
        slowbro = test_pokemon
        terrain = Terrain()
        terrain.set_terrain("Psychic Terrain", slowbro)
        assert terrain.current_terrain == "Psychic Terrain"
        terrain.clear_terrain()
        terrain.terrain_counter = 0
        terrain.clear_terrain()
        assert terrain.current_terrain == None

    def test_check_damage_mod_from_terrain(self, test_pokemon):
        slowbro = test_pokemon
        slowbro.moves[0].type = "Electric"
        slowbro.moves[1].type = "Grass"
        slowbro.moves[2].type = "Dragon"
        slowbro.moves[3].type = "Psychic"
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

    def test_heal_from_grassy_terrain(self, test_pokemon):
        slowbro = test_pokemon
        t = Terrain()
        slowbro.stat["hp"] = 100
        heal_from_grassy_terrain(t, slowbro)
        assert slowbro.stat["hp"] == 100
        t.current_terrain = "Grassy Terrain"
        heal_from_grassy_terrain(t, slowbro)
        assert slowbro.stat["hp"] == 124
        slowbro.grounded = False
        heal_from_grassy_terrain(t, slowbro)
        assert slowbro.stat["hp"] == 124