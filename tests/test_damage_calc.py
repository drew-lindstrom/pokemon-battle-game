from player import Player
from pokemon import Pokemon
from move import Move
from weather import Weather
from terrain import Terrain
from frame import Frame
from damage_calc import *
import gameText
import pytest

gameText.output = []


class TestDamageCalc:
    @pytest.fixture
    def testFrame(self):
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
            ("Crunch", "Stealth Rock", "Toxic", "Earthquake"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 0, 0, 216, 40),
            "Careful",
        )

        p1 = Player([slowbro])
        p2 = Player([tyranitar])
        w = Weather()
        t = Terrain()
        testFrame = Frame(p1, p2, None, None, w, t)
        return testFrame

    @pytest.mark.parametrize(
        "i,expectedInt,expectedBool", [(1, 1.5, True), (2, 1, False)]
    )
    def testRollCrit(self, testFrame, i, expectedInt, expectedBool):
        assert rollCrit(testFrame, i) == expectedInt
        assert testFrame.crit == expectedBool

    @pytest.mark.parametrize("moveNumber,expectedInt", [(0, 1.5), (2, 1.5), (1, 1)])
    def testCheckStab(self, testFrame, moveNumber, expectedInt):
        testFrame.attack = testFrame.user.moves[moveNumber]
        assert checkStab(testFrame) == expectedInt

    @pytest.mark.parametrize("moveNumber,expectedInt", [(0, 2), (2, 0), (1, 0.5)])
    def testCheckTypeEffectiveness(self, testFrame, moveNumber, expectedInt):
        testFrame.attack = testFrame.user.moves[moveNumber]
        assert checkTypeEffectiveness(testFrame) == expectedInt

    def testCheckBurn(self, testFrame):
        testFrame.user.status = ["Burn"]
        testFrame.attack = testFrame.user.moves[0]
        assert checkBurn(testFrame) == 1
        testFrame.user.moves[0].category = "Physical"
        assert checkBurn(testFrame) == 0.5

    def testRollRandom(self):
        assert rollRandom(85) == 0.85

    @pytest.mark.parametrize(
        "inputCategory,inputName,expectedResult",
        [
            ("Special", "Tackle", (236, 319)),
            ("Physical", "Tackle", (236, 256)),
            ("Special", "Psyshock", (236, 256)),
        ],
    )
    def testCheckAttackingAndDefendingStats(
        self, testFrame, inputCategory, inputName, expectedResult
    ):
        testFrame.attack = testFrame.user.moves[0]
        assert checkAttackingAndDefendingStats(testFrame) == (236, 319)
        testFrame.user.moves[0].category = "Physical"
        assert checkAttackingAndDefendingStats(testFrame) == (186, 256)
        testFrame.attack.name = "Psyshock"
        assert checkAttackingAndDefendingStats(testFrame) == (236, 256)

    @pytest.mark.parametrize("inputHp,expectedInt", [(394, 150), (1, 0)])
    def testActivateEruption(self, testFrame, inputHp, expectedInt):
        testFrame.user.stat["hp"] = inputHp
        assert activateEruption(testFrame) == expectedInt

    def testActivateKnockOff(self, testFrame):
        testFrame.target.item = "Leftovers"
        testFrame.attackName = "Knock Off"
        assert activateKnockOff(testFrame) == 97
        assert testFrame.target.item == None
        assert activateKnockOff(testFrame) == 65

    @pytest.mark.parametrize(
        "number,name,inputHp,inputBaseDamage,inputAttackType,inputTerrainName,expectedInt",
        [
            (0, "Eruption", 394, 150, "Fire", None, 150),
            (0, "Eruption", 1, 150, "Fire", None, 0),
            (0, "Tackle", 394, 100, "Electric", "Electric Terrain", 130),
        ],
    )
    def testCalcModifiedBaseDamage(
        self,
        testFrame,
        number,
        name,
        inputHp,
        inputBaseDamage,
        inputAttackType,
        inputTerrainName,
        expectedInt,
    ):
        testFrame.user.setMove(number, name)
        testFrame.attack = testFrame.user.moves[0]
        testFrame.user.stat["hp"] = inputHp
        testFrame.attack.type = inputAttackType
        testFrame.terrain.currentTerrain = inputTerrainName
        assert (
            calcModifiedBaseDamage(testFrame, inputBaseDamage, ghostCalc=False)
            == expectedInt
        )

    def testCalcModifiedDamage(self, testFrame):
        pass

    def testCalcDamage(self, testFrame):
        testFrame.attack = testFrame.user.moves[0]
        assert calcDamage(testFrame, False, False) == 153