from player import (
    Player,
    game_over_check,
    set_light_screen,
    set_reflect,
    reset_light_screen,
    reset_reflect,
    set_stealth_rocks,
    set_spike,
    set_tspike,
    set_sticky_web,
    clear_hazards,
)
from pokemon import Pokemon
import pytest


class TestPlayer:
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

        test_player = Player([slowbro, tyranitar])
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

        test_player = Player([slowbro, tyranitar])
        assert game_over_check(test_player) == 1
        test_player[1].hp = 0
        assert game_over_check(test_player) == 1
        test_player[0].hp = 0
        assert game_over_check(test_player) == 0

    def test_set_light_screen_and_reset_light_screen(self):
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
        test_player = Player([slowbro])

        set_light_screen(test_player)
        assert test_player.light_screen == True
        assert test_player.light_screen_counter == 5
        test_player.light_screen_counter = 0
        reset_light_screen(test_player)
        assert test_player.light_screen == False
        slowbro.item = "Light Clay"
        set_light_screen(test_player)
        assert test_player.light_screen_counter == 8

    def test_set_reflect_and_reset_reflect(self):
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
        test_player = Player([slowbro])

        set_reflect(test_player)
        assert test_player.reflect == True
        assert test_player.reflect_counter == 5
        test_player.reflect_counter = 0
        reset_reflect(test_player)
        assert test_player.reflect == False
        slowbro.item = "Light Clay"
        set_reflect(test_player)
        assert test_player.reflect_counter == 8

    def test_set_stealth_rocks(self):
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
        test_player = Player([slowbro])

        set_stealth_rocks(test_player)
        assert test_player.stealth_rocks == True

    def test_set_spike(self):
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
        test_player = Player([slowbro])

        set_spike(test_player)
        assert test_player.spikes == 1
        set_spike(test_player)
        assert test_player.spikes == 2
        set_spike(test_player)
        set_spike(test_player)
        assert test_player.spikes == 3

    def test_set_tspike(self):
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

        test_player = Player([slowbro])

        set_tspike(test_player)
        assert test_player.tspikes == 1
        set_tspike(test_player)
        assert test_player.tspikes == 2
        set_tspike(test_player)
        assert test_player.tspikes == 2

    def test_set_sticky_web(self):
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
        test_player = Player([slowbro])

        set_sticky_web(test_player)
        assert test_player.sticky_web == True

    def test_clear_hazards(self):
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

        test_player = Player([slowbro])

        test_player.spikes = 2
        test_player.tspikes = 2
        test_player.stealth_rocks = True
        test_player.sticky_web = True
        clear_hazards(test_player)
        assert test_player.spikes == 0
        assert test_player.tspikes == 0
        assert test_player.stealth_rocks == False
        assert test_player.stealth_rocks == False