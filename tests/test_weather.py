from pokemon import Pokemon
from weather import (
    Weather,
    weather_damage,
    check_sandstorm_sp_def_boost,
    weather_move_damage_mod,
)
import pytest


class Test_Weather:
    def test_set_weather(self):
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
        weather = Weather()
        weather.set_weather("Rain", slowbro)
        assert weather.current_weather == "Rain"
        assert weather.weather_counter == 5
        weather.set_weather("Harsh Sunlight", slowbro)
        assert weather.current_weather == "Harsh Sunlight"
        assert weather.weather_counter == 8

    def test_clear_weather(self):
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
        weather = Weather()
        weather.set_weather("Rain", slowbro)
        weather.clear_weather()
        assert weather.current_weather == "Rain"
        weather.weather_counter = 0
        weather.clear_weather()
        assert weather.current_weather == "Clear Skies"

    def test_weather_damage(self):
        weather = Weather("Sandstorm", 5)
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
        assert weather_damage(weather, slowbro) == True
        slowbro.ability = "Sand Force"
        assert weather_damage(weather, slowbro) == False
        slowbro.ability = "Sand Rush"
        assert weather_damage(weather, slowbro) == False
        slowbro.ability = "Sand Veil"
        assert weather_damage(weather, slowbro) == False
        slowbro.ability = "Magic Guard"
        assert weather_damage(weather, slowbro) == False
        slowbro.ability = "Overcoat"
        assert weather_damage(weather, slowbro) == False
        slowbro.ability = None
        assert weather_damage(weather, slowbro) == True
        slowbro.typing = ["Ground", "Grass"]
        assert weather_damage(weather, slowbro) == False
        slowbro.typing = ["Steel"]
        assert weather_damage(weather, slowbro) == False
        slowbro.typing = ["Water", "Rock"]
        assert weather_damage(weather, slowbro) == False
        slowbro.typing = ["Water", "Psychic"]
        slowbro.item = "Safety Goggles"
        assert weather_damage(weather, slowbro) == False

        weather = Weather("Hail", 5)
        slowbro.typing = ["Grass", "Ice"]
        assert weather_damage(weather, slowbro) == False
        weather = Weather("Rain", 5)
        assert weather_damage(weather, slowbro) == False

    def test_check_sandstorm_sp_def_boost(self):
        weather = Weather("Sandstorm", 5)
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
        assert check_sandstorm_sp_def_boost(weather, slowbro) == 1
        slowbro.typing = ["Rock", "Fire"]
        assert check_sandstorm_sp_def_boost(weather, slowbro) == 1.5
        slowbro.typing = ["Dark", "Rock"]
        assert check_sandstorm_sp_def_boost(weather, slowbro) == 1.5

    def test_weather_move_damage_mod(self):
        weather = Weather("Harsh Sunlight", 5)
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Fire Blast", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        assert weather_move_damage_mod(weather, slowbro, 0) == 0.5
        assert weather_move_damage_mod(weather, slowbro, 1) == 1.5
        weather.current_weather = "Rain"
        assert weather_move_damage_mod(weather, slowbro, 0) == 1.5
        assert weather_move_damage_mod(weather, slowbro, 1) == 0.5