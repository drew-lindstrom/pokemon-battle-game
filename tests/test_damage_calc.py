from player import Player
from pokemon import Pokemon
import damage_calc
import pytest


def testDamageCalc():
    def test_roll_crit(self):
        assert damage_calc.roll_crit(1) == 1.5
        assert damage_calc.roll_crit(2) == 1

    def check_stab(self):
        pass

    def check_type_effectiveness(self):
        pass

    def test_roll_random(self):
        pass

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