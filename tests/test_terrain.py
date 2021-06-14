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

    @pytest.mark.parametrize(
        "terrain_name_1,terrain_name_2,item,expected_terrain,expected_int",
        [
            (None, "Psychic Terrain", None, "Psychic Terrain", 4),
            ("Psychic Terrain", "Grassy Terrain", None, "Psychic Terrain", 4),
            (None, "Grassy Terrain", "Terrain Extender", "Grassy Terrain", 7),
        ],
    )
    def test_set_terrain(
        self,
        test_pokemon,
        terrain_name_1,
        terrain_name_2,
        item,
        expected_terrain,
        expected_int,
    ):
        slowbro = test_pokemon
        terrain = Terrain()
        slowbro.item = item
        terrain.set_terrain(terrain_name_1, slowbro)
        terrain.set_terrain(terrain_name_2, slowbro)
        terrain.set_terrain("Psychic Terrain", slowbro)
        assert terrain.current_terrain == expected_terrain
        assert terrain.counter == expected_int

    @pytest.mark.parametrize(
        "terrain_name,counter,expected_terrain,expected_int",
        [("Psychic Terrain", 4, "Psychic Terrain", 3), ("Psychic Terrain", 0, None, 0)],
    )
    def test_decrement_terrain(
        self, test_pokemon, terrain_name, counter, expected_terrain, expected_int
    ):
        slowbro = test_pokemon
        terrain = Terrain()
        terrain.set_terrain(terrain_name, slowbro)
        terrain.counter = counter
        terrain.decrement_terrain()
        assert terrain.current_terrain == expected_terrain
        assert terrain.counter == expected_int

    @pytest.mark.parametrize(
        "terrain_name,counter,expected_terrain",
        [
            ("Psychic Terrain", 3, None),
        ],
    )
    def test_clear_terrain(self, test_pokemon, terrain_name, counter, expected_terrain):
        slowbro = test_pokemon
        terrain = Terrain()
        terrain.set_terrain(terrain_name, slowbro)
        terrain.counter = counter
        terrain.clear_terrain()
        assert terrain.current_terrain == expected_terrain

    @pytest.mark.parametrize(
        "move_type,terrain_name,expected_int",
        [
            ("Electric", "Electric Terrain", 1.3),
            ("Grass", "Electric Terrain", 1),
            ("Grass", "Grassy Terrain", 1.3),
            ("Dragon", "Grassy Terrain", 1),
            ("Dragon", "Misty Terrain", 0.5),
            ("Psychic", "Misty Terrain", 1),
            ("Psychic", "Psychic Terrain", 1.3),
            ("Electric", "Psychic Terrain", 1),
        ],
    )
    def test_check_damage_mod_from_terrain(
        self, test_pokemon, move_type, terrain_name, expected_int
    ):
        slowbro = test_pokemon
        slowbro.moves[0].type = move_type
        terrain = Terrain()
        terrain.current_terrain = terrain_name
        assert check_damage_mod_from_terrain(terrain, slowbro, 0) == expected_int

    @pytest.mark.parametrize(
        "hp,terrain_name,grounded_bool,expected_int",
        [(100, "Grassy Terrain", True, 124), (100, "Grassy Terrain", False, 100)],
    )
    def test_heal_from_grassy_terrain(
        self, test_pokemon, hp, terrain_name, grounded_bool, expected_int
    ):
        slowbro = test_pokemon
        t = Terrain()
        t.current_terrain = terrain_name
        slowbro.stat["hp"] = hp
        slowbro.grounded = grounded_bool
        heal_from_grassy_terrain(t, slowbro)
        assert slowbro.stat["hp"] == expected_int
