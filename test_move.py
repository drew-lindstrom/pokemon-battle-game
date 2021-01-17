from move import Move
import pytest


class TestMove:
    def test_check_pp(self):
        earthquake = Move("Earthquake")
        assert earthquake.check_pp() == True
        earthquake.pp = 0
        assert earthquake.check_pp() == False
        earthquake.pp = -9
        assert earthquake.check_pp() == False