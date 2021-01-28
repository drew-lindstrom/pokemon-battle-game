from pokemon import Pokemon
from weather import Weather, sandstorm_damage
import pytest


class Test_Weather:
    def test_set_weather(self):
        weather = Weather()
        weather.set_weather("Rain", 5)
        assert weather.current_weather == "Rain"
        assert weather.weather_counter == 5

    def test_clear_weather(self):
        weather = Weather()
        weather.set_weather("Rain", 5)
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
        tyranitar = Pokemon(
            "Tyranitar",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        torterra = Pokemon(
            "Torterra",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        metagross = Pokemon(
            "Metagross",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        pikachu = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            "Safety Goggles",
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        assert sandstorm_damage(weather, slowbro) == True
        assert sandstorm_damage(weather, tyranitar) == False
        assert sandstorm_damage(weather, torterra) == False
        assert sandstorm_damage(weather, metagross) == False
        assert sandstorm_damage(weather, pikachu) == False