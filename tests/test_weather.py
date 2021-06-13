from pokemon import Pokemon
from weather import (
    Weather,
    apply_weather_damage,
    check_sandstorm_sp_def_boost,
    check_damage_mod_from_weather,
)
import pytest


class Test_Weather:
    @pytest.fixture
    def test_pokemon(self):
        test_pokemon = Pokemon(
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
        return test_pokemon

    @pytest.mark.parametrize(
        "weather_name_1,weather_name_2,expected_weather,weather_counter",
        [
            ("Clear Skies", "Rain", "Rain", 4),
            ("Rain", "Harsh Sunlight", "Rain", 4),
            ("Clear Skies", "Harsh Sunlight", "Harsh Sunlight", 7),
        ],
    )
    def test_set_weather(
        self,
        test_pokemon,
        weather_name_1,
        weather_name_2,
        expected_weather,
        weather_counter,
    ):
        slowbro = test_pokemon
        weather = Weather()
        weather.set_weather(weather_name_1, slowbro)
        weather.set_weather(weather_name_2, slowbro)
        assert weather.current_weather == expected_weather
        assert weather.counter == weather_counter

    @pytest.mark.parametrize(
        "weather_name,weather_counter,expected_weather,expected_weather_counter",
        [
            ("Rain", 4, "Rain", 3),
            ("Rain", 0, "Clear Skies", 0),
        ],
    )
    def test_decrement_weather(
        self,
        test_pokemon,
        weather_name,
        weather_counter,
        expected_weather,
        expected_weather_counter,
    ):
        slowbro = test_pokemon
        weather = Weather()
        weather.set_weather(weather_name, slowbro)
        weather.counter = weather_counter
        weather.decrement_weather()
        assert weather.current_weather == expected_weather
        assert weather.counter == expected_weather_counter

    @pytest.mark.parametrize(
        "weather_name,expected_weather,expected_counter",
        [("Harsh Sunlight", "Clear Skies", 0)],
    )
    def test_clear_weather(
        self, test_pokemon, weather_name, expected_weather, expected_counter
    ):
        weather = Weather()
        slowbro = test_pokemon
        weather.set_weather(weather_name, slowbro)
        weather.clear_weather()
        assert weather.current_weather == expected_weather
        assert weather.counter == expected_counter

    @pytest.mark.parametrize(
        "weather_name,ability,item,typing,expected_bool",
        [
            ("Sandstorm", None, None, ["Water", "Psychic"], True),
            ("Sandstorm", "Sand Force", None, ["Water", "Psychic"], False),
            ("Sandstorm", "Sand Rush", None, ["Water", "Psychic"], False),
            ("Sandstorm", "Sand Veil", None, ["Water", "Psychic"], False),
            ("Sandstorm", "Magic Guard", None, ["Water", "Psychic"], False),
            ("Sandstorm", "Overcoat", None, ["Water", "Psychic"], False),
            ("Sandstorm", None, None, ["Ground", "Grass"], False),
            ("Sandstorm", None, None, ["Steel"], False),
            ("Sandstorm", None, None, ["Water", "Rock"], False),
            ("Sandstorm", None, "Safety Goggles", ["Water", "Psychic"], False),
            ("Hail", None, None, ["Grass", "Ice"], False),
            ("Rain", None, None, ["Steel"], False),
        ],
    )
    def test_apply_weather_damage(
        self, test_pokemon, weather_name, ability, item, typing, expected_bool
    ):
        weather = Weather(weather_name, 5)
        slowbro = test_pokemon
        slowbro.item = item
        slowbro.ability = ability
        slowbro.typing = typing
        assert apply_weather_damage(weather, slowbro) == expected_bool

    @pytest.mark.parametrize(
        "weather_name,typing,expected_int",
        [
            ("Sandstorm", ["Water", "Psychic"], 1),
            ("Sandstorm", ["Rock", "Fire"], 1.5),
            ("Sandstorm", ["Dark", "Rock"], 1.5),
        ],
    )
    def test_check_sandstorm_sp_def_boost(
        self, test_pokemon, weather_name, typing, expected_int
    ):
        weather = Weather(weather_name, 5)
        slowbro = test_pokemon
        slowbro.typing = typing
        assert check_sandstorm_sp_def_boost(weather, slowbro) == expected_int

    @pytest.mark.parametrize(
        "weather_name,move_type,expected_int",
        [
            ("Harsh Sunlight", "Water", 0.5),
            ("Harsh Sunlight", "Fire", 1.5),
            ("Rain", "Water", 1.5),
            ("Rain", "Fire", 0.5),
        ],
    )
    def test_check_damage_mod_from_weather(
        self, test_pokemon, weather_name, move_type, expected_int
    ):
        weather = Weather(weather_name, 5)
        slowbro = test_pokemon
        slowbro.moves[0].type = move_type
        assert check_damage_mod_from_weather(weather, slowbro, 0) == expected_int