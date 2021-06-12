from player import Player
from pokemon import Pokemon
import pytest


class TestPlayer:
    @pytest.fixture
    def test_player(self):
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

        test_player = Player([slowbro, tyranitar])
        return test_player

    @pytest.mark.parametrize(
        "pokemon_1_hp,pokemon_2_hp,expected_output",
        [(100, 100, False), (0, 100, False), (0, 0, True)],
    )
    def test_game_over_check(
        self, test_player, pokemon_1_hp, pokemon_2_hp, expected_output
    ):
        test_player[1].stat["hp"] = pokemon_1_hp
        test_player[0].stat["hp"] = pokemon_2_hp
        assert test_player.check_game_over() == expected_output

    def test_clear_hazards(self, test_player):
        test_player.spikes = 2
        test_player.tspikes = 2
        test_player.stealth_rocks = True
        test_player.sticky_web = True
        test_player.clear_hazards()
        assert test_player.spikes == 0
        assert test_player.tspikes == 0
        assert test_player.stealth_rocks == False
        assert test_player.stealth_rocks == False