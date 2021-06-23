from move import Move
import pytest


class TestMove:
    @pytest.mark.parametrize(
        "moveName,expectedType,expectedCategory,expectedPower,expectedAccuracy,expectedMaxPP,expectedPP",
        [
            ("Earthquake", "Ground", "Physical", 100, 100, 16, 16),
            ("Bulk Up", "Fighting", "Status", 0, 0, 32, 32),
        ],
    )
    def testInitMove(
        self,
        moveName,
        expectedType,
        expectedCategory,
        expectedPower,
        expectedAccuracy,
        expectedMaxPP,
        expectedPP,
    ):
        attack = Move(moveName)

        assert attack.type == expectedType
        assert attack.category == expectedCategory
        assert attack.power == expectedPower
        assert attack.accuracy == expectedAccuracy
        assert attack.maxPP == expectedMaxPP
        assert attack.PP == expectedPP

    @pytest.mark.parametrize(
        "moveName,inputPP,expectedPP",
        [("Earthquake", -5, 0), ("Earthquake", 99, 16), ("Earthquake", 7, 7)],
    )
    def testPP(self, moveName, inputPP, expectedPP):
        earthquake = Move(moveName)
        earthquake.PP = inputPP
        assert earthquake.PP == expectedPP

    @pytest.mark.parametrize(
        "moveName,inputPP,expectedBool",
        [("Earthquake", 10, True), ("Earthquake", 0, False), ("Earthquake", -9, False)],
    )
    def testCheckPP(self, moveName, inputPP, expectedBool):
        earthquake = Move(moveName)
        earthquake.PP = inputPP
        assert earthquake.checkPP() == expectedBool

    def testDecrementPP(self):
        earthquake = Move("Earthquake")
        earthquake.decrementPP()
        assert earthquake.PP == 15