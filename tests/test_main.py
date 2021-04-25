import main
from pokemon import Pokemon
import pytest


class TestMain:
    def test_check_priority(self):
        assert main.check_priority("Ice Shard") == 1
        assert main.check_priority("Avalanche") == -4
        assert main.check_priority("Tackle") == 0

    def test_roll_frozen(self):
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
        assert main.roll_frozen(p, 4) == True
        assert main.roll_frozen(p, 1) == False

    def test_check_speed(self):
        p1 = Pokemon(
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

        p2 = Pokemon(
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

        assert main.check_speed(p1, 1, p2, 2) == [2, 1]
        p1.status = "Paralyzed"
        assert main.check_speed(p1, 1, p2, 2) == [2, 1]
        p1.status = None
        p1.stat_mod["speed"] = 4
        assert main.check_speed(p1, 1, p2, 2) == [1, 2]
        p1.status = "Paralyzed"
        assert main.check_speed(p1, 1, p2, 2) == [1, 2]
        p1.status = None
        p1.stat_mod["speed"] = -4
        assert main.check_speed(p1, 1, p2, 2) == [2, 1]

        p1 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 252, 0, 0, 252),
            "Relaxed",
        )
        p1.stat_mod["speed"] = 0
        assert main.check_speed(p1, 1, p2, 2) == [1, 2]
        p1.status = "Paralyzed"
        assert main.check_speed(p1, 1, p2, 2) == [2, 1]
        p1.status = None
        p1.stat_mod["speed"] = 4
        assert main.check_speed(p1, 1, p2, 2) == [1, 2]
        p1.stat_mod["speed"] = -4
        assert main.check_speed(p1, 1, p2, 2) == [2, 1]

        p1 = Pokemon(
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
        p2 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 252),
            "Relaxed",
        )
        p1.stat_mod["speed"] = 0
        assert main.check_speed(p1, 1, p2, 2) == [2, 1]
        p1.stat_mod["speed"] = 4
        assert main.check_speed(p1, 1, p2, 2) == [1, 2]
        p1.stat_mod["speed"] = -4
        assert main.check_speed(p1, 1, p2, 2) == [2, 1]

    def test_get_turn_order(self):
        p1 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 252, 0, 4, 252),
            "Relaxed",
        )

        p2 = Pokemon(
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

        assert main.get_turn_order(
            p1, ("p1", "Pursuit", 0), p2, ("p2", "Switch", 0)
        ) == [("p1", "Pursuit", 0), ("p2", "Switch", 0)]
        assert main.get_turn_order(
            p1, ("p1", "Tackle", 0), p2, ("p2", "Pursuit", 0)
        ) == [("p1", "Tackle", 0), ("p2", "Pursuit", 0)]
        assert main.get_turn_order(
            p1, ("p1", "Switch", 0), p2, ("p2", "Switch", 0)
        ) == [("p1", "Switch", 0), ("p2", "Switch", 0)]
        assert main.get_turn_order(
            p1, ("p1", "Tackle", 0), p2, ("p2", "Switch", 0)
        ) == [("p2", "Switch", 0), ("p1", "Tackle", 0)]
        assert main.get_turn_order(
            p1, ("p1", "Tackle", 0), p2, ("p2", "Extreme Speed", 0)
        ) == [("p2", "Extreme Speed", 0), ("p1", "Tackle", 0)]
        assert main.get_turn_order(
            p1, ("p1", "Teleport", 0), p2, ("p2", "Tackle", 0)
        ) == [("p2", "Tackle", 0), ("p1", "Teleport", 0)]
        assert main.get_turn_order(
            p1, ("p1", "Extreme Speed", 0), p2, ("p2", "Extreme Speed", 0)
        ) == [("p1", "Extreme Speed", 0), ("p2", "Extreme Speed", 0)]
        p1.status = "Paralyzed"
        assert main.get_turn_order(
            p1, ("p1", "Switch", 0), p2, ("p2", "Switch", 0)
        ) == [("p2", "Switch", 0), ("p1", "Switch", 0)]
        assert main.get_turn_order(
            p1, ("p1", "Tackle", 0), p2, ("p2", "Tackle", 0)
        ) == [("p2", "Tackle", 0), ("p1", "Tackle", 0)]
