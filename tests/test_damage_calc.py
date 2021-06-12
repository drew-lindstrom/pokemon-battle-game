from player import Player
from pokemon import Pokemon
from move import Move
from weather import Weather
from terrain import Terrain
from frame import Frame

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

    @pytest.mark.parametrize(
        "i,expected_int,expected_bool", [(1, 1.5, True), (2, 1, False)]
    )
    def test_roll_crit(self, test_frame, i, expected_int, expected_bool):
        assert roll_crit(test_frame, i) == expected_int
        assert test_frame.crit == expected_bool

    @pytest.mark.parametrize("move_number,expected_int", [(0, 1.5), (2, 1.5), (1, 1)])
    def test_check_stab(self, test_frame, move_number, expected_int):
        test_frame.attack = test_frame.user.moves[move_number]
        assert check_stab(test_frame) == expected_int

    @pytest.mark.parametrize("move_number,expected_int", [(0, 2), (2, 0), (1, 0.5)])
    def test_check_type_effectiveness(self, test_frame, move_number, expected_int):
        test_frame.attack = test_frame.user.moves[move_number]
        assert check_type_effectiveness(test_frame) == expected_int

    def test_check_burn(self, test_frame):
        test_frame.user.status = ["Burn"]
        test_frame.attack = test_frame.user.moves[0]
        assert check_burn(test_frame) == 1
        test_frame.user.moves[0].category = "Physical"
        assert check_burn(test_frame) == 0.5

    def test_roll_random(self):
        assert roll_random(85) == 0.85

    @pytest.mark.parametrize(
        "input_category,input_name,expected_result",
        [
            ("Special", "Tackle", (236, 319)),
            ("Physical", "Tackle", (236, 256)),
            ("Special", "Psyshock", (236, 256)),
        ],
    )
    def test_check_attacking_and_defending_stats(
        self, test_frame, input_category, input_name, expected_result
    ):
        test_frame.attack = test_frame.user.moves[0]
        assert check_attacking_and_defending_stats(test_frame) == (236, 319)
        test_frame.user.moves[0].category = "Physical"
        assert check_attacking_and_defending_stats(test_frame) == (186, 256)
        test_frame.attack.name = "Psyshock"
        assert check_attacking_and_defending_stats(test_frame) == (236, 256)

    @pytest.mark.parametrize("input_hp,expected_int", [(394, 150), (1, 0)])
    def test_activate_eruption(self, test_frame, input_hp, expected_int):
        test_frame.user.stat["hp"] = input_hp
        assert activate_eruption(test_frame) == expected_int

    def test_activate_knock_off(self, test_frame):
        test_frame.target.item = "Leftovers"
        test_frame.attack_name = "Knock Off"
        assert activate_knock_off(test_frame) == 97
        assert test_frame.target.item == None
        assert activate_knock_off(test_frame) == 65

    @pytest.mark.parametrize(
        "number,name,input_hp,expected_int",
        [(0, "Eruption", 394, 150), (0, "Eruption", 1, 0)],
    )
    def test_calc_modified_base_damage(
        self, test_frame, number, name, input_hp, expected_int
    ):
        test_frame.user.set_move(number, name)
        test_frame.attack = test_frame.user.moves[0]
        test_frame.user.stat["hp"] = input_hp
        assert calc_modified_base_damage(test_frame) == expected_int

    def test_calc_modified_damage(self, test_frame):
        pass

    def test_calc_damage(self, test_frame):
        test_frame.attack = test_frame.user.moves[0]
        assert calc_damage(test_frame, False, False) == 153