from pokemon import Pokemon
from weather import (
    Weather,
    apply_weather_damage,
    check_sandstorm_sp_def_boost,
    check_damage_mod_from_weather,
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
        assert weather.counter == 4
        weather.set_weather("Harsh Sunlight", slowbro)
        assert weather.current_weather == "Rain"
        assert weather.counter == 4
        weather = Weather()
        weather.set_weather("Harsh Sunlight", slowbro)
        assert weather.current_weather == "Harsh Sunlight"
        assert weather.counter == 7

    def test_decrement_weather(self):
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
        weather.decrement_weather()
        assert weather.current_weather == "Rain"
        assert weather.counter == 3
        weather.counter = 0
        weather.decrement_weather()
        assert weather.current_weather == "Clear Skies"
        assert weather.counter == 0

    def test_clear_weather(self):
        weather = Weather()
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
        weather.set_weather("Harsh Sunlight", slowbro)
        assert weather.current_weather == "Harsh Sunlight"
        assert weather.counter == 7
        weather.clear_weather()
        assert weather.current_weather == "Clear Skies"
        assert weather.counter == 0

    def test_apply_weather_damage(self):
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
        assert apply_weather_damage(weather, slowbro) == True
        slowbro.ability = "Sand Force"
        assert apply_weather_damage(weather, slowbro) == False
        slowbro.ability = "Sand Rush"
        assert apply_weather_damage(weather, slowbro) == False
        slowbro.ability = "Sand Veil"
        assert apply_weather_damage(weather, slowbro) == False
        slowbro.ability = "Magic Guard"
        assert apply_weather_damage(weather, slowbro) == False
        slowbro.ability = "Overcoat"
        assert apply_weather_damage(weather, slowbro) == False
        slowbro.ability = None
        assert apply_weather_damage(weather, slowbro) == True
        slowbro.typing = ["Ground", "Grass"]
        assert apply_weather_damage(weather, slowbro) == False
        slowbro.typing = ["Steel"]
        assert apply_weather_damage(weather, slowbro) == False
        slowbro.typing = ["Water", "Rock"]
        assert apply_weather_damage(weather, slowbro) == False
        slowbro.typing = ["Water", "Psychic"]
        slowbro.item = "Safety Goggles"
        assert apply_weather_damage(weather, slowbro) == False

        weather = Weather("Hail", 5)
        slowbro.typing = ["Grass", "Ice"]
        assert apply_weather_damage(weather, slowbro) == False
        weather = Weather("Rain", 5)
        assert apply_weather_damage(weather, slowbro) == False

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

    def test_check_damage_mod_from_weather(self):
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
        assert check_damage_mod_from_weather(weather, slowbro, 0) == 0.5
        assert check_damage_mod_from_weather(weather, slowbro, 1) == 1.5
        weather.current_weather = "Rain"
        assert check_damage_mod_from_weather(weather, slowbro, 0) == 1.5
        assert check_damage_mod_from_weather(weather, slowbro, 1) == 0.5