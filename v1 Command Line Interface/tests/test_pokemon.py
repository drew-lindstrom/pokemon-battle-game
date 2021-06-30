import pytest
from pokemon import Pokemon


class TestPokemon:
    @pytest.fixture
    def testPokemon(self):
        testPokemon = Pokemon(
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
        return testPokemon

    @pytest.mark.parametrize(
        "statName,expectedInt",
        [
            ("hp", 394),
            ("maxHp", 394),
            ("attack", 186),
            ("defense", 350),
            ("spAttack", 236),
            ("spDefense", 197),
            ("speed", 86),
        ],
    )
    def testInitStats(self, testPokemon, statName, expectedInt):
        p = testPokemon
        assert p.stat[statName] == expectedInt

    def testSetMove(self, testPokemon):
        testPokemon.setMove(0, "Close Combat")
        assert testPokemon.moves[0].name == "Close Combat"
        assert testPokemon.moves[0].type == "Fighting"
        assert testPokemon.moves[0].power == 120
        assert testPokemon.moves[0].accuracy == 100
        assert testPokemon.moves[0].category == "Physical"
        assert testPokemon.moves[0].maxPp == 8
        assert testPokemon.moves[0].pp == 8

    @pytest.mark.parametrize(
        "statName,inputInt,expectedInt",
        [("attack", 4, 4), ("attack", 8, 6), ("attack", -7, -6)],
    )
    def testUpdateStatModifier(self, testPokemon, statName, inputInt, expectedInt):
        p = testPokemon
        p.updateStatModifier(statName, inputInt)
        assert p.statMod[statName] == expectedInt

    def testResetStatModifier(self, testPokemon):
        p = testPokemon

        p.statMod["attack"] == 5
        p.statMod["defense"] == -4
        p.resetStatModifier()
        assert p.statMod["attack"] == 0
        assert p.statMod["defense"] == 0
        assert p.statMod["speed"] == 0

    def testCalcModifiedStat(self, testPokemon):
        p = testPokemon
        p.statMod["spAttack"] = 6
        p.statMod["attack"] = -6
        p.statMod["accuracy"] = 4
        p.statMod["evasion"] = -4
        assert p.calcModifiedStat("spAttack") == int(p.stat["spAttack"] * 4)
        assert p.calcModifiedStat("attack") == int(p.stat["attack"] / 4)
        assert p.calcModifiedStat("accuracy") == int(7 / 3 * 100)
        assert p.calcModifiedStat("evasion") == int(3 / 7 * 100)

    @pytest.mark.parametrize(
        "inputHp,healPercentage,expectedHp",
        [(150, 0.5, 347), (393, 0.5, 394), (0, 0, 0)],
    )
    def testApplyHeal(self, testPokemon, inputHp, healPercentage, expectedHp):
        p = testPokemon
        p.stat["hp"] = inputHp
        p.applyHeal(healPercentage)
        assert p.stat["hp"] == expectedHp

    @pytest.mark.parametrize(
        "inputHp,damageAmount,damagePercentage,expectedHp,expectedStatus",
        [
            (200, 50, None, 150, None),
            (35, 50, None, 0, "Fainted"),
            (394, None, 0.5, 197, None),
            (35, None, 0.5, 0, "Fainted"),
        ],
    )
    def testApplyDamage(
        self,
        testPokemon,
        inputHp,
        damageAmount,
        damagePercentage,
        expectedHp,
        expectedStatus,
    ):
        p = testPokemon
        p.stat["hp"] = inputHp
        p.applyDamage(damageAmount, damagePercentage)
        assert p.stat["hp"] == expectedHp
        assert p.status[0] == expectedStatus

    @pytest.mark.parametrize(
        "inputHp,expectedHp,expectedBool,expectedStatus",
        [(200, 200, False, None), (0, 0, True, "Fainted"), (-4, 0, True, "Fainted")],
    )
    def testCheckFainted(
        self, testPokemon, inputHp, expectedHp, expectedBool, expectedStatus
    ):
        p = testPokemon
        p.stat["hp"] = inputHp
        assert p.checkFainted() == expectedBool
        assert p.stat["hp"] == expectedHp
        assert p.status[0] == expectedStatus

    @pytest.mark.parametrize(
        "move1Pp,move2Pp,move3Pp,move4Pp,expectedBool",
        [
            (5, 5, 5, 5, False),
            (0, 5, 5, 5, False),
            (0, 0, 5, 5, False),
            (0, 0, 0, 5, False),
            (0, 0, 0, 0, True),
        ],
    )
    def testStruggleCheck(
        self, testPokemon, move1Pp, move2Pp, move3Pp, move4Pp, expectedBool
    ):
        p = testPokemon
        p.moves[0].pp = move1Pp
        p.moves[1].pp = move2Pp
        p.moves[2].pp = move3Pp
        p.moves[3].pp = move4Pp
        assert p.struggleCheck() == expectedBool

    @pytest.mark.parametrize(
        "startingStatus,inputStatus,expectedResult",
        [
            ([None, 0], None, [None, 0]),
            ([None, 0], "Paralyzed", ["Paralyzed", 0]),
            (["Paralyzed", 0], "Asleep", ["Paralyzed", 0]),
            ([None, 0], "Badly Poisoned", ["Badly Poisoned", 14]),
        ],
    )
    def testSetStatus(self, testPokemon, startingStatus, inputStatus, expectedResult):
        p = testPokemon
        p.status = startingStatus
        p.setStatus(inputStatus)
        assert p.status == expectedResult

    def testCureStatus(self, testPokemon):
        p = testPokemon
        assert p.status == [None, 0]
        p.status = ["Paralyzed", 0]
        p.cureStatus()
        assert p.status == [None, 0]

    def testSetVStatus(self, testPokemon):
        p = testPokemon
        p.setVStatus("Flinched")
        assert "Flinched" in p.vStatus
        assert p.vStatus["Flinched"] == [1]
        p.setVStatus("Confused")
        assert "Confused" in p.vStatus

    def testDecrementStatuses(self, testPokemon):
        p = testPokemon
        p.vStatus["Flinched"] = [1]
        p.vStatus["Leech Seeded"] = [float("inf")]
        p.vStatus["Confused"] = [2]
        p.vStatus["Infatuated"] = [-4]
        p.status = ["Badly Poisoned", 14]
        p.decrementStatuses()
        assert p.vStatus["Leech Seeded"] == [float("inf")]
        assert p.vStatus["Confused"] == [1]
        assert len(p.vStatus) == 2
        assert p.status == ["Badly Poisoned", 13]

    def testResetStatuses(self, testPokemon):
        p = testPokemon
        p.vStatus["Flinched"] = [3]
        p.vStatus["Leech Seeded"] = [float("inf")]
        p.status = ["Badly Poisoned", 5]
        p.resetStatuses()
        assert p.status == ["Badly Poisoned", 14]
        assert len(p.vStatus) == 0

    @pytest.mark.parametrize(
        "inputAbility,inputItem,inputVStatusName,inputVStatusNumber,expectedBool",
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
    def testCheckGrounded(
        self,
        testPokemon,
        inputAbility,
        inputItem,
        inputVStatusName,
        inputVStatusNumber,
        expectedBool,
    ):
        p = testPokemon
        p.ability = inputAbility
        p.item = inputItem
        p.vStatus[inputVStatusName] = inputVStatusNumber
        p.checkGrounded()
        assert p.grounded == expectedBool

    def testSetPrevMove(self, testPokemon):
        p = testPokemon
        assert p.prevMove == None
        p.setPreviousMove("Scald")
        assert p.prevMove == "Scald"

    def testResetPrevMove(self, testPokemon):
        p = testPokemon
        p.prevMove = "Scald"
        p.resetPreviousMove()
        assert p.prevMove == None

    def testCheckChoiceItem(self, testPokemon):
        p = testPokemon
        p.prevMove = "Slack Off"
        p.item = "Choice Scarf"
        p.checkChoiceItem()
        assert "Move Lock" in p.vStatus

    def testCheckMoveLock(self, testPokemon):
        p = testPokemon
        assert p.checkMoveLock() == False
        p.vStatus["Move Lock"] = 1
        assert p.checkMoveLock() == True
