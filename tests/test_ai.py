from frame import Frame
from pokemon import Pokemon
from player import Player
from weather import Weather
from terrain import Terrain
from ai import *

import pytest


class TestAI:
    @pytest.fixture
    def test_frame(self):
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
        test_frame = Frame(p1, p2, None, None, w, t)
        return test_frame

    def test_choose_highest_damaging_attack(self, test_frame):
        choose_highest_damaging_attack(test_frame)
        assert test_frame.attack == test_frame.user.moves[1]
        # TODO: Test with move lock.

    def test_choose_next_pokemon(self, test_frame):
        test_frame.attacking_team[1].stat["hp"] = 0
        test_frame.attacking_team[1].check_fainted()
        assert choose_next_pokemon(test_frame) == 2