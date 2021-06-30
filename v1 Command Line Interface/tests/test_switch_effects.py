from pokemon import Pokemon
from terrain import Terrain
from weather import Weather
import switch_effects
import pytest


class TestSwitchEffects:
    @pytest.fixture
    def testPokemon(self):
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

    def testActivateGrassySurge(self, testPokemon):
        tyranitar, slowbro = testPokemon
        tyranitar.ability = "Grassy Surge"
        terrain = Terrain()
        assert terrain.currentTerrain == None
        switch_effects.activateGrassySurge(tyranitar, terrain)
        assert terrain.currentTerrain == "Grassy Terrain"

    def testActivateIntimidate(self, testPokemon):
        tyranitar, slowbro = testPokemon
        slowbro.ability = "Intimidate"
        switch_effects.activateIntimidate(slowbro, tyranitar)
        assert tyranitar.statMod["attack"] == -1

    @pytest.mark.parametrize("inputHp,expectedHp", [(100, 231), (0, 0)])
    def testActivateRegenerator(self, testPokemon, inputHp, expectedHp):
        tyranitar, slowbro = testPokemon
        slowbro.stat["hp"] = inputHp
        switch_effects.activateRegenerator(slowbro)
        assert slowbro.stat["hp"] == expectedHp

    def testActivatePsychicSurge(self, testPokemon):
        tyranitar, slowbro = testPokemon
        tyranitar.ability = "Psychic Surge"
        terrain = Terrain()
        assert terrain.currentTerrain == None
        switch_effects.activatePsychicSurge(tyranitar, terrain)
        assert terrain.currentTerrain == "Psychic Terrain"

    def testActivateSandStream(self, testPokemon):
        tyranitar, slowbro = testPokemon
        weather = Weather()
        assert weather.currentWeather == "Clear Skies"
        switch_effects.activateSandStream(tyranitar, weather)
        assert weather.currentWeather == "Sandstorm"