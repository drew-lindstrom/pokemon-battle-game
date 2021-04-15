from post_attack import leftovers_check
from pokemon import Pokemon
import pytest


class TestPostAttack:
    def test_leftovers_check(self):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            "Leftovers",
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        slowbro.hp = 360
        leftovers_check(slowbro)
        assert slowbro.hp == 384
        slowbro.hp = 380
        leftovers_check(slowbro)
        assert slowbro.hp == 394
