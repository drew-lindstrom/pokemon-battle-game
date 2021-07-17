from ui import *
from frame import Frame
from pokemon import Pokemon
from player import Player
from weather import Weather
from terrain import Terrain
import pytest


class TestUI:
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
        testFrame.attack = testFrame.user.moves[0]
        return testFrame

    @pytest.mark.parametrize(
        "inputList,testAttribute,expectedResult",
        [
            (["8", "-4", "b", "2"], testFrame.attack, testFrame.user.moves[1]),
            (["5", "1"], testFrame.switchChoice, 1),
        ],
    )
    def testGetChoice(self, testFrame, inputList, testAttribute, expectedResult):
        getChoice(testFrame, inputList)
        assert testAttribute == expectedResult

    def testGetNextChoice(self, testFrame):
        inputList = [1]
        assert getNextChoice(testFrame, inputList) == 1

    def testCallAppropriateFunctionBasedOnChoice(self, testFrame):
        callAppropriateFunctionBasedOnChoice(testFrame, 2, None)
        assert testFrame.attack == testFrame.user.moves[1]
        callAppropriateFunctionBasedOnChoice(testFrame, 5, ["1"])
        assert testFrame.switchChoice == "1"

    @pytest.mark.parametrize(
        "inputPP,inputVStatus,inputPrevMove,inputChoice,expectedBool",
        [
            (5, None, None, 1, True),
            (0, None, None, 1, False),
            (5, "Move Lock", "Slack Off", 1, False),
        ],
    )
    def testCheckIfValidChoice(
        self, testFrame, inputPP, inputVStatus, inputPrevMove, inputChoice, expectedBool
    ):
        testFrame.user.moves[inputChoice - 1].pp = inputPP
        testFrame.user.vStatus[inputVStatus] = None
        testFrame.user.prevMove = inputPrevMove
        assert checkIfValidChoice(testFrame, inputChoice) == expectedBool

    @pytest.mark.parametrize(
        "inputPP,inputChoice,expectedBool", [(5, 1, True), (0, 1, False)]
    )
    def testCheckIfChoiceHasEnoughPP(
        self, testFrame, inputPP, inputChoice, expectedBool
    ):
        testFrame.user.moves[inputChoice - 1].pp = inputPP
        assert checkIfChoiceHasEnoughPP(testFrame, inputChoice) == expectedBool

    @pytest.mark.parametrize(
        "inputVStatus,inputPrevMove,inputChoice,expectedBool",
        [
            (None, None, 1, True),
            ("Move Lock", None, 1, True),
            (None, "Slack Off", 1, True),
            ("Move Lock", "Scald", 1, True),
            ("Move Lock", "Slack Off", 1, False),
        ],
    )
    def testCheckIfUserHasMoveLock(
        self, testFrame, inputVStatus, inputPrevMove, inputChoice, expectedBool
    ):
        testFrame.user.vStatus[inputVStatus] = None
        testFrame.user.prevMove = inputPrevMove
        assert checkIfUserHasMoveLock(testFrame, inputChoice) == expectedBool

    def testGetSwitch(self, testFrame):
        getSwitch(testFrame, ["3", "a", "1"])
        assert testFrame.switchChoice == 1

    def testGetNextSwitchChoice(self, testFrame):
        inputList = [1]
        assert getNextSwitchChoice(testFrame, inputList) == 1

    @pytest.mark.parametrize(
        "inputSwitchChoice,inputStatus,expectedResult",
        [(1, None, 1), (1, "Fainted", 0)],
    )
    def testCheckIfSwitchChoiceHasFainted(
        self, testFrame, inputSwitchChoice, inputStatus, expectedResult
    ):
        switchChoice = inputSwitchChoice
        testFrame.attackingTeam[1].status[0] = inputStatus
        assert checkIfSwitchChoiceHasFainted(testFrame, switchChoice) == expectedResult
