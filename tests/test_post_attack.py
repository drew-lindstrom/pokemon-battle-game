from post_attack import apply_leftovers, apply_burn, apply_bad_poison
from pokemon import Pokemon
from frame import Frame
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
        frame = Frame(slowbro)
        frame.user.stat["hp"] = 360
        apply_leftovers(frame.user)
        assert frame.user.stat["hp"] == 384
        frame.user.stat["hp"] = 380
        apply_leftovers(frame.user)
        assert frame.user.stat["hp"] == 394

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
        frame = Frame(p)
        apply_burn(frame.user)
        assert frame.user.stat["hp"] == 394
        frame.user.status = ["Burned"]
        apply_burn(frame.user)
        assert frame.user.stat["hp"] == 369
        frame.user.stat["hp"] = 5
        apply_burn(frame.user)
        assert frame.user.stat["hp"] == 0

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
        frame = Frame(p)
        apply_bad_poison(frame.user)
        assert frame.user.stat["hp"] == 394
        frame.user.status = ["Badly Poisoned", 14]
        apply_bad_poison(frame.user)
        assert frame.user.stat["hp"] == 369
        frame.user.status = ["Badly Poisoned", 13]
        apply_bad_poison(frame.user)
        assert frame.user.stat["hp"] == 319
        frame.user.stat["hp"] = 394
        frame.user.status = ["Badly Poisoned", 0]
        apply_bad_poison(frame.user)
        assert frame.user.stat["hp"] == 24