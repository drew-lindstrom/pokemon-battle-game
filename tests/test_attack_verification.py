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

    def test_check_flinched(self, test_pokemon):
        p = test_pokemon
        assert attack_verification.check_flinched(p, "Scald", 0) == False
        p.v_status["Flinched"] = 1
        assert attack_verification.check_flinched(p, "Scald", 0) == True

    def test_choice_item(self, test_pokemon):
        p = test_pokemon
        assert attack_verification.check_choice_item(p, "Scald", 0) == False
        p.v_status["Choice Locked"] = float("inf")
        assert attack_verification.check_choice_item(p, "Scald", 0) == False
        p.prev_move = "Scald"
        assert attack_verification.check_choice_item(p, "Scald", 0) == False
        assert attack_verification.check_choice_item(p, "Slack Off", 1) == True

    def test_check_encored(self, test_pokemon):
        p = test_pokemon
        assert attack_verification.check_encored(p, "Scald", 0) == False
        p.v_status["Encored"] = 1
        assert attack_verification.check_encored(p, "Scald", 0) == False
        p.prev_move = "Scald"
        assert attack_verification.check_encored(p, "Scald", 0) == False
        assert attack_verification.check_encored(p, "Slack Off", 1) == True

    def test_check_taunted(self, test_pokemon):
        p = test_pokemon
        assert attack_verification.check_taunted(p, "Slack Off", 1) == False
        p.v_status["Taunted"] = 1
        assert attack_verification.check_taunted(p, "Slack Off", 1) == True
        assert attack_verification.check_taunted(p, "Scald", 0) == False

    def check_disabled(self, test_pokemon):
        p = test_pokemon
        assert attack_verification.check_disabled(p, "Scald", 0) == False
        p.v_status["Disabled"] = (1, "Scald", 0)
        assert attack_verification.check_disabled(p, "Scald", 0) == True
        assert attack_verification.check_disabled(p, "Slack Off", 1) == False