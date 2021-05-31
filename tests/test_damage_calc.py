from player import Player
from pokemon import Pokemon
from move import Move
from weather import Weather
from terrain import Terrain
from main import Frame

from damage_calc import *
import pytest


class TestDamageCalc:
    @pytest.fixture
    def test_frame(self):
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
        test_frame = Frame(p1, p2, None, None, w, t)
        return test_frame

    def test_roll_crit(self):
        assert roll_crit(1) == 1.5
        assert roll_crit(2) == 1

    def test_check_stab(self, test_frame):
        test_frame.attack = test_frame.user.moves[0]
        assert check_stab(test_frame) == 1.5
        test_frame.attack = test_frame.user.moves[2]
        assert check_stab(test_frame) == 1.5
        test_frame.attack = test_frame.user.moves[1]
        assert check_stab(test_frame) == 1

    def test_check_type_effectiveness(self, test_frame):
        test_frame.attack = test_frame.user.moves[0]
        assert check_type_effectiveness(test_frame) == 2
        test_frame.attack = test_frame.user.moves[2]
        assert check_type_effectiveness(test_frame) == 0
        test_frame.attack = test_frame.user.moves[1]
        assert check_type_effectiveness(test_frame) == 0.5

    def test_check_burn(self, test_frame):
        test_frame.user.status = ["Burn"]
        test_frame.attack = test_frame.user.moves[0]
        assert check_burn(test_frame) == 1
        test_frame.user.moves[0].category = "Physical"
        assert check_burn(test_frame) == 0.5

    def test_roll_random(self):
        assert roll_random(85) == 0.85

    def test_check_attacking_and_defending_stats(self, test_frame):
        test_frame.attack = test_frame.user.moves[0]
        assert check_attacking_and_defending_stats(test_frame) == (236, 319)
        test_frame.user.moves[0].category = "Physical"
        assert check_attacking_and_defending_stats(test_frame) == (186, 256)
        test_frame.attack_name = "Psyshock"
        assert check_attacking_and_defending_stats(test_frame) == (236, 256)

    def test_activate_eruption(self, test_frame):
        assert activate_eruption(test_frame) == 150
        test_frame.user.stat["hp"] = 1
        assert activate_eruption(test_frame) == 0

    def test_calc_modified_base_damage(self, test_frame):
        test_frame.attack_name = "Eruption"
        assert calc_modified_base_damage(test_frame) == 150
        test_frame.user.stat["hp"] = 1
        assert calc_modified_base_damage(test_frame) == 0

    def test_calc_modified_damage(self, test_frame):
        pass

    def test_calc_damage(self, test_frame):
        test_frame.attack = test_frame.user.moves[0]
        assert calc_damage(test_frame, False, False) == 153