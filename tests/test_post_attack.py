from post_attack import apply_leftovers, apply_burn, apply_bad_poison
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

    def test_apply_burn(self):
        p = Pokemon(
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

        apply_burn(p)
        assert p.stat["hp"] == 394
        p.status = ["Burned"]
        apply_burn(p)
        assert p.stat["hp"] == 369
        p.stat["hp"] = 5
        apply_burn(p)
        assert p.stat["hp"] == 0

    def test_apply_bad_poison(self):
        p = Pokemon(
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

        apply_bad_poison(p)
        assert p.stat["hp"] == 394
        p.status = ["Badly Poisoned", 14]
        apply_bad_poison(p)
        assert p.stat["hp"] == 369
        p.status = ["Badly Poisoned", 13]
        apply_bad_poison(p)
        assert p.stat["hp"] == 319
        p.stat["hp"] = 394
        p.status = ["Badly Poisoned", 0]
        apply_bad_poison(p)
        assert p.stat["hp"] == 24