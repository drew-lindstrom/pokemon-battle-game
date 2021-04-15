from post_attack import apply_leftovers
from pokemon import Pokemon
import pytest


class TestPostAttack:
    def test_apply_leftovers(self):
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
        slowbro.stat["hp"] = 360
        apply_leftovers(slowbro)
        assert slowbro.stat["hp"] == 384
        slowbro.hp = 380
        apply_leftovers(slowbro)
        assert slowbro.stat["hp"] == 394
