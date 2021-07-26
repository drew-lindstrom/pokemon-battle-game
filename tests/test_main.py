import pytest
from main import *
from frame import Frame
from player import Player
from pokemon import Pokemon
from weather import Weather
from terrain import Terrain
import gameText

gameText.output = []


class TestMain:
    @pytest.fixture
    def testPlayer(self):
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
        p1 = Player([tyranitar, slowbro])
        return p1

    @pytest.fixture
    def testPlayer2(self):
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
        p2 = Player([tapuLele, cinderace])
        return p2

    @pytest.fixture
    def testFrame(self, testPlayer, testPlayer2):
        w = Weather()
        t = Terrain()
        testFrame = Frame(testPlayer, testPlayer2, None, None, w, t)
        return testFrame

    @pytest.fixture
    def testFrame2(self, testPlayer, testPlayer2):
        w = Weather()
        t = Terrain()
        testFrame = Frame(testPlayer2, testPlayer, None, None, w, t)
        return testFrame

    def testActivateTurnOneSwitchAbilities(self, testPlayer, testPlayer2):
        w = Weather()
        t = Terrain()
        activateTurnOneSwitchAbilities(testPlayer, testPlayer2, w, t)
        assert w.currentWeather == "Sandstorm"
        assert t.currentTerrain == "Psychic Terrain"

    def testApplySwitch(self, testFrame, testFrame2):
        assert testFrame.user.name == "Tyranitar"
        testFrame.switchChoice = 1
        applySwitch(testFrame, testFrame, testFrame2)
        assert testFrame.user.name == "Slowbro"

    def testCheckIfCanAttackAndAttackLands(self, testFrame):
        testFrame.attack = testFrame.user.moves[3]
        assert checkIfCanAttackAndAttackLands(testFrame) == True
        testFrame.attack.type = "Dragon"
        assert checkIfCanAttackAndAttackLands(testFrame) == False

    @pytest.mark.parametrize(
        "inputHp,inputHp2,expectedBool",
        [(100, 100, False), (100, 0, False), (0, 0, True)],
    )
    def testCheckForGameOver(
        self, testFrame, testFrame2, inputHp, inputHp2, expectedBool
    ):
        testFrame.attackingTeam[0].stat["hp"] = inputHp
        testFrame.attackingTeam[1].stat["hp"] = inputHp2
        assert checkForGameOver([testFrame, testFrame2]) == expectedBool
