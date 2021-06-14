from stat_calc import *
from frame import Frame
from pokemon import Pokemon
from player import Player
from weather import Weather
from terrain import Terrain
import pytest


class TestStatCalc:
    @pytest.fixture
    def test_frame(self):
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

        p1 = Player([slowbro])
        p2 = Player([slowbro])
        w = Weather()
        t = Terrain()
        test_frame = Frame(p1, p2, None, None, w, t)
        return test_frame

    @pytest.mark.parametrize(
        "attack_type,item,ability,hp,crit_bool,stat_mod,expected_int",
        [
            ("Water", None, None, 300, False, 0, 186),
            ("Fire", None, "Blaze", 1, False, 0, 279),
            ("Fire", None, "Blaze", 300, True, 0, 186),
            ("Fire", "Choice Band", "Blaze", 300, False, 0, 279),
            ("Normal", None, None, 300, False, 6, 744),
            ("Normal", None, None, 300, True, 6, 744),
            ("Normal", "Choice Band", None, 300, False, 6, 744),
            ("Normal", None, None, 300, False, -6, 46),
            ("Normal", None, None, 300, True, -6, 186),
            ("Normal", "Choice Band", None, 300, False, -6, 69),
        ],
    )
    def test_calc_attack(
        self,
        test_frame,
        attack_type,
        item,
        ability,
        hp,
        crit_bool,
        stat_mod,
        expected_int,
    ):
        p1 = test_frame.user
        test_frame.attack = test_frame.user.moves[0]
        test_frame.attack.type = attack_type
        p1.item = item
        p1.ability = ability
        p1.stat["hp"] = hp
        test_frame.crit = crit_bool
        p1.stat_mod["attack"] = stat_mod
        assert calc_attack(test_frame) == expected_int

    @pytest.mark.parametrize(
        "stat_mod,crit_bool,expected_int",
        [
            (0, False, 350),
            (0, True, 350),
            (6, False, 1400),
            (6, True, 350),
            (-6, False, 87),
            (-6, True, 87),
        ],
    )
    def test_calc_defense(self, test_frame, stat_mod, crit_bool, expected_int):
        p1 = test_frame.target
        p1.stat_mod["defense"] = stat_mod
        test_frame.crit = crit_bool
        assert calc_defense(test_frame) == expected_int

    @pytest.mark.parametrize(
        "attack_type,item,ability,hp,crit_bool,stat_mod,expected_int",
        [
            ("Water", None, None, 300, False, 0, 236),
            ("Fire", None, "Blaze", 1, False, 0, 354),
            ("Fire", None, "Blaze", 300, True, 0, 236),
            ("Fire", "Choice Specs", "Blaze", 300, False, 0, 354),
            ("Fire", "Choice Specs", "Blaze", 300, True, 0, 354),
            ("Normal", None, None, 300, False, 6, 944),
            ("Normal", None, None, 300, True, 6, 944),
            ("Normal", "Choice Spec", None, 300, False, 6, 1416),
            ("Normal", "Choice Spec", None, 300, True, 6, 1416),
            ("Normal", None, None, 300, False, -6, 59),
            ("Normal", None, None, 300, True, -6, 236),
            ("Normal", "Choice Spec", None, 300, False, -6, 88),
            ("Normal", "Choice Spec", None, 300, True, -6, 354),
        ],
    )
    def test_calc_sp_attack(
        self,
        test_frame,
        attack_type,
        item,
        ability,
        hp,
        crit_bool,
        stat_mod,
        expected_int,
    ):
        p1 = test_frame.user
        test_frame.attack = test_frame.user.moves[0]
        test_frame.attack.type = attack_type
        p1.item = item
        p1.ability = ability
        p1.stat["hp"] = hp
        test_frame.crit = crit_bool
        p1.stat_mod["sp_attack"] = stat_mod
        assert calc_sp_attack(test_frame) == expected_int

    @pytest.mark.parametrize(
        "type,weather,crit,stat_mod,expected_int",
        [
            (["Rock", "Psychic"], "Clear Skies", False, 0, 197),
            (["Rock", "Psychic"], "Clear Skies", True, 0, 197),
            (["Rock", "Psychic"], "Sandstorm", False, 0, 295),
            (["Rock", "Psychic"], "Sandstorm", True, 0, 295),
            (["Rock", "Psychic"], "Clear Skies", False, 6, 788),
            (["Rock", "Psychic"], "Clear Skies", False, 6, 197),
            (["Rock", "Psychic"], "Sandstorm", False, 6, 1182),
            (["Rock", "Psychic"], "Sandstorm", True, 6, 295),
            (["Rock", "Psychic"], "Clear Skies", False, -6, 49),
            (["Rock", "Psychic"], "Clear Skies", True, -6, 49),
            (["Rock", "Psychic"], "Sandstorm", False, -6, 73),
            (["Rock", "Psychic"], "Sandstorm", True, -6, 73),
        ],
    )
    def test_calc_sp_defense(
        self, test_frame, type, weather, crit, stat_mod, expected_int
    ):
        p1 = test_frame.target
        w = test_frame.weather
        p1.typing = type
        p1.stat_mod["sp_defense"] = stat_mod
        w.current_weather = weather
        test_frame.crit = crit
        assert calc_sp_defense(test_frame) == expected_int

    @pytest.mark.parametrize(
        "item,ability,weather,status,stat_mod,expected_int",
        [
            (None, None, "Clear Skies", [None], 0, 86),
            ("Choice Scarf", None, "Clear Skies", [None], 0, 129),
            (None, "Sand Rush", "Clear Skies", [None], 0, 86),
            (None, "Sand Rush", "Sandstorm", [None], 0, 172),
            (None, None, "Clear Skies", ["Paralyzed"], 0, 43),
            ("Choice Scarf", None, "Clear Skies", ["Paralyzed"], 0, 64),
            (None, None, "Clear Skies", [None], 6, 344),
            ("Choice Scarf", None, "Clear Skies", [None], 6, 516),
            (None, None, "Clear Skies", ["Paralyzed"], 6, 172),
            ("Choice Scarf", None, "Clear Skies", ["Paralyzed"], 6, 258),
            (None, None, "Clear Skies", [None], -6, 21),
            ("Choice Scarf", None, "Clear Skies", [None], -6, 31),
            (None, None, "Clear Skies", ["Paralyzed"], -6, 10),
            ("Choice Scarf", None, "Clear Skies", ["Paralyzed"], -6, 15),
        ],
    )
    def test_calc_speed(
        self, test_frame, item, ability, weather, status, stat_mod, expected_int
    ):
        p1 = test_frame.user
        p1.item = item
        p1.ability = ability
        p1.status = status
        p1.stat_mod["speed"] = stat_mod
        test_frame.current_weather = weather
        assert calc_speed(test_frame) == expected_int

    def check_blaze(self, test_frame):
        test_frame.user.ability = "Blaze"
        assert check_blaze(test_frame) == 1
        test_frame.attack = test_frame.user.moves[0]
        test_frame.attack.type = "Fire"
        test_frame.user.stat["hp"] = 1
        assert check_blaze(test_frame) == 1.5

    # def test_calc_accuracy(self):
    #     pass

    # def test_calc_evasion(self):
    #     pass
