import pytest
from pokemon import Pokemon


class TestPokemon:
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

    @pytest.mark.parametrize(
        "stat_name,expected_int",
        [
            ("hp", 394),
            ("max_hp", 394),
            ("attack", 186),
            ("defense", 350),
            ("sp_attack", 236),
            ("sp_defense", 197),
            ("speed", 86),
        ],
    )
    def test_init_stats(self, test_pokemon, stat_name, expected_int):
        p = test_pokemon
        assert p.stat[stat_name] == expected_int

    def test_set_move(self, test_pokemon):
        test_pokemon.set_move(0, "Close Combat")
        assert test_pokemon.moves[0].name == "Close Combat"
        assert test_pokemon.moves[0].type == "Fighting"
        assert test_pokemon.moves[0].power == 120
        assert test_pokemon.moves[0].accuracy == 100
        assert test_pokemon.moves[0].category == "Physical"
        assert test_pokemon.moves[0].max_pp == 8
        assert test_pokemon.moves[0].pp == 8

    @pytest.mark.parametrize(
        "stat_name,input_int,expected_int",
        [("attack", 4, 4), ("attack", 8, 6), ("attack", -7, -6)],
    )
    def test_update_stat_modifier(
        self, test_pokemon, stat_name, input_int, expected_int
    ):
        p = test_pokemon
        p.update_stat_modifier(stat_name, input_int)
        assert p.stat_mod[stat_name] == expected_int

    def test_reset_stat_modifier(self, test_pokemon):
        p = test_pokemon

        p.stat_mod["attack"] == 5
        p.stat_mod["defense"] == -4
        p.reset_stat_modifier()
        assert p.stat_mod["attack"] == 0
        assert p.stat_mod["defense"] == 0
        assert p.stat_mod["speed"] == 0

    def test_calc_modified_stat(self, test_pokemon):
        p = test_pokemon
        p.stat_mod["sp_attack"] = 6
        p.stat_mod["attack"] = -6
        p.stat_mod["accuracy"] = 4
        p.stat_mod["evasion"] = -4
        assert p.calc_modified_stat("sp_attack") == int(p.stat["sp_attack"] * 4)
        assert p.calc_modified_stat("attack") == int(p.stat["attack"] / 4)
        assert p.calc_modified_stat("accuracy") == int(7 / 3 * 100)
        assert p.calc_modified_stat("evasion") == int(3 / 7 * 100)

    @pytest.mark.parametrize(
        "input_hp,heal_percentage,expected_hp",
        [(150, 0.5, 347), (393, 0.5, 394), (0, 0, 0)],
    )
    def test_apply_heal(self, test_pokemon, input_hp, heal_percentage, expected_hp):
        p = test_pokemon
        p.stat["hp"] = input_hp
        p.apply_heal(heal_percentage)
        assert p.stat["hp"] == expected_hp

    @pytest.mark.parametrize(
        "input_hp,damage_amount,damage_percentage,expected_hp,expected_status",
        [
            (200, 50, None, 150, None),
            (35, 50, None, 0, "Fainted"),
            (394, None, 0.5, 197, None),
            (35, None, 0.5, 0, "Fainted"),
        ],
    )
    def test_apply_damage(
        self,
        test_pokemon,
        input_hp,
        damage_amount,
        damage_percentage,
        expected_hp,
        expected_status,
    ):
        p = test_pokemon
        p.stat["hp"] = input_hp
        p.apply_damage(damage_amount, damage_percentage)
        assert p.stat["hp"] == expected_hp
        assert p.status[0] == expected_status

    @pytest.mark.parametrize(
        "input_hp,expected_hp,expected_bool,expected_status",
        [(200, 200, False, None), (0, 0, True, "Fainted"), (-4, 0, True, "Fainted")],
    )
    def test_check_fainted(
        self, test_pokemon, input_hp, expected_hp, expected_bool, expected_status
    ):
        p = test_pokemon
        p.stat["hp"] = input_hp
        assert p.check_fainted() == expected_bool
        assert p.stat["hp"] == expected_hp
        assert p.status[0] == expected_status

    @pytest.mark.parametrize(
        "move_1_pp,move_2_pp,move_3_pp,move_4_pp,expected_bool",
        [
            (5, 5, 5, 5, False),
            (0, 5, 5, 5, False),
            (0, 0, 5, 5, False),
            (0, 0, 0, 5, False),
            (0, 0, 0, 0, True),
        ],
    )
    def test_struggle_check(
        self, test_pokemon, move_1_pp, move_2_pp, move_3_pp, move_4_pp, expected_bool
    ):
        p = test_pokemon
        p.moves[0].pp = move_1_pp
        p.moves[1].pp = move_2_pp
        p.moves[2].pp = move_3_pp
        p.moves[3].pp = move_4_pp
        assert p.struggle_check() == expected_bool

    @pytest.mark.parametrize(
        "starting_status,input_status,expected_result",
        [
            ([None, 0], None, [None, 0]),
            ([None, 0], "Paralyzed", ["Paralyzed", 0]),
            (["Paralyzed", 0], "Asleep", ["Paralyzed", 0]),
            ([None, 0], "Badly Poisoned", ["Badly Poisoned", 14]),
        ],
    )
    def test_set_status(
        self, test_pokemon, starting_status, input_status, expected_result
    ):
        p = test_pokemon
        p.status = starting_status
        p.set_status(input_status)
        assert p.status == expected_result

    def test_cure_status(self, test_pokemon):
        p = test_pokemon
        assert p.status == [None, 0]
        p.status = ["Paralyzed", 0]
        p.cure_status()
        assert p.status == [None, 0]

    def test_set_v_status(self, test_pokemon):
        p = test_pokemon
        p.set_v_status("Flinched")
        assert "Flinched" in p.v_status
        assert p.v_status["Flinched"] == [1]
        p.set_v_status("Confused")
        assert "Confused" in p.v_status

    def test_decrement_statuses(self, test_pokemon):
        p = test_pokemon
        p.v_status["Flinched"] = [1]
        p.v_status["Leech Seeded"] = [float("inf")]
        p.v_status["Confused"] = [2]
        p.v_status["Infatuated"] = [-4]
        p.status = ["Badly Poisoned", 14]
        p.decrement_statuses()
        assert p.v_status["Leech Seeded"] == [float("inf")]
        assert p.v_status["Confused"] == [1]
        assert len(p.v_status) == 2
        assert p.status == ["Badly Poisoned", 13]

    def test_reset_statuses(self, test_pokemon):
        p = test_pokemon
        p.v_status["Flinched"] = [3]
        p.v_status["Leech Seeded"] = [float("inf")]
        p.status = ["Badly Poisoned", 5]
        p.reset_statuses()
        assert p.status == ["Badly Poisoned", 14]
        assert len(p.v_status) == 0

    @pytest.mark.parametrize(
        "input_ability,input_item,input_v_status_name,input_v_status_number,expected_bool",
        [
            (None, None, None, None, True),
            ("Levitate", None, None, None, False),
            ("Levitate", "Iron Ball", None, None, True),
            (None, "Air Balloon", None, None, False),
            (None, "Air Balloon", "Ingrained", [1], True),
            (None, None, "Magnet Rise", [4], False),
            (None, None, "Telekinesis", [3], False),
        ],
    )
    def test_check_grounded(
        self,
        test_pokemon,
        input_ability,
        input_item,
        input_v_status_name,
        input_v_status_number,
        expected_bool,
    ):
        p = test_pokemon
        p.ability = input_ability
        p.item = input_item
        p.v_status[input_v_status_name] = input_v_status_number
        p.check_grounded()
        assert p.grounded == expected_bool

    def test_set_prev_move(self, test_pokemon):
        p = test_pokemon
        assert p.prev_move == None
        p.set_previous_move("Scald")
        assert p.prev_move == "Scald"

    def test_reset_prev_move(self, test_pokemon):
        p = test_pokemon
        p.prev_move = "Scald"
        p.reset_previous_move()
        assert p.prev_move == None

    def test_check_choice_item(self, test_pokemon):
        p = test_pokemon
        p.prev_move = "Slack Off"
        p.item = "Choice Scarf"
        p.check_choice_item()
        assert "Move Lock" in p.v_status

    def test_check_move_lock(self, test_pokemon):
        p = test_pokemon
        assert p.check_move_lock() == False
        p.v_status["Move Lock"] = 1
        assert p.check_move_lock() == True
