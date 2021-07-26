from move_effects import *
from pokemon import Pokemon
from player import Player
from frame import Frame
from weather import Weather
from terrain import Terrain
import gameText
import pytest

gameText.output = []


class TestMoveEffects:
    @pytest.fixture
    def testFrame(self):
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

        p1 = Player([tapuLele])
        p2 = Player([cinderace])
        w = Weather()
        t = Terrain()
        testFrame = Frame(p1, p2, None, None, w, t)
        return testFrame

    def testActivateDefog(self, testFrame):
        testFrame.attackingTeam.stealthRocks == True
        testFrame.defendingTeam.stealthRocks == True
        activateDefog(testFrame)
        assert testFrame.attackingTeam.stealthRocks == False
        assert testFrame.defendingTeam.stealthRocks == False
        assert testFrame.target.statMod["evasion"] == -1

    def testActivateRoost(self, testFrame):
        testFrame.user.stat["hp"] = 30
        activateRoost(testFrame)
        assert testFrame.user.stat["hp"] == 170
        assert testFrame.user.vStatus["Temporary Grounded"][0] == 1

    def testActivateSlackOff(self, testFrame):
        testFrame.user.stat["hp"] = 30
        activateSlackOff(testFrame)
        assert testFrame.user.stat["hp"] == 170

    def testSetStealthRocks(self, testFrame):
        setStealthRocks(testFrame)
        assert testFrame.defendingTeam.stealthRocks == True

    # def testSetLightScreenAndResetLightScreen(self):
    #     slowbro = Pokemon(
    #         "Slowbro",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (252, 0, 252, 0, 4, 0),
    #         "Relaxed",
    #     )
    #     testPlayer = Player([slowbro])

    #     setLightScreen(testPlayer)
    #     assert testPlayer.lightScreen == True
    #     assert testPlayer.lightScreenCounter == 5
    #     testPlayer.lightScreenCounter = 0
    #     resetLightScreen(testPlayer)
    #     assert testPlayer.lightScreen == False
    #     slowbro.item = "Light Clay"
    #     setLightScreen(testPlayer)
    #     assert testPlayer.lightScreenCounter == 8

    # def testSetReflectAndResetReflect(self):
    #     slowbro = Pokemon(
    #         "Slowbro",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (252, 0, 252, 0, 4, 0),
    #         "Relaxed",
    #     )
    #     testPlayer = Player([slowbro])

    #     setReflect(testPlayer)
    #     assert testPlayer.reflect == True
    #     assert testPlayer.reflectCounter == 5
    #     testPlayer.reflectCounter = 0
    #     resetReflect(testPlayer)
    #     assert testPlayer.reflect == False
    #     slowbro.item = "Light Clay"
    #     setReflect(testPlayer)
    #     assert testPlayer.reflectCounter == 8

    # def testSetSpike(self):
    #     slowbro = Pokemon(
    #         "Slowbro",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (252, 0, 252, 0, 4, 0),
    #         "Relaxed",
    #     )
    #     testPlayer = Player([slowbro])

    #     setSpike(testPlayer)
    #     assert testPlayer.spikes == 1
    #     setSpike(testPlayer)
    #     assert testPlayer.spikes == 2
    #     setSpike(testPlayer)
    #     setSpike(testPlayer)
    #     assert testPlayer.spikes == 3

    # def testSetTspike(self):
    #     slowbro = Pokemon(
    #         "Slowbro",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (252, 0, 252, 0, 4, 0),
    #         "Relaxed",
    #     )

    #     testPlayer = Player([slowbro])

    #     setTspike(testPlayer)
    #     assert testPlayer.tspikes == 1
    #     setTspike(testPlayer)
    #     assert testPlayer.tspikes == 2
    #     setTspike(testPlayer)
    #     assert testPlayer.tspikes == 2

    # def testSetStickyWeb(self):
    #     slowbro = Pokemon(
    #         "Slowbro",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (252, 0, 252, 0, 4, 0),
    #         "Relaxed",
    #     )
    #     testPlayer = Player([slowbro])

    #     setStickyWeb(testPlayer)
    #     assert testPlayer.stickyWeb == True
