import pytest
from pokemon import Pokemon
import attack_verification


class TestAttackVerification:
    def test_check_flinched(self):
        p = Pokemon(
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
        assert attack_verification.check_flinched(p, "Scald", 0) == False
        p.volatile_statuses["Flinched"] = 1
        assert attack_verification.check_flinched(p, "Scald", 0) == True

    def test_choice_item(self):
        p = Pokemon(
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
        assert attack_verification.check_choice_item(p, "Scald", 0) == False
        p.volatile_statuses["Choice Locked"] = float("inf")
        assert attack_verification.check_choice_item(p, "Scald", 0) == False
        p.prev_move = "Scald"
        assert attack_verification.check_choice_item(p, "Scald", 0) == False
        assert attack_verification.check_choice_item(p, "Slack Off", 1) == True

    def test_check_encored(self):
        p = Pokemon(
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
        assert attack_verification.check_encored(p, "Scald", 0) == False
        p.volatile_statuses["Encored"] = 1
        assert attack_verification.check_encored(p, "Scald", 0) == False
        p.prev_move = "Scald"
        assert attack_verification.check_encored(p, "Scald", 0) == False
        assert attack_verification.check_encored(p, "Slack Off", 1) == True

    def test_check_taunted(self):
        p = Pokemon(
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
        assert attack_verification.check_taunted(p, "Slack Off", 1) == False
        p.volatile_statuses["Taunted"] = 1
        assert attack_verification.check_taunted(p, "Slack Off", 1) == True
        assert attack_verification.check_taunted(p, "Scald", 0) == False

    def check_disabled(self):
        p = Pokemon(
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
        assert attack_verification.check_disabled(p, "Scald", 0) == False
        p.volatile_statuses["Disabled"] = (1, "Scald", 0)
        assert attack_verification.check_disabled(p, "Scald", 0) == True
        assert attack_verification.check_disabled(p, "Slack Off", 1) == False