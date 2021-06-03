from move_effects import *
from pokemon import Pokemon
from player import Player
from frame import Frame
from weather import Weather
from terrain import Terrain
import pytest


class TestMoveEffects:
    @pytest.fixture
    def test_frame(self):
        tapu_lele = Pokemon(
            "Tapu Lele",
            100,
            None,
            ("Psychic", "Moonblast", "Focus Blast", "Psyshock"),
            "Psychic Surge",
            "Choice Specs",
            (31, 0, 31, 31, 31, 31),
            (0, 0, 0, 252, 4, 252),
            "Timid",
        )
        cinderace = Pokemon(
            "Cinderace",
            100,
            "Male",
            ("Pyro Ball", "U-turn", "Gunk Shot", "High Jump Kick"),
            "Libero",
            "Heavy Duty Boots",
            (31, 31, 31, 31, 31, 31),
            (0, 252, 0, 0, 4, 252),
            "Jolly",
        )

        p1 = Player([tapu_lele])
        p2 = Player([cinderace])
        w = Weather()
        t = Terrain()
        test_frame = Frame(p1, p2, None, None, w, t)
        return test_frame

    def test_activate_defog(self, test_frame):
        test_frame.attacking_team.stealth_rocks == True
        test_frame.defending_team.stealth_rocks == True
        activate_defog(test_frame)
        assert test_frame.attacking_team.stealth_rocks == False
        assert test_frame.defending_team.stealth_rocks == False
        assert test_frame.target.stat_mod["evasion"] == -1

    def test_activate_roost(self, test_frame):
        test_frame.user.stat["hp"] = 30
        activate_roost(test_frame)
        assert test_frame.user.stat["hp"] == 170
        assert test_frame.user.v_status["Temporary Grounded"][0] == 1

    def test_activate_slack_off(self, test_frame):
        test_frame.user.stat["hp"] = 30
        activate_slack_off(test_frame)
        assert test_frame.user.stat["hp"] == 170

    def test_set_stealth_rocks(self, test_frame):
        set_stealth_rocks(test_frame)
        assert test_frame.defending_team.stealth_rocks == True

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
