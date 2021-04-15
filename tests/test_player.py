from player import Player
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
        slowbro.move_lock = 1
        slowbro.prev_move = "Scald"
        test_player = Player([slowbro, tyranitar])
        test_player.switch(1)
        assert test_player.cur_pokemon.name == "Tyranitar"
        assert slowbro.move_lock == -1
        assert slowbro.prev_move == None
        test_player[1].stat["hp"] = 0
        test_player.switch(1)
        assert test_player.cur_pokemon.name == "Tyranitar"

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
        assert test_player.game_over_check() == False
        test_player[1].stat["hp"] = 0
        assert test_player.game_over_check() == False
        test_player[0].stat["hp"] = 0
        assert test_player.game_over_check() == True

    # def test_set_light_screen_and_reset_light_screen(self):
    #     slowbro = Pokemon(
    #         "Slowbro",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (252, 0, 252, 0, 4, 0),
    #         "Relaxed",
    #     )
    #     test_player = Player([slowbro])

    #     set_light_screen(test_player)
    #     assert test_player.light_screen == True
    #     assert test_player.light_screen_counter == 5
    #     test_player.light_screen_counter = 0
    #     reset_light_screen(test_player)
    #     assert test_player.light_screen == False
    #     slowbro.item = "Light Clay"
    #     set_light_screen(test_player)
    #     assert test_player.light_screen_counter == 8

    # def test_set_reflect_and_reset_reflect(self):
    #     slowbro = Pokemon(
    #         "Slowbro",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (252, 0, 252, 0, 4, 0),
    #         "Relaxed",
    #     )
    #     test_player = Player([slowbro])

    #     set_reflect(test_player)
    #     assert test_player.reflect == True
    #     assert test_player.reflect_counter == 5
    #     test_player.reflect_counter = 0
    #     reset_reflect(test_player)
    #     assert test_player.reflect == False
    #     slowbro.item = "Light Clay"
    #     set_reflect(test_player)
    #     assert test_player.reflect_counter == 8

    # def test_set_stealth_rocks(self):
    #     slowbro = Pokemon(
    #         "Slowbro",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (252, 0, 252, 0, 4, 0),
    #         "Relaxed",
    #     )
    #     test_player = Player([slowbro])

    #     set_stealth_rocks(test_player)
    #     assert test_player.stealth_rocks == True

    # def test_set_spike(self):
    #     slowbro = Pokemon(
    #         "Slowbro",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (252, 0, 252, 0, 4, 0),
    #         "Relaxed",
    #     )
    #     test_player = Player([slowbro])

    #     set_spike(test_player)
    #     assert test_player.spikes == 1
    #     set_spike(test_player)
    #     assert test_player.spikes == 2
    #     set_spike(test_player)
    #     set_spike(test_player)
    #     assert test_player.spikes == 3

    # def test_set_tspike(self):
    #     slowbro = Pokemon(
    #         "Slowbro",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (252, 0, 252, 0, 4, 0),
    #         "Relaxed",
    #     )

    #     test_player = Player([slowbro])

    #     set_tspike(test_player)
    #     assert test_player.tspikes == 1
    #     set_tspike(test_player)
    #     assert test_player.tspikes == 2
    #     set_tspike(test_player)
    #     assert test_player.tspikes == 2

    # def test_set_sticky_web(self):
    #     slowbro = Pokemon(
    #         "Slowbro",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (252, 0, 252, 0, 4, 0),
    #         "Relaxed",
    #     )
    #     test_player = Player([slowbro])

    #     set_sticky_web(test_player)
    #     assert test_player.sticky_web == True

    # def test_apply_stealth_rocks_damage(self):
    #     slowbro = Pokemon(
    #         "Slowbro",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (0, 0, 0, 0, 0, 0),
    #         "Relaxed",
    #     )
    #     charizard = Pokemon(
    #         "Charizard",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (0, 0, 0, 0, 0, 0),
    #         "Relaxed",
    #     )
    #     fearow = Pokemon(
    #         "Fearow",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (0, 0, 0, 0, 0, 0),
    #         "Relaxed",
    #     )

    #     aggron = Pokemon(
    #         "Aggron",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (0, 0, 0, 0, 0, 0),
    #         "Relaxed",
    #     )

    #     steelix = Pokemon(
    #         "Steelix",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (0, 0, 0, 0, 0, 0),
    #         "Relaxed",
    #     )
    #     test_player = Player([slowbro, aggron, steelix, fearow, charizard])
    #     test_player.switch(1)
    #     assert test_player.current_pokemon.hp == 263
    #     test_player.switch(1)
    #     assert test_player.current_pokemon.hp == 289
    #     test_player.switch(2)
    #     assert test_player.current_pokemon.hp == 281
    #     test_player.switch(3)
    #     assert test_player.current_pokemon.hp == 203
    #     test_player.switch(4)
    #     assert test_player.current_pokemon.hp == 148

    # def test_clear_hazards(self):
    #     slowbro = Pokemon(
    #         "Slowbro",
    #         100,
    #         "Male",
    #         ("Scald", "Slack Off", "Future Sight", "Teleport"),
    #         None,
    #         None,
    #         (31, 31, 31, 31, 31, 31),
    #         (252, 0, 252, 0, 4, 0),
    #         "Relaxed",
    #     )

    #     test_player = Player([slowbro])

    #     test_player.spikes = 2
    #     test_player.tspikes = 2
    #     test_player.stealth_rocks = True
    #     test_player.sticky_web = True
    #     clear_hazards(test_player)
    #     assert test_player.spikes == 0
    #     assert test_player.tspikes == 0
    #     assert test_player.stealth_rocks == False
    #     assert test_player.stealth_rocks == False