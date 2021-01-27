from team import Team, game_over_check
from pokemon import Pokemon
import pytest


class TestTeam:
    def test_switch(self):
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

        test_player = Team([slowbro, tyranitar])
        test_player.switch(1)
        assert test_player.current_pokemon.name == "Tyranitar"
        test_player[1].hp = 0
        test_player.switch(1)
        assert test_player.current_pokemon.name == "Tyranitar"

    def test_game_over_check(self):
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

        test_player = Team([slowbro, tyranitar])
        assert game_over_check(test_player) == 1
        test_player[1].hp = 0
        assert game_over_check(test_player) == 1
        test_player[0].hp = 0
        assert game_over_check(test_player) == 0
