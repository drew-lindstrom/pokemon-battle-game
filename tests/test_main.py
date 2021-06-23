from frame import Frame
from player import Player
from pokemon import Pokemon
from weather import Weather
from terrain import Terrain
import pytest


class TestMain:
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
        return testFrame, slowbro, tyranitar, tapuLele, cinderace

    def testUpdateCurPokemon(self, testFrame):
        frame = testFrame[0]
        slowbro = testFrame[1]
        tyranitar = testFrame[2]
        tapuLele = testFrame[3]
        cinderace = testFrame[4]
        assert frame.user == slowbro
        assert frame.target == tapuLele
        frame.attackingTeam.curPokemon = tyranitar
        frame.defendingTeam.curPokemon = cinderace
        frame.updateCurPokemon()
        assert frame.user == tyranitar
        assert frame.target == cinderace