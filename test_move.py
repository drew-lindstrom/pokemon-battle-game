from move import Move
import pytest


class TestMove:
    def test_init_move(self):
        earthquake = Move("Earthquake")
        bulk_up = Move("Bulk Up")

        assert earthquake.type == "Ground"
        assert earthquake.category == "Physical"
        assert earthquake.power == 100
        assert earthquake.accuracy == 100
        assert earthquake.max_pp == 16
        assert earthquake.pp == 16

        assert bulk_up.type == "Fighting"
        assert bulk_up.category == "Status"
        assert bulk_up.power == 0
        assert bulk_up.accuracy == 0
        assert bulk_up.max_pp == 32
        assert bulk_up.pp == 32

    def test_pp(self):
        earthquake = Move("Earthquake")
        earthquake.pp = -5
        assert earthquake.pp == 0
        earthquake.pp = 99
        assert earthquake.pp == 16
        earthquake.pp = 7
        assert earthquake.pp == 7

    def test_check_pp(self):
        earthquake = Move("Earthquake")
        assert earthquake.check_pp() == True
        earthquake.pp = 0
        assert earthquake.check_pp() == False
        earthquake.pp = -9
        assert earthquake.check_pp() == False