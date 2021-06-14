from pokemon import Pokemon
from terrain import Terrain
from weather import Weather
import switch_effects
import pytest


class TestSwitchEffects:
    @pytest.fixture
    def test_pokemon(self):
        tyranitar = Pokemon(
            "Tyranitar",
            100,
            "Male",
            ("Crunch", "Stealth Rock", "Toxic", "Earthquake"),
            "Sand Stream",
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 0, 0, 216, 40),
            "Careful",
        )
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            "Regenerator",
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        return tyranitar, slowbro

    def test_activate_grassy_surge(self, test_pokemon):
        tyranitar, slowbro = test_pokemon
        tyranitar.ability = "Grassy Surge"
        terrain = Terrain()
        assert terrain.current_terrain == None
        switch_effects.activate_grassy_surge(tyranitar, terrain)
        assert terrain.current_terrain == "Grassy Terrain"

    def test_activate_intimidate(self, test_pokemon):
        tyranitar, slowbro = test_pokemon
        slowbro.ability = "Intimidate"
        switch_effects.activate_intimidate(slowbro, tyranitar)
        assert tyranitar.stat_mod["attack"] == -1

    @pytest.mark.parametrize("input_hp,expected_hp", [(100, 231), (0, 0)])
    def test_activate_regenerator(self, test_pokemon, input_hp, expected_hp):
        tyranitar, slowbro = test_pokemon
        slowbro.stat["hp"] = input_hp
        switch_effects.activate_regenerator(slowbro)
        assert slowbro.stat["hp"] == expected_hp

    def test_activate_psychic_surge(self, test_pokemon):
        tyranitar, slowbro = test_pokemon
        tyranitar.ability = "Psychic Surge"
        terrain = Terrain()
        assert terrain.current_terrain == None
        switch_effects.activate_psychic_surge(tyranitar, terrain)
        assert terrain.current_terrain == "Psychic Terrain"

    def test_activate_sand_stream(self, test_pokemon):
        tyranitar, slowbro = test_pokemon
        weather = Weather()
        assert weather.current_weather == "Clear Skies"
        switch_effects.activate_sand_stream(tyranitar, weather)
        assert weather.current_weather == "Sandstorm"