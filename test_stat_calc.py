from stat_calc import (
    calc_attack,
    calc_defense,
    calc_sp_attack,
    calc_sp_defense,
    calc_speed,
    calc_accuracy,
    calc_evasion,
)
from pokemon import Pokemon
from player import Player
import pytest


class TestStatCalc:
    def test_calc_attack(self):
        p1 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )
        team = Player([p1])
        assert calc_attack(team, False) == 186
        assert calc_attack(team, True) == 186
        p1.item = "Choice Band"
        assert calc_attack(team, False) == 279
        p1.item = None
        p1.status = "Burn"
        assert calc_attack(team, False) == 93
        p1.item = "Choice Band"
        assert calc_attack(team, False) == 139
        assert calc_attack(team, True) == 139

        p1.item = None
        p1.status = None
        p1.stat_mod["attack"] = 6
        assert calc_attack(team, False) == 744
        assert calc_attack(team, True) == 744
        p1.item = "Choice Band"
        assert calc_attack(team, False) == 1116
        p1.item = None
        p1.status = "Burn"
        assert calc_attack(team, False) == 372
        p1.item = "Choice Band"
        assert calc_attack(team, False) == 558
        assert calc_attack(team, True) == 558

        p1.item = None
        p1.status = None
        p1.stat_mod["attack"] = -6
        assert calc_attack(team, False) == 46
        assert calc_attack(team, True) == 186
        p1.item = "Choice Band"
        assert calc_attack(team, False) == 69
        p1.item = None
        p1.status = "Burn"
        assert calc_attack(team, False) == 23
        p1.item = "Choice Band"
        assert calc_attack(team, False) == 34
        assert calc_attack(team, True) == 139

    def test_calc_defense(self):
        p1 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )
        team = Player([p1])
        assert calc_defense(team, False) == 281
        assert calc_defense(team, True) == 281
        p1.stat_mod["defense"] = 6
        assert calc_defense(team, False) == 1124
        assert calc_defense(team, True) == 281
        p1.stat_mod["defense"] = -6
        assert calc_defense(team, False) == 70
        assert calc_defense(team, True) == 70

    def test_calc_sp_attack(self):
        pass

    def test_calc_sp_defense(self):
        p1 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )
        team = Player([p1])
        assert calc_sp_defense(team, False) == 196
        assert calc_sp_defense(team, True) == 196
        p1.stat_mod["sp_defense"] = 6
        assert calc_sp_defense(team, False) == 784
        assert calc_sp_defense(team, True) == 196
        p1.stat_mod["sp_defense"] = -6
        assert calc_sp_defense(team, False) == 49
        assert calc_sp_defense(team, True) == 49

    def test_calc_speed(self):
        pass

    def test_calc_accuracy(self):
        pass

    def test_calc_evasion(self):
        pass
