from stat_calc import *
from frame import Frame
from pokemon import Pokemon
from player import Player
from weather import Weather
from terrain import Terrain
import pytest


class TestStatCalc:
    @pytest.fixture
    def testFrame(self):
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

        p1 = Player([slowbro])
        p2 = Player([slowbro])
        w = Weather()
        t = Terrain()
        testFrame = Frame(p1, p2, None, None, w, t)
        return testFrame

    @pytest.mark.parametrize(
        "attackType,item,ability,hp,critBool,statMod,expectedInt",
        [
            ("Water", None, None, 300, False, 0, 186),
            ("Fire", None, "Blaze", 1, False, 0, 279),
            ("Fire", None, "Blaze", 300, True, 0, 186),
            ("Fire", "Choice Band", "Blaze", 300, False, 0, 279),
            ("Normal", None, None, 300, False, 6, 744),
            ("Normal", None, None, 300, True, 6, 744),
            ("Normal", "Choice Band", None, 300, False, 6, 1116),
            ("Normal", None, None, 300, False, -6, 46),
            ("Normal", None, None, 300, True, -6, 186),
            ("Normal", "Choice Band", None, 300, False, -6, 69),
        ],
    )
    def testCalcAttack(
        self,
        testFrame,
        attackType,
        item,
        ability,
        hp,
        critBool,
        statMod,
        expectedInt,
    ):
        p1 = testFrame.user
        testFrame.attack = testFrame.user.moves[0]
        testFrame.attack.type = attackType
        p1.item = item
        p1.ability = ability
        p1.stat["hp"] = hp
        testFrame.crit = critBool
        p1.statMod["attack"] = statMod
        assert calcAttack(testFrame) == expectedInt

    @pytest.mark.parametrize(
        "statMod,critBool,expectedInt",
        [
            (0, False, 350),
            (0, True, 350),
            (6, False, 1400),
            (6, True, 350),
            (-6, False, 87),
            (-6, True, 87),
        ],
    )
    def testCalcDefense(self, testFrame, statMod, critBool, expectedInt):
        p1 = testFrame.target
        p1.statMod["defense"] = statMod
        testFrame.crit = critBool
        assert calcDefense(testFrame) == expectedInt

    @pytest.mark.parametrize(
        "attackType,item,ability,hp,critBool,statMod,expectedInt",
        [
            ("Water", None, None, 300, False, 0, 236),
            ("Fire", None, "Blaze", 1, False, 0, 354),
            ("Fire", None, "Blaze", 300, True, 0, 236),
            ("Fire", "Choice Spec", "Blaze", 300, False, 0, 354),
            ("Fire", "Choice Spec", "Blaze", 300, True, 0, 354),
            ("Normal", None, None, 300, False, 6, 944),
            ("Normal", None, None, 300, True, 6, 944),
            ("Normal", "Choice Spec", None, 300, False, 6, 1416),
            ("Normal", "Choice Spec", None, 300, True, 6, 1416),
            ("Normal", None, None, 300, False, -6, 59),
            ("Normal", None, None, 300, True, -6, 236),
            ("Normal", "Choice Spec", None, 300, False, -6, 88),
            ("Normal", "Choice Spec", None, 300, True, -6, 354),
        ],
    )
    def testCalcSpAttack(
        self,
        testFrame,
        attackType,
        item,
        ability,
        hp,
        critBool,
        statMod,
        expectedInt,
    ):
        p1 = testFrame.user
        testFrame.attack = testFrame.user.moves[0]
        testFrame.attack.type = attackType
        p1.item = item
        p1.ability = ability
        p1.stat["hp"] = hp
        testFrame.crit = critBool
        p1.statMod["spAttack"] = statMod
        assert calcSpAttack(testFrame) == expectedInt

    @pytest.mark.parametrize(
        "type,weather,crit,statMod,expectedInt",
        [
            (["Rock", "Psychic"], "Clear Skies", False, 0, 197),
            (["Rock", "Psychic"], "Clear Skies", True, 0, 197),
            (["Rock", "Psychic"], "Sandstorm", False, 0, 295),
            (["Rock", "Psychic"], "Sandstorm", True, 0, 295),
            (["Rock", "Psychic"], "Clear Skies", False, 6, 788),
            (["Rock", "Psychic"], "Clear Skies", False, 6, 788),
            (["Rock", "Psychic"], "Sandstorm", False, 6, 1182),
            (["Rock", "Psychic"], "Sandstorm", True, 6, 295),
            (["Rock", "Psychic"], "Clear Skies", False, -6, 49),
            (["Rock", "Psychic"], "Clear Skies", True, -6, 49),
            (["Rock", "Psychic"], "Sandstorm", False, -6, 73),
            (["Rock", "Psychic"], "Sandstorm", True, -6, 73),
        ],
    )
    def testCalcSpDefense(self, testFrame, type, weather, crit, statMod, expectedInt):
        p1 = testFrame.target
        w = testFrame.weather
        p1.typing = type
        p1.statMod["spDefense"] = statMod
        w.currentWeather = weather
        testFrame.crit = crit
        assert calcSpDefense(testFrame) == expectedInt

    @pytest.mark.parametrize(
        "item,ability,weather,status,statMod,expectedInt",
        [
            (None, None, "Clear Skies", [None], 0, 86),
            ("Choice Scarf", None, "Clear Skies", [None], 0, 129),
            (None, "Sand Rush", "Clear Skies", [None], 0, 86),
            (None, "Sand Rush", "Sandstorm", [None], 0, 172),
            (None, None, "Clear Skies", ["Paralyzed"], 0, 43),
            ("Choice Scarf", None, "Clear Skies", ["Paralyzed"], 0, 64),
            (None, None, "Clear Skies", [None], 6, 344),
            ("Choice Scarf", None, "Clear Skies", [None], 6, 516),
            (None, None, "Clear Skies", ["Paralyzed"], 6, 172),
            ("Choice Scarf", None, "Clear Skies", ["Paralyzed"], 6, 258),
            (None, None, "Clear Skies", [None], -6, 21),
            ("Choice Scarf", None, "Clear Skies", [None], -6, 31),
            (None, None, "Clear Skies", ["Paralyzed"], -6, 10),
            ("Choice Scarf", None, "Clear Skies", ["Paralyzed"], -6, 15),
        ],
    )
    def testCalcSpeed(
        self, testFrame, item, ability, weather, status, statMod, expectedInt
    ):
        p1 = testFrame.user
        p1.item = item
        p1.ability = ability
        p1.status = status
        p1.statMod["speed"] = statMod
        testFrame.weather.currentWeather = weather
        assert calcSpeed(testFrame) == expectedInt

    def checkBlaze(self, testFrame):
        testFrame.user.ability = "Blaze"
        assert checkBlaze(testFrame) == 1
        testFrame.attack = testFrame.user.moves[0]
        testFrame.attack.type = "Fire"
        testFrame.user.stat["hp"] = 1
        assert checkBlaze(testFrame) == 1.5
