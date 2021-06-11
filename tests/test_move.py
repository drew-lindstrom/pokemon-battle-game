from move import Move
import pytest


class TestMove:
    @pytest.mark.parametrize(
        "move_name,expected_type,expected_category,expected_power,expected_accuracy,expected_max_pp,expected_pp",
        [
            ("Earthquake", "Ground", "Physical", 100, 100, 16, 16),
            ("Bulk Up", "Fighting", "Status", 0, 0, 32, 32),
        ],
    )
    def test_init_move(
        self,
        move_name,
        expected_type,
        expected_category,
        expected_power,
        expected_accuracy,
        expected_max_pp,
        expected_pp,
    ):
        attack = Move(move_name)

        assert attack.type == expected_type
        assert attack.category == expected_category
        assert attack.power == expected_power
        assert attack.accuracy == expected_accuracy
        assert attack.max_pp == expected_max_pp
        assert attack.pp == expected_pp

    @pytest.mark.parametrize(
        "move_name,input_pp,expected_pp",
        [("Earthquake", -5, 0), ("Earthquake", 99, 16), ("Earthquake", 7, 7)],
    )
    def test_pp(self, move_name, input_pp, expected_pp):
        earthquake = Move(move_name)
        earthquake.pp = input_pp
        assert earthquake.pp == expected_pp

    @pytest.mark.parametrize(
        "move_name,input_pp,expected_bool",
        [("Earthquake", 10, True), ("Earthquake", 0, False), ("Earthquake", -9, False)],
    )
    def test_check_pp(self, move_name, input_pp, expected_bool):
        earthquake = Move(move_name)
        earthquake.pp = input_pp
        assert earthquake.check_pp() == expected_bool

    def test_decrement_pp(self):
        earthquake = Move("Earthquake")
        earthquake.decrement_pp()
        assert earthquake.pp == 15