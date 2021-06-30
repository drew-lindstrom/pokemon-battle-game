from player import Player
from pokemon import Pokemon
import pytest


class TestPlayer:
    @pytest.fixture
    def testPlayer(self):
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

        testPlayer = Player([slowbro, tyranitar])
        return testPlayer

    @pytest.mark.parametrize(
        "pokemon1Hp,pokemon2Hp,expectedOutput",
        [(100, 100, False), (0, 100, False), (0, 0, True)],
    )
    def testGameOverCheck(self, testPlayer, pokemon1Hp, pokemon2Hp, expectedOutput):
        testPlayer[1].stat["hp"] = pokemon1Hp
        testPlayer[0].stat["hp"] = pokemon2Hp
        assert testPlayer.checkGameOver() == expectedOutput

    def testClearHazards(self, testPlayer):
        testPlayer.spikes = 2
        testPlayer.tspikes = 2
        testPlayer.stealthRocks = True
        testPlayer.stickyWeb = True
        testPlayer.clearHazards()
        assert testPlayer.spikes == 0
        assert testPlayer.tspikes == 0
        assert testPlayer.stealthRocks == False
        assert testPlayer.stealthRocks == False