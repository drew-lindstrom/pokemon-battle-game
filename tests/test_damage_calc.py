from player import Player
from pokemon import Pokemon
from move import Move
import damage_calc
import pytest


class TestDamageCalc:
    def test_roll_crit(self):
        assert damage_calc.roll_crit(1) == 1.5
        assert damage_calc.roll_crit(2) == 1

    def test_check_stab(self):
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
        scald = Move("Scald")
        future_sight = Move("Future Sight")
        earthquake = Move("Earthquake")
        assert damage_calc.check_stab(slowbro, scald) == 1.5
        assert damage_calc.check_stab(slowbro, future_sight) == 1.5
        assert damage_calc.check_stab(slowbro, earthquake) == 1

    def test_check_type_effectiveness(self):
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
        scald = Move("Scald")
        future_sight = Move("Future Sight")
        slack_off = Move("Slack Off")
        assert damage_calc.check_type_effectiveness(slowbro, tyranitar, scald) == 2
        assert (
            damage_calc.check_type_effectiveness(slowbro, tyranitar, future_sight) == 0
        )
        assert (
            damage_calc.check_type_effectiveness(slowbro, tyranitar, slack_off) == 0.5
        )

    def test_roll_random(self):
        assert damage_calc.roll_random(85) == 0.85

    def test_activate_defog(self):
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
        player1 = Player([slowbro])
        player2 = Player([tyranitar])
        player1.stealth_rocks = True
        player2.stealth_rocks = True
        damage_calc.activate_defog(player1, player2)
        assert player1.stealth_rocks == False
        assert player2.stealth_rocks == False
        assert player2.cur_pokemon.stat["evasion"] == -1