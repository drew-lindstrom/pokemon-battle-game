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

    def test_calc_attack(self, test_frame):
        p1 = test_frame.user
        test_frame.attack = test_frame.user.moves[0]
        assert calc_attack(test_frame) == 186
        test_frame.user.ability = "Blaze"
        assert check_blaze(test_frame) == 1

        test_frame.attack.type = "Fire"
        test_frame.user.stat["hp"] = 1
        assert calc_attack(test_frame) == 279
        test_frame.user.stat["hp"] = 300
        test_frame.crit = True
        assert calc_attack(test_frame) == 186
        p1.item = "Choice Band"
        test_frame.crit = False
        assert calc_attack(test_frame) == 279

        p1.item = None
        p1.stat_mod["attack"] = 6
        assert calc_attack(test_frame) == 744
        test_frame.crit = True
        assert calc_attack(test_frame) == 744
        p1.item = "Choice Band"
        test_frame.crit = False
        assert calc_attack(test_frame) == 1116

        p1.item = None
        p1.stat_mod["attack"] = -6
        assert calc_attack(test_frame) == 46
        test_frame.crit = True
        assert calc_attack(test_frame) == 186
        p1.item = "Choice Band"
        test_frame.crit = False
        assert calc_attack(test_frame) == 69

    def test_calc_defense(self, test_frame):
        p1 = test_frame.target

        assert calc_defense(test_frame) == 350
        test_frame.crit = True
        assert calc_defense(test_frame) == 350

        p1.stat_mod["defense"] = 6
        test_frame.crit = False
        assert calc_defense(test_frame) == 1400
        test_frame.crit = True
        assert calc_defense(test_frame) == 350

        p1.stat_mod["defense"] = -6
        test_frame.crit = False
        assert calc_defense(test_frame) == 87
        test_frame.crit = True
        assert calc_defense(test_frame) == 87

    def test_calc_sp_attack(self, test_frame):
        p1 = test_frame.user
        test_frame.attack = test_frame.user.moves[0]

        assert calc_sp_attack(test_frame) == 236
        test_frame.user.ability = "Blaze"
        assert check_blaze(test_frame) == 1

        test_frame.attack.type = "Fire"
        test_frame.user.stat["hp"] = 1
        assert calc_sp_attack(test_frame) == 354
        test_frame.user.stat["hp"] = 300
        test_frame.crit = True
        assert calc_sp_attack(test_frame) == 236
        p1.item = "Choice Spec"
        test_frame.crit = False
        assert calc_sp_attack(test_frame) == 354
        test_frame.crit = True
        assert calc_sp_attack(test_frame) == 354

        p1.item = None
        p1.stat_mod["sp_attack"] = 6
        test_frame.crit = False
        assert calc_sp_attack(test_frame) == 944
        test_frame.crit = True
        assert calc_sp_attack(test_frame) == 944
        p1.item = "Choice Spec"
        test_frame.crit = False
        assert calc_sp_attack(test_frame) == 1416
        test_frame.crit = True
        assert calc_sp_attack(test_frame) == 1416

        p1.item = None
        p1.stat_mod["sp_attack"] = -6
        test_frame.crit = False
        assert calc_sp_attack(test_frame) == 59
        test_frame.crit = True
        assert calc_sp_attack(test_frame) == 236
        p1.item = "Choice Spec"
        test_frame.crit = False
        assert calc_sp_attack(test_frame) == 88
        test_frame.crit = True
        assert calc_sp_attack(test_frame) == 354

    def test_calc_sp_defense(self, test_frame):
        p1 = test_frame.target
        w = test_frame.weather

        p1.typing = ["Rock", "Psychic"]
        assert calc_sp_defense(test_frame) == 197
        test_frame.crit = True
        assert calc_sp_defense(test_frame) == 197
        w.current_weather = "Sandstorm"
        test_frame.crit = False
        assert calc_sp_defense(test_frame) == 295
        test_frame.crit = True
        assert calc_sp_defense(test_frame) == 295
        w.current_weather = "Clear Skies"
        p1.stat_mod["sp_defense"] = 6
        test_frame.crit = False
        assert calc_sp_defense(test_frame) == 788
        test_frame.crit = True
        assert calc_sp_defense(test_frame) == 197
        w.current_weather = "Sandstorm"
        test_frame.crit = False
        assert calc_sp_defense(test_frame) == 1182
        test_frame.crit = True
        assert calc_sp_defense(test_frame) == 295
        w.current_weather = "Clear Skies"
        p1.stat_mod["sp_defense"] = -6
        test_frame.crit = False
        assert calc_sp_defense(test_frame) == 49
        test_frame.crit = True
        assert calc_sp_defense(test_frame) == 49
        w.current_weather = "Sandstorm"
        test_frame.crit = False
        assert calc_sp_defense(test_frame) == 73
        test_frame.crit = True
        assert calc_sp_defense(test_frame) == 73

    def test_calc_speed(self, test_frame):
        p1 = test_frame.user
        assert calc_speed(test_frame) == 86
        p1.item = "Choice Scarf"
        assert calc_speed(test_frame) == 129
        p1.item = None
        p1.ability = "Sand Rush"
        assert calc_speed(test_frame) == 86
        test_frame.weather.current_weather = "Sandstorm"
        assert calc_speed(test_frame) == 172
        p1.ability = None
        p1.status = ["Paralyzed", 2]
        assert calc_speed(test_frame) == 43
        p1.item = "Choice Scarf"
        assert calc_speed(test_frame) == 64

        p1.item = None
        p1.status = None
        p1.stat_mod["speed"] = 6
        assert calc_speed(test_frame) == 344
        p1.item = "Choice Scarf"
        assert calc_speed(test_frame) == 516
        p1.item = None
        p1.status = ["Paralyzed", 2]
        assert calc_speed(test_frame) == 172
        p1.item = "Choice Scarf"
        assert calc_speed(test_frame) == 258

        p1.item = None
        p1.status = None
        p1.stat_mod["speed"] = -6
        assert calc_speed(test_frame) == 21
        p1.item = "Choice Scarf"
        assert calc_speed(test_frame) == 31
        p1.item = None
        p1.status = ["Paralyzed", 2]
        assert calc_speed(test_frame) == 10
        p1.item = "Choice Scarf"
        assert calc_speed(test_frame) == 15

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
