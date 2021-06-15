from util import *
from player import Player
from move import Move
from pokemon import Pokemon
from weather import Weather
from terrain import Terrain
from frame import Frame

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
            "Regenerator",
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

    @pytest.mark.parametrize(
        "f1_move,f2_move,f1_switch,f2_switch,f1_status,terrain,expected_result",
        [
            (0, None, None, 1, [None], None, ["f1", "f2"]),
            (1, 0, None, None, [None], None, ["f1", "f2"]),
            (None, None, 1, 1, [None], None, ["f1", "f2"]),
            (1, None, None, 1, [None], None, ["f2", "f1"]),
            (1, 3, None, None, [None], None, ["f2", "f1"]),
            (2, 1, None, None, [None], None, ["f2", "f1"]),
            (3, 3, None, None, [None], None, ["f1", "f2"]),
            (None, None, 1, 1, ["Paralyzed"], None, ["f2", "f1"]),
            (1, 1, None, None, ["Paralyzed"], None, ["f2", "f1"]),
        ],
    )
    def test_get_frame_order(
        self,
        f1_move,
        f2_move,
        f1_switch,
        f2_switch,
        f1_status,
        terrain,
        expected_result,
    ):
        test_pokemon_1 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Pursuit", "Tackle", "Teleport", "Extreme Speed"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 252, 0, 4, 252),
            "Relaxed",
        )

        test_pokemon_2 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Pursuit", "Tackle", "Teleport", "Extreme Speed"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        player1 = Player([test_pokemon_1])
        player2 = Player([test_pokemon_2])
        t = Terrain()
        f1 = Frame(player1, player2, None, None, None, t)
        f2 = Frame(player2, player1, None, None, None, t)

        if f1_move is not None:
            f1.attack = f1.user.moves[f1_move]
        f1.switch_choice = f1_switch
        if f2_move is not None:
            f2.attack = f2.user.moves[f2_move]
        f2.switch_choice = f2_switch
        f1.status = f1_status
        t.current_terrain = terrain
        result = get_frame_order(f1, f2)
        if result == [f1, f2]:
            result = ["f1", "f2"]
        else:
            result = ["f2", "f1"]
        assert result == expected_result

    @pytest.mark.parametrize(
        "f1_speed_ev,f2_speed_ev,speed_mod,status,expected_result",
        [
            (0, 0, 0, None, ["f2", "f1"]),
            (0, 0, 0, "Paralyzed", ["f2", "f1"]),
            (0, 0, 4, None, ["f1", "f2"]),
            (0, 0, 4, "Paralyzed", ["f1", "f2"]),
            (0, 0, -4, None, ["f2", "f1"]),
            (252, 0, 0, None, ["f1", "f2"]),
            (252, 0, 0, "Paralyzed", ["f2", "f1"]),
            (252, 0, 4, None, ["f1", "f2"]),
            (252, 0, -4, None, ["f2", "f1"]),
            (0, 252, 0, None, ["f2", "f1"]),
            (0, 252, 4, None, ["f1", "f2"]),
            (0, 252, -4, None, ["f2", "f1"]),
        ],
    )
    def test_check_speed(
        self, f1_speed_ev, f2_speed_ev, speed_mod, status, expected_result
    ):
        test_pokemon_1 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, f1_speed_ev),
            "Relaxed",
        )

        test_pokemon_2 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, f2_speed_ev),
            "Relaxed",
        )
        player1 = Player([test_pokemon_1])
        player2 = Player([test_pokemon_2])
        f1 = Frame(player1, player2, None, None, None, None)
        f2 = Frame(player2, player1, None, None, None, None)

        f1.user.stat_mod["speed"] = speed_mod
        f1.user.status[0] = status
        result = check_speed(f1, f2)

        if result == [f1, f2]:
            result = ["f1", "f2"]
        else:
            result = ["f2", "f1"]

        assert result == expected_result

    @pytest.mark.parametrize(
        "terrain_name,attack_name,expected",
        [
            ("Grassy Terrain", "Ice Shard", 1),
            ("Grassy Terrain", "Avalanche", -4),
            ("Grassy Terrain", "Tackle", 0),
            ("Grassy Terrain", "Grassy Glide", 1),
            ("Psychic Terrain", "Ice Shard", 0),
        ],
    )
    def test_check_priority(self, test_frame, terrain_name, attack_name, expected):
        test_frame.terrain.current_terrain = terrain_name
        test_frame.user.set_move(0, attack_name)
        test_frame.attack = test_frame.user.moves[0]
        assert check_priority(test_frame) == expected

    @pytest.mark.parametrize("input_int,expected_bool", [(4, True), (1, False)])
    def test_roll_paralysis(self, test_pokemon, input_int, expected_bool):
        assert roll_paralysis(test_pokemon, input_int) == expected_bool

    @pytest.mark.parametrize(
        "input_int,expected_bool,expected_status",
        [(4, False, "Frozen"), (1, True, None)],
    )
    def test_roll_frozen(self, test_pokemon, input_int, expected_bool, expected_status):
        test_pokemon.status[0] = "Frozen"
        assert roll_frozen(test_pokemon, input_int) == expected_bool
        assert test_pokemon.status[0] == expected_status

    @pytest.mark.parametrize(
        "input_int,expected_bool,expected_hp", [(2, True, 394), (1, False, 375)]
    )
    def test_roll_confusion(self, test_pokemon, input_int, expected_bool, expected_hp):
        assert roll_confusion(test_pokemon, input_int) == expected_bool
        assert test_pokemon.stat["hp"] == expected_hp

    def test_calc_confusion_damage(self, test_pokemon):
        assert calc_confusion_damage(test_pokemon) == 19

    @pytest.mark.parametrize(
        "attack_type,target_type,expected",
        [
            ("Poison", "Steel", False),
            ("Dragon", "Fairy", False),
            ("Normal", "Ghost", False),
            ("Fighting", "Ghost", False),
            ("Ghost", "Normal", False),
            ("Electric", "Ground", False),
            ("Psychic", "Dark", False),
            ("Poison", "Fire", True),
        ],
    )
    def test_check_immunity(self, test_frame, attack_type, target_type, expected):
        test_frame.attack = test_frame.user.moves[0]
        test_frame.attack.type = attack_type
        test_frame.target.typing[0] = target_type
        assert check_immunity(test_frame) == expected

    def test_check_can_attack(self, test_frame):
        test_frame.attack = test_frame.user.moves[0]
        test_frame.user.status = ["Paralyzed", 2]
        assert check_can_attack(test_frame, 1) == False
        assert check_can_attack(test_frame, 2) == True
        test_frame.user.status = ["Asleep", 3]
        assert check_can_attack(test_frame) == False
        test_frame.user.status = ["Frozen", 3]
        assert check_can_attack(test_frame, 2) == False

        test_frame.user.status = [None]
        test_frame.user.v_status["Flinched"] = [2]
        assert check_can_attack(test_frame) == False
        del test_frame.user.v_status["Flinched"]
        test_frame.user.v_status["Confusion"] = [1]
        assert check_can_attack(test_frame, 1) == False
        del test_frame.user.v_status["Confusion"]
        test_frame.attack.type = "Poison"
        test_frame.target.typing[0] = "Steel"
        assert check_can_attack(test_frame) == False
        test_frame.target.typing[0] = "Water"
        assert check_can_attack(test_frame) == True
        test_frame.target.ability = "Flash Fire"
        test_frame.attack.type = "Fire"
        assert check_can_attack(test_frame) == False
        assert test_frame.target.stat_mod["attack"] == 1
        assert test_frame.target.stat_mod["sp_attack"] == 1

    def test_check_attack_lands(self, test_frame, test_frame2):
        test_frame.attack = test_frame.user.moves[1]
        check_attack_lands(test_frame)
        assert test_frame.attack_lands == True
        test_frame2.attack = test_frame2.user.moves[2]
        check_attack_lands(test_frame2, 100)
        assert test_frame2.attack_lands == False
        check_attack_lands(test_frame2, 20)
        assert test_frame2.attack_lands == True
        test_frame2.user.set_move(0, "High Jump Kick")
        test_frame2.attack = test_frame2.user.moves[0]
        check_attack_lands(test_frame2, 100)
        assert test_frame2.user.stat["hp"] == 141

    @pytest.mark.parametrize(
        "move_name,stealth_rocks,expected_bool,expected_status",
        [
            ("Stealth Rock", False, True, None),
            ("Defog", True, False, None),
            ("Toxic", False, False, "Badly Poisoned"),
        ],
    )
    def test_apply_non_damaging_move(
        self, test_frame, move_name, stealth_rocks, expected_bool, expected_status
    ):
        test_frame.user.set_move(0, move_name)
        test_frame.attack = test_frame.user.moves[0]
        test_frame.defending_team.stealth_rocks = stealth_rocks
        apply_non_damaging_move(test_frame)
        assert test_frame.defending_team.stealth_rocks == expected_bool
        assert test_frame.target.status[0] == expected_status

    def test_switch(self, test_frame):
        test_frame.user.prev_move = "Scald"
        test_frame.user.stat_mod["attack"] = 6
        test_frame.user.v_status["Confused"] = [0]
        test_frame.user.stat["hp"] = 50
        test_frame.attacking_team.stealth_rocks = True
        test_frame.switch_choice = 1
        switch(test_frame)
        test_frame.update_cur_pokemon()
        assert test_frame.user.name == "Tyranitar"
        assert test_frame.user.stat["hp"] == 354
        assert test_frame.attacking_team[1].prev_move == None
        assert test_frame.attacking_team[1].stat_mod["attack"] == 0
        assert len(test_frame.attacking_team[1].v_status) == 0
        assert test_frame.attacking_team[1].stat["hp"] == 181
        test_frame.attacking_team[1].stat["hp"] = 0
        switch(test_frame)
        test_frame.update_cur_pokemon()
        assert test_frame.user.name == "Tyranitar"

    @pytest.mark.parametrize(
        "ability_name,switch_direction,hp,expected_terrain,expected_weather,expected_attack_mod,expected_hp",
        [
            ("Grassy Surge", "In", 300, "Grassy Terrain", "Clear Skies", 0, 300),
            ("Psychic Surge", "In", 300, "Psychic Terrain", "Clear Skies", 0, 300),
            ("Intimidate", "In", 300, None, "Clear Skies", -1, 300),
            ("Sand Stream", "In", 300, None, "Sandstorm", 0, 300),
            ("Regenerator", "Out", 50, None, "Clear Skies", 0, 181),
        ],
    )
    def test_apply_switch_effect(
        self,
        test_frame,
        ability_name,
        switch_direction,
        hp,
        expected_terrain,
        expected_weather,
        expected_attack_mod,
        expected_hp,
    ):
        test_frame.user.ability = ability_name
        test_frame.user.stat["hp"] = hp
        apply_switch_effect(test_frame, 0, switch_direction)
        assert test_frame.terrain.current_terrain == expected_terrain
        assert test_frame.target.stat_mod["attack"] == expected_attack_mod
        assert test_frame.weather.current_weather == expected_weather
        assert test_frame.user.stat["hp"] == expected_hp

    @pytest.mark.parametrize(
        "item,expected_hp", [(None, 345), ("Heavy Duty Boots", 394)]
    )
    def test_apply_entry_hazards(self, test_frame, item, expected_hp):
        test_frame.attacking_team.stealth_rocks = True
        test_frame.user.item = item
        apply_entry_hazards(test_frame)
        assert test_frame.user.stat["hp"] == expected_hp

    @pytest.mark.parametrize(
        "position,expected_hp", [(0, 290), (1, 264), (2, 282), (3, 204), (4, 149)]
    )
    def test_apply_stealth_rocks_damage(self, position, expected_hp):
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
        test_frame = Frame(test_player, test_player, None, None, None, None)
        test_frame.user = test_frame.attacking_team[position]
        apply_stealth_rocks_damage(test_frame)
        assert test_frame.user.stat["hp"] == expected_hp

    def test_apply_post_attack_effects(self):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Close Combat", "Toxic", "Test Dark Pulse", "Teleport"),
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
        team1 = Player([slowbro])
        team2 = Player([tyranitar])
        test_frame = Frame(team1, team2, None, None, None, None)
        test_frame.attack = test_frame.user.moves[0]
        assert test_frame.user.stat_mod["defense"] == 0
        assert test_frame.user.stat_mod["sp_defense"] == 0
        apply_post_attack_effects(test_frame)
        assert test_frame.user.stat_mod["defense"] == -1
        assert test_frame.user.stat_mod["sp_defense"] == -1
        test_frame.attack = test_frame.user.moves[1]
        assert test_frame.target.status[0] == None
        apply_post_attack_effects(test_frame)
        assert test_frame.target.status[0] == "Badly Poisoned"
        test_frame.attack = test_frame.user.moves[2]
        assert len(test_frame.target.v_status) == 0
        apply_post_attack_effects(test_frame)
        assert test_frame.target.v_status["Flinched"] == [1]
        test_frame.target.ability = "Static"
        test_frame.attack_name = "Close Combat"
        apply_post_attack_effects(test_frame, 20)
        assert test_frame.user.status[0] == "Paralyzed"

    def test_apply_end_of_turn_effects(self, test_frame, test_frame2):
        frame_order = [test_frame, test_frame2]
        test_frame.attack = test_frame.user.moves[0]
        test_frame2.attack = test_frame2.user.moves[0]
        test_frame.weather.current_weather = "Sandstorm"
        test_frame.user.status = ["Asleep", 3]
        test_frame.user.v_status["Flinched"] = [2]
        apply_end_of_turn_effects(frame_order)
        assert test_frame.user.moves[0].pp == 23
        assert test_frame.user.stat["hp"] == 370
        assert test_frame.user.status[1] == 2
        assert test_frame.user.v_status["Flinched"] == [1]
        test_frame.user.stat["hp"] = 50
        test_frame.weather.current_weather = None
        test_frame.terrain.current_terrain = "Grassy Terrain"
        test_frame2.user.status = ["Burned", 1]
        apply_end_of_turn_effects(frame_order)
        assert test_frame.user.stat["hp"] == 74
        assert test_frame2.user.stat["hp"] == 264
        test_frame.terrain.current_terrain = None
        test_frame.user.item = "Leftovers"
        test_frame2.user.status = ["Badly Poisoned", 3]
        apply_end_of_turn_effects(frame_order)
        assert test_frame.user.stat["hp"] == 98
        assert test_frame2.user.stat["hp"] == 36
        test_frame2.user.status = ["Poisoned", 4]
        test_frame2.user.stat["hp"] = 200
        apply_end_of_turn_effects(frame_order)
        assert test_frame2.user.stat["hp"] == 165
        test_frame.user.set_move(0, "Wood Hammer")
        test_frame.attack = test_frame.user.moves[0]
        test_frame.attack_damage = 100
        assert test_frame.user.stat["hp"] == 122
        apply_end_of_turn_effects(frame_order)
        assert test_frame.user.prev_move == "Wood Hammer"
