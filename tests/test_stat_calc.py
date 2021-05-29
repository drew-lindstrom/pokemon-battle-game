from stat_calc import *
from pokemon import Pokemon
from player import Player
from weather import Weather
import pytest


class TestStatCalc:
    @pytest.fixture
    def test_pokemon(self):
        test_pokemon = Pokemon(
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
        return test_pokemon

    def test_calc_attack(self, test_pokemon):
        p1 = test_pokemon
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

    def test_calc_defense(self, test_pokemon):
        p1 = test_pokemon
        team = Player([p1])

        assert calc_defense(team, False) == 281
        assert calc_defense(team, True) == 281

        p1.stat_mod["defense"] = 6
        assert calc_defense(team, False) == 1124
        assert calc_defense(team, True) == 281

        p1.stat_mod["defense"] = -6
        assert calc_defense(team, False) == 70
        assert calc_defense(team, True) == 70

    def test_calc_sp_attack(self, test_pokemon):
        p1 = test_pokemon
        team = Player([p1])
        assert calc_sp_attack(team, False) == 236
        assert calc_sp_attack(team, True) == 236
        p1.item = "Choice Spec"
        assert calc_sp_attack(team, False) == 354
        assert calc_sp_attack(team, True) == 354

        p1.item = None
        p1.stat_mod["sp_attack"] = 6
        assert calc_sp_attack(team, False) == 944
        assert calc_sp_attack(team, True) == 944
        p1.item = "Choice Spec"
        assert calc_sp_attack(team, False) == 1416
        assert calc_sp_attack(team, True) == 1416

        p1.item = None
        p1.stat_mod["sp_attack"] = -6
        assert calc_sp_attack(team, False) == 59
        assert calc_sp_attack(team, True) == 236
        p1.item = "Choice Spec"
        assert calc_sp_attack(team, False) == 88
        assert calc_sp_attack(team, True) == 354

    def test_calc_sp_defense(self, test_pokemon):
        p1 = test_pokemon
        team = Player([p1])
        w = Weather()
        p1.typing = ["Rock", "Psychic"]
        assert calc_sp_defense(team, False, w) == 196
        assert calc_sp_defense(team, True, w) == 196
        w.current_weather = "Sandstorm"
        assert calc_sp_defense(team, False, w) == 294
        assert calc_sp_defense(team, True, w) == 294
        w.current_weather = "Clear Skies"
        p1.stat_mod["sp_defense"] = 6
        assert calc_sp_defense(team, False, w) == 784
        assert calc_sp_defense(team, True, w) == 196
        w.current_weather = "Sandstorm"
        assert calc_sp_defense(team, False, w) == 1176
        assert calc_sp_defense(team, True, w) == 294
        w.current_weather = "Clear Skies"
        p1.stat_mod["sp_defense"] = -6
        assert calc_sp_defense(team, False, w) == 49
        assert calc_sp_defense(team, True, w) == 49
        w.current_weather = "Sandstorm"
        assert calc_sp_defense(team, False, w) == 73
        assert calc_sp_defense(team, True, w) == 73
        w.current_weather = "Clear Skies"

    def test_calc_speed(self, test_pokemon):
        p1 = test_pokemon
        team = Player([p1])
        assert calc_speed(team, False) == 86
        p1.item = "Choice Scarf"
        assert calc_speed(team, False) == 129
        p1.item = None
        p1.ability = "Sand Rush"
        assert calc_speed(team, False) == 86
        assert calc_speed(team, False, "Sandstorm") == 172
        p1.ability = None
        p1.status = "Paralyzed"
        assert calc_speed(team, False) == 43
        p1.item = "Choice Scarf"
        assert calc_speed(team, False) == 64

        p1.item = None
        p1.status = None
        p1.stat_mod["speed"] = 6
        assert calc_speed(team, False) == 344
        p1.item = "Choice Scarf"
        assert calc_speed(team, False) == 516
        p1.item = None
        p1.status = "Paralyzed"
        assert calc_speed(team, False) == 172
        p1.item = "Choice Scarf"
        assert calc_speed(team, False) == 258

        p1.item = None
        p1.status = None
        p1.stat_mod["speed"] = -6
        assert calc_speed(team, False) == 21
        p1.item = "Choice Scarf"
        assert calc_speed(team, False) == 31
        p1.item = None
        p1.status = "Paralyzed"
        assert calc_speed(team, False) == 10
        p1.item = "Choice Scarf"
        assert calc_speed(team, False) == 15

    # def test_calc_accuracy(self):
    #     pass

    # def test_calc_evasion(self):
    #     pass
