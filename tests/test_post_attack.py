from post_attack import *
from pokemon import Pokemon
from player import Player
from weather import Weather
from terrain import Terrain
from frame import Frame
import pytest


class TestPostAttack:
    @pytest.fixture
    def testPokemon(self):
        testPokemon = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            "Leftovers",
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        return testPokemon

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
        tyranitar = Pokemon(
            "Tyranitar",
            100,
            "Male",
            ("Crunch", "Stealth Rock", "Toxic", "Earthquake"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 0, 0, 216, 40),
            "Careful",
        )
        tapuLele = Pokemon(
            "Tapu Lele",
            100,
            None,
            ("Psychic", "Moonblast", "Focus Blast", "Psyshock"),
            "Psychic Surge",
            "Choice Specs",
            (31, 0, 31, 31, 31, 31),
            (0, 0, 0, 252, 4, 252),
            "Timid",
        )
        cinderace = Pokemon(
            "Cinderace",
            100,
            "Male",
            ("Pyro Ball", "U-turn", "Gunk Shot", "High Jump Kick"),
            "Libero",
            "Heavy Duty Boots",
            (31, 31, 31, 31, 31, 31),
            (0, 252, 0, 0, 4, 252),
            "Jolly",
        )
        p1 = Player([slowbro, tyranitar])
        p2 = Player([tapuLele, cinderace])
        w = Weather()
        t = Terrain()
        testFrame = Frame(p1, p2, None, None, w, t)
        return testFrame

    def testApplyStatAltAttack(self, testPokemon):
        p = testPokemon
        assert p.statMod["defense"] == 0
        assert p.statMod["spDefense"] == 0
        applyStatAltAttack(p, None, "Close Combat", 50)
        assert p.statMod["defense"] == -1
        assert p.statMod["spDefense"] == -1

    def testApplyStatusInflictingAttack(self, testPokemon):
        p = testPokemon
        assert p.status[0] == None
        applyStatusInflictingAttack(None, p, "Toxic", 50)
        assert p.status[0] == "Badly Poisoned"

    def testApplyVStatusInflictingAttack(self, testPokemon):
        p = testPokemon
        assert len(p.vStatus) == 0
        applyVStatusInflictingAttack(None, p, "Dark Pulse", 20)
        assert p.vStatus["Flinched"] == [1]

    @pytest.mark.parametrize("inputHp,expectedHp", [(360, 384), (380, 394)])
    def testApplyLeftovers(self, testPokemon, inputHp, expectedHp):
        slowbro = testPokemon
        slowbro.stat["hp"] = inputHp
        applyLeftovers(slowbro)
        assert slowbro.stat["hp"] == expectedHp

    @pytest.mark.parametrize("inputHp,expectedHp", [(394, 370), (5, 0)])
    def testApplyBurn(self, testPokemon, inputHp, expectedHp):
        p = testPokemon
        p.stat["hp"] = inputHp
        p.status = ["Burned"]
        applyBurn(p)
        assert p.stat["hp"] == expectedHp

    @pytest.mark.parametrize(
        "inputHp,inputStatus,expectedHp",
        [
            (394, ["Badly Poisoned", 14], 370),
            (370, ["Badly Poisoned", 13], 321),
            (394, ["Badly Poisoned", 0], 25),
            (300, ["Poisoned"], 251),
        ],
    )
    def testApplyPoison(self, testPokemon, inputHp, inputStatus, expectedHp):
        p = testPokemon
        applyPoison(p)
        p.stat["hp"] = inputHp
        p.status = inputStatus
        applyPoison(p)
        assert p.stat["hp"] == expectedHp

    @pytest.mark.parametrize("inputHp,expectedHp", [(394, 344), (35, 0)])
    def testApplyRecoil(self, testPokemon, inputHp, expectedHp):
        p = testPokemon
        p.stat["hp"] = inputHp
        applyRecoil(p, 100, 0.5)
        assert p.stat["hp"] == expectedHp

    @pytest.mark.parametrize(
        "inputName,i,item,expectedResult",
        [
            ("Close Combat", 100, None, None),
            ("Close Combat", 20, "Protective Pads", None),
            ("Close Combat", 20, None, "Paralyzed"),
            ("Surf", 20, None, None),
        ],
    )
    def testApplyStatic(self, testFrame, inputName, i, item, expectedResult):
        testFrame.user.setMove(0, inputName)
        testFrame.attack = testFrame.user.moves[0]
        testFrame.user.item = item
        applyStatic(testFrame, i)
        assert testFrame.user.status[0] == expectedResult