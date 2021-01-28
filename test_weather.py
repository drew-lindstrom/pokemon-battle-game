from pokemon import Pokemon
from weather import Weather
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
