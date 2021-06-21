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
            ("Slack Off", "Scald", "Future Sight", "Teleport"),
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
        test_frame = Frame(p1, p2, None, None, w, t)
        return test_frame

    def test_choose_highest_damaging_attack(self, test_frame):
        assert choose_highest_damaging_attack(test_frame) == 1
        # TODO: Test with move lock.
