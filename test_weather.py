from pokemon import Pokemon
from weather import Weather, sandstorm_damage
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

    def test_sandstorm_damage(self):
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
        assert sandstorm_damage(weather, slowbro) == True
        slowbro.ability = "Sand Force"
        assert sandstorm_damage(weather, slowbro) == False
        slowbro.ability = "Sand Rush"
        assert sandstorm_damage(weather, slowbro) == False
        slowbro.ability = "Sand Veil"
        assert sandstorm_damage(weather, slowbro) == False
        slowbro.ability = "Magic Guard"
        assert sandstorm_damage(weather, slowbro) == False
        slowbro.ability = "Overcoat"
        assert sandstorm_damage(weather, slowbro) == False
        slowbro.ability = None
        assert sandstorm_damage(weather, slowbro) == True
        slowbro.typing = ["Ground", "Grass"]
        assert sandstorm_damage(weather, slowbro) == False
        slowbro.typing = ["Steel"]
        assert sandstorm_damage(weather, slowbro) == False
        slowbro.typing = ["Water", "Rock"]
        assert sandstorm_damage(weather, slowbro) == False
        slowbro.typing = ["Water", "Psychic"]
        slowbro.item = "Safety Goggles"
        assert sandstorm_damage(weather, slowbro) == False
