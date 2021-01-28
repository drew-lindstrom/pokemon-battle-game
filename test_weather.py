from pokemon import Pokemon
import weather
import pytest


class Test_Weather:
    def test_set_weather(self):
        weather.set_weather("Rain", 5)
        assert weather.current_weather == "Rain"
        assert weather.weather_counter == 5