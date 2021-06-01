from util import *
from player import Player
from move import Move
from pokemon import Pokemon
from weather import Weather
from terrain import Terrain
from main import Frame

import pytest


class TestUtil:
    @pytest.fixture
    def test_pokemon(self):
        test_pokemon = Pokemon(
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
        return test_pokemon

    @pytest.fixture
    def test_frame(self):
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
        p1 = Player([slowbro, tyranitar])
        p2 = Player([tapu_lele, cinderace])
        w = Weather()
        t = Terrain()
        test_frame = Frame(p1, p2, None, None, w, t)
        return test_frame

    @pytest.fixture
    def test_frame2(self):
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
        p1 = Player([tapu_lele, cinderace])
        p2 = Player([slowbro, tyranitar])
        w = Weather()
        t = Terrain()
        test_frame = Frame(p1, p2, None, None, w, t)
        return test_frame

    def test_get_frame_order(self):
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
        p1.status[0] = "Paralyzed"
        assert main.check_speed(p1, 1, p2, 2) == [2, 1]
        p1.status[0] = None
        p1.stat_mod["speed"] = 4
        assert main.check_speed(p1, 1, p2, 2) == [1, 2]
        p1.status[0] = "Paralyzed"
        assert main.check_speed(p1, 1, p2, 2) == [1, 2]
        p1.status[0] = None
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
        p1.status[0] = "Paralyzed"
        assert main.check_speed(p1, 1, p2, 2) == [2, 1]
        p1.status[0] = None
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

    def test_check_priority(self, test_frame):
        test_frame.terrain.current_terrain = "Grassy Terrain"
        test_frame.attack_name = "Ice Shard"
        assert check_priority(test_frame) == 1
        test_frame.attack_name = "Avalanche"
        assert check_priority(test_frame) == -4
        test_frame.attack_name = "Tackle"
        assert check_priority(test_frame) == 0
        test_frame.attack_name = "Grassy Glide"
        assert check_priority(test_frame) == 1
        test_frame.terrain.current_terrain = "Psychic Terrain"
        test_frame.attack_name = "Ice Shard"
        assert check_priority(test_frame) == 0

    def test_roll_paralysis(self, test_pokemon):
        assert roll_paralysis(test_pokemon, 4) == False
        assert roll_paralysis(test_pokemon, 1) == True

    def test_roll_frozen(self, test_pokemon):
        test_pokemon.status[0] = "Frozen"
        assert roll_frozen(test_pokemon, 4) == True
        assert test_pokemon.status[0] == "Frozen"
        assert roll_frozen(test_pokemon, 1) == False
        assert test_pokemon.status[0] == None

    def test_roll_confusion(self, test_pokemon):
        assert roll_confusion(test_pokemon, 2) == False
        assert roll_confusion(test_pokemon, 1) == True

    def test_check_can_attack(self, test_frame):
        pass

    @pytest.mark.parametrize(
        "attack_type,target_type,expected",
        [
            ("Poison", "Steel", True),
            ("Dragon", "Fairy", True),
            ("Normal", "Ghost", True),
            ("Fighting", "Ghost", True),
            ("Ghost", "Normal", True),
            ("Electric", "Ground", True),
            ("Psychic", "Dark", True),
            ("Poison", "Fire", False),
        ],
    )
    def test_check_immunity(self, test_frame, attack_type, target_type, expected):
        test_frame.attack = test_frame.user.moves[0]
        test_frame.attack.type = attack_type
        test_frame.target.typing[0] = target_type
        assert check_immunity(test_frame) == expected

    def test_check_attack_lands(self, test_frame, test_frame2):
        test_frame.attack = test_frame.user.moves[1]
        check_attack_lands(test_frame)
        assert test_frame.attack_lands == True
        test_frame2.attack = test_frame2.user.moves[2]
        check_attack_lands(test_frame2, 100)
        assert test_frame2.attack_lands == False
        check_attack_lands(test_frame2, 20)
        assert test_frame2.attack_lands == True

    def test_apply_non_damaging_move(self, test_frame):
        test_frame.attack = test_frame.user.moves[0]
        test_frame.attack_name = "Stealth Rocks"
        apply_non_damaging_move(test_frame)
        assert test_frame.defending_team.stealth_rocks == True
        test_frame.attack_name = "Defog"
        apply_non_damaging_move(test_frame)
        assert test_frame.defending_team.stealth_rocks == False

    def test_switch(self):
        # TODO: Needs to be updated.
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
        slowbro.stat_mod["attack"] = 6
        slowbro.v_status["Confused"] = [0]
        test_player = Player([slowbro, tyranitar])
        test_player.switch(1)
        assert test_player.cur_pokemon.name == "Tyranitar"
        assert slowbro.move_lock == -1
        assert slowbro.prev_move == None
        assert slowbro.stat_mod["attack"] == 0
        assert len(slowbro.v_status) == 0
        test_player[1].stat["hp"] = 0
        test_player.switch(1)
        assert test_player.cur_pokemon.name == "Tyranitar"

    def test_apply_switch_effect(self):
        pass

    def test_apply_entry_hazards(self):
        pass

    def test_apply_stealth_rocks_damage(self):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )
        charizard = Pokemon(
            "Charizard",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )
        fearow = Pokemon(
            "Fearow",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )

        aggron = Pokemon(
            "Aggron",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )

        steelix = Pokemon(
            "Steelix",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )
        test_player = Player([slowbro, aggron, steelix, fearow, charizard])
        test_player.switch(1)
        assert test_player.current_pokemon.hp == 263
        test_player.switch(1)
        assert test_player.current_pokemon.hp == 289
        test_player.switch(2)
        assert test_player.current_pokemon.hp == 281
        test_player.switch(3)
        assert test_player.current_pokemon.hp == 203
        test_player.switch(4)
        assert test_player.current_pokemon.hp == 148

    def test_apply_post_attack_effects(self):
        pass

    def test_apply_end_of_turn_effects(self):
        pass