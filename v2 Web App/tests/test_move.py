from move import Move
import gameText
import pytest

gameText.output = []


class TestMove:
    @pytest.mark.parametrize(
        "moveName,expectedType,expectedCategory,expectedPower,expectedAccuracy,expectedMaxPp,expectedPp",
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
        expectedMaxPp,
        expectedPp,
    ):
        attack = Move(moveName)

        assert attack.type == expectedType
        assert attack.category == expectedCategory
        assert attack.power == expectedPower
        assert attack.accuracy == expectedAccuracy
        assert attack.maxPp == expectedMaxPp
        assert attack.pp == expectedPp

    @pytest.mark.parametrize(
        "moveName,inputPp,expectedPp",
        [("Earthquake", -5, 0), ("Earthquake", 99, 16), ("Earthquake", 7, 7)],
    )
    def testPp(self, moveName, inputPp, expectedPp):
        earthquake = Move(moveName)
        earthquake.pp = inputPp
        assert earthquake.pp == expectedPp

    @pytest.mark.parametrize(
        "moveName,inputPp,expectedBool",
        [("Earthquake", 10, True), ("Earthquake", 0, False), ("Earthquake", -9, False)],
    )
    def testCheckPp(self, moveName, inputPp, expectedBool):
        earthquake = Move(moveName)
        earthquake.pp = inputPp
        assert earthquake.checkPp() == expectedBool

    def testDecrementPp(self):
        earthquake = Move("Earthquake")
        earthquake.decrementPp()
        assert earthquake.pp == 15