from pokemon import Pokemon
from weather import (
    Weather,
    applyWeatherDamage,
    checkSandstormSpDefBoost,
    checkDamageModFromWeather,
)
import gameText
import pytest

gameText.output = []


class TestWeather:
    @pytest.fixture
    def testPokemon(self):
        testPokemon = Pokemon(
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
        return testPokemon

    @pytest.mark.parametrize(
        "weatherName1,weatherName2,expectedWeather,weatherCounter",
        [
            ("Clear Skies", "Rain", "Rain", 4),
            ("Rain", "Harsh Sunlight", "Rain", 4),
            ("Clear Skies", "Harsh Sunlight", "Harsh Sunlight", 7),
        ],
    )
    def testSetWeather(
        self,
        testPokemon,
        weatherName1,
        weatherName2,
        expectedWeather,
        weatherCounter,
    ):
        slowbro = testPokemon
        weather = Weather()
        weather.setWeather(weatherName1, slowbro)
        weather.setWeather(weatherName2, slowbro)
        assert weather.currentWeather == expectedWeather
        assert weather.counter == weatherCounter

    @pytest.mark.parametrize(
        "weatherName,weatherCounter,expectedWeather,expectedWeatherCounter",
        [
            ("Rain", 4, "Rain", 3),
            ("Rain", 0, "Clear Skies", 0),
        ],
    )
    def testDecrementWeather(
        self,
        testPokemon,
        weatherName,
        weatherCounter,
        expectedWeather,
        expectedWeatherCounter,
    ):
        slowbro = testPokemon
        weather = Weather()
        weather.setWeather(weatherName, slowbro)
        weather.counter = weatherCounter
        weather.decrementWeather()
        assert weather.currentWeather == expectedWeather
        assert weather.counter == expectedWeatherCounter

    @pytest.mark.parametrize(
        "weatherName,expectedWeather,expectedCounter",
        [("Harsh Sunlight", "Clear Skies", 0)],
    )
    def testClearWeather(
        self, testPokemon, weatherName, expectedWeather, expectedCounter
    ):
        weather = Weather()
        slowbro = testPokemon
        weather.setWeather(weatherName, slowbro)
        weather.clearWeather()
        assert weather.currentWeather == expectedWeather
        assert weather.counter == expectedCounter

    @pytest.mark.parametrize(
        "weatherName,ability,item,typing,expectedBool",
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
    def testApplyWeatherDamage(
        self, testPokemon, weatherName, ability, item, typing, expectedBool
    ):
        weather = Weather(weatherName, 5)
        slowbro = testPokemon
        slowbro.item = item
        slowbro.ability = ability
        slowbro.typing = typing
        assert applyWeatherDamage(weather, slowbro) == expectedBool

    @pytest.mark.parametrize(
        "weatherName,typing,expectedInt",
        [
            ("Sandstorm", ["Water", "Psychic"], 1),
            ("Sandstorm", ["Rock", "Fire"], 1.5),
            ("Sandstorm", ["Dark", "Rock"], 1.5),
        ],
    )
    def testCheckSandstormSpDefBoost(
        self, testPokemon, weatherName, typing, expectedInt
    ):
        weather = Weather(weatherName, 5)
        slowbro = testPokemon
        slowbro.typing = typing
        assert checkSandstormSpDefBoost(weather, slowbro) == expectedInt

    @pytest.mark.parametrize(
        "weatherName,moveType,expectedInt",
        [
            ("Harsh Sunlight", "Water", 0.5),
            ("Harsh Sunlight", "Fire", 1.5),
            ("Rain", "Water", 1.5),
            ("Rain", "Fire", 0.5),
        ],
    )
    def testCheckDamageModFromWeather(
        self, testPokemon, weatherName, moveType, expectedInt
    ):
        weather = Weather(weatherName, 5)
        slowbro = testPokemon
        slowbro.moves[0].type = moveType
        assert checkDamageModFromWeather(weather, slowbro, 0) == expectedInt