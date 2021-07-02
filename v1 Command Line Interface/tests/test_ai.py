from frame import Frame
from pokemon import Pokemon
from player import Player
from weather import Weather
from terrain import Terrain
from ai import *

import pytest


class TestAI:
    @pytest.fixture
    def testFrame(self):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Slack Off", "Scald", "Tackle", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
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
            ("Pyro Ball", "Blaze Kick", "Gunk Shot", "High Jump Kick"),
            "Libero",
            "Heavy Duty Boots",
            (31, 31, 31, 31, 31, 31),
            (0, 252, 0, 0, 4, 252),
            "Jolly",
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

        p1 = Player([slowbro, tapuLele, cinderace])
        p2 = Player([tyranitar])
        w = Weather()
        t = Terrain()
        testFrame = Frame(p1, p2, None, None, w, t)
        return testFrame

    def testChooseMove(self, testFrame):
        chooseMove(testFrame)
        assert testFrame.attack == testFrame.user.moves[1]

    def testChooseHighestDamagingAttack(self, testFrame):
        assert chooseHighestDamagingAttack(testFrame) == (153, 1)

    @pytest.mark.parametrize(
        "inputN,inputPp,inputVStatus,inputPrevMove,expectedBool",
        [
            (1, 5, None, None, True),
            (1, 0, None, None, False),
            (1, 5, "Move Lock", "Surf", False),
            (1, 5, "Move Lock", "Scald", True),
        ],
    )
    def testCheckIfDamagingAttack(
        self, testFrame, inputN, inputPp, inputVStatus, inputPrevMove, expectedBool
    ):
        testFrame.attack = testFrame.user.moves[inputN]
        testFrame.user.moves[inputN].pp = inputPp
        testFrame.user.vStatus[inputVStatus] = None
        testFrame.user.prevMove = inputPrevMove
        assert checkIfDamagingAttack(testFrame, inputN) == expectedBool

    @pytest.mark.parametrize(
        "inputN,inputAttackType,inputTargetType,expectedBool",
        [(1, "Water", "Water", True), (1, "Poison", "Steel", False)],
    )
    def testCheckIfNoTypeImmunity(
        self, testFrame, inputN, inputAttackType, inputTargetType, expectedBool
    ):
        testFrame.user.moves[inputN].type = inputAttackType
        testFrame.target.typing[0] = inputTargetType
        assert checkIfNoTypeImmunity(testFrame, inputN) == expectedBool

    @pytest.mark.parametrize(
        "inputDamage,inputHighestDamage,inputMoveNumber,inputN,expectedHighestDamage,expectedMoveNumber",
        [(100, 150, 0, 1, 150, 0), (150, 100, 0, 1, 150, 1)],
    )
    def testSetHighestDamageAndMoveNumber(
        self,
        inputDamage,
        inputHighestDamage,
        inputMoveNumber,
        inputN,
        expectedHighestDamage,
        expectedMoveNumber,
    ):
        assert setHighestDamageAndMoveNumber(
            inputHighestDamage, inputDamage, inputMoveNumber, inputN
        ) == (expectedHighestDamage, expectedMoveNumber)

    def testChooseNextPokemon(self, testFrame):
        testFrame.attackingTeam[1].stat["hp"] = 0
        testFrame.attackingTeam[1].checkFainted()
        chooseNextPokemon(testFrame)
        assert testFrame.switchChoice == 2