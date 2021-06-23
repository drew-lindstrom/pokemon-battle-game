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
        tapu_lele = Pokemon(
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

        p1 = Player([slowbro, tapu_lele, cinderace])
        p2 = Player([tyranitar])
        w = Weather()
        t = Terrain()
        testFrame = Frame(p1, p2, None, None, w, t)
        return testFrame

    def test_choose_highest_damaging_attack(self, testFrame):
        chooseHighestDamagingAttack(testFrame)
        assert testFrame.attack == testFrame.user.moves[1]
        # TODO: Test with move lock.

    def test_choose_next_pokemon(self, testFrame):
        testFrame.attacking_team[1].stat["hp"] = 0
        testFrame.attacking_team[1].check_fainted()
        chooseNextPokemon(testFrame)
        assert testFrame.switch_choice == 2