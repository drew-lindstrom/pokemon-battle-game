import pytest
from pokemon import Pokemon
import attack_verification


class TestAttackVerification:
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
        "input_status_name,input_status_number,input_attack_name,move_number,expected_bool",
        [(None, None, "Scald", 0, False), ("Flinched", 1, "Scald", 0, True)],
    )
    def test_check_flinched(
        self,
        test_pokemon,
        input_status_name,
        input_status_number,
        input_attack_name,
        move_number,
        expected_bool,
    ):
        p = test_pokemon
        p.v_status[input_status_name] = input_status_number
        assert (
            attack_verification.check_flinched(p, input_attack_name, move_number)
            == expected_bool
        )

    @pytest.mark.parametrize(
        "input_status_name,input_status_number,input_attack_name,move_number,previous_move,expected_bool",
        [
            (None, None, "Scald", 0, None, False),
            ("Choice Locked", float("inf"), "Scald", 0, None, False),
            ("Choice Locked", float("inf"), "Scald", 0, "Scald", False),
            ("Choice Locked", float("inf"), "Slack Off", 1, "Scald", True),
        ],
    )
    def test_choice_item(
        self,
        test_pokemon,
        input_status_name,
        input_status_number,
        input_attack_name,
        move_number,
        previous_move,
        expected_bool,
    ):
        p = test_pokemon
        p.v_status[input_status_name] = input_status_number
        p.prev_move = previous_move
        assert (
            attack_verification.check_choice_item(p, input_attack_name, move_number)
            == expected_bool
        )

    @pytest.mark.parametrize(
        "input_status_name,input_status_number,input_attack_name,move_number,previous_move,expected_bool",
        [
            (None, None, "Scald", 0, None, False),
            ("Encored", 1, "Scald", 0, None, False),
            ("Encored", 1, "Scald", 0, "Scald", False),
            ("Encored", 1, "Slack Off", 1, "Scald", True),
        ],
    )
    def test_check_encored(
        self,
        test_pokemon,
        input_status_name,
        input_status_number,
        input_attack_name,
        move_number,
        previous_move,
        expected_bool,
    ):
        p = test_pokemon
        p.v_status[input_status_name] = input_status_number
        p.prev_move = previous_move
        assert (
            attack_verification.check_encored(p, input_attack_name, move_number)
            == expected_bool
        )

    @pytest.mark.parametrize(
        "input_status_name,input_status_number,input_attack_name,move_number,expected_bool",
        [(None, None, "Scald", 0, False), ("Taunted", 1, "Slack Off", 1, True)],
    )
    def test_check_taunted(
        self,
        test_pokemon,
        input_status_name,
        input_status_number,
        input_attack_name,
        move_number,
        expected_bool,
    ):
        p = test_pokemon
        p.v_status[input_status_name] = input_status_number
        assert (
            attack_verification.check_taunted(p, input_attack_name, move_number)
            == expected_bool
        )

    @pytest.mark.parametrize(
        "input_status_name,input_status_number,input_attack_name,move_number,expected_bool",
        [
            (None, None, "Scald", 0, False),
            ("Disabled", (1, "Scald", 0), "Scald", 0, True),
            ("Disabled", (1, "Scald", 0), "Slack Off", 0, False),
        ],
    )
    def test_check_disabled(
        self,
        test_pokemon,
        input_status_name,
        input_status_number,
        input_attack_name,
        move_number,
        expected_bool,
    ):
        p = test_pokemon
        p.v_status[input_status_name] = input_status_number
        assert (
            attack_verification.check_disabled(p, input_attack_name, move_number)
            == expected_bool
        )
