import pytest
from pokemon import Pokemon
import attack_verification
import gameText

gameText.output = []


class TestAttackVerification:
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
        "inputStatusName,inputStatusNumber,inputAttackName,moveNumber,expectedBool",
        [(None, None, "Scald", 0, False), ("Flinched", 1, "Scald", 0, True)],
    )
    def testCheckFlinched(
        self,
        testPokemon,
        inputStatusName,
        inputStatusNumber,
        inputAttackName,
        moveNumber,
        expectedBool,
    ):
        p = testPokemon
        p.vStatus[inputStatusName] = inputStatusNumber
        assert (
            attack_verification.checkFlinched(p, inputAttackName, moveNumber)
            == expectedBool
        )

    @pytest.mark.parametrize(
        "inputStatusName,inputStatusNumber,inputAttackName,moveNumber,previousMove,expectedBool",
        [
            (None, None, "Scald", 0, None, False),
            ("Choice Locked", float("inf"), "Scald", 0, None, False),
            ("Choice Locked", float("inf"), "Scald", 0, "Scald", False),
            ("Choice Locked", float("inf"), "Slack Off", 1, "Scald", True),
        ],
    )
    def testChoiceItem(
        self,
        testPokemon,
        inputStatusName,
        inputStatusNumber,
        inputAttackName,
        moveNumber,
        previousMove,
        expectedBool,
    ):
        p = testPokemon
        p.vStatus[inputStatusName] = inputStatusNumber
        p.prevMove = previousMove
        assert (
            attack_verification.checkChoiceItem(p, inputAttackName, moveNumber)
            == expectedBool
        )

    @pytest.mark.parametrize(
        "inputStatusName,inputStatusNumber,inputAttackName,moveNumber,previousMove,expectedBool",
        [
            (None, None, "Scald", 0, None, False),
            ("Encored", 1, "Scald", 0, None, False),
            ("Encored", 1, "Scald", 0, "Scald", False),
            ("Encored", 1, "Slack Off", 1, "Scald", True),
        ],
    )
    def testCheckEncored(
        self,
        testPokemon,
        inputStatusName,
        inputStatusNumber,
        inputAttackName,
        moveNumber,
        previousMove,
        expectedBool,
    ):
        p = testPokemon
        p.vStatus[inputStatusName] = inputStatusNumber
        p.prevMove = previousMove
        assert (
            attack_verification.checkEncored(p, inputAttackName, moveNumber)
            == expectedBool
        )

    @pytest.mark.parametrize(
        "inputStatusName,inputStatusNumber,inputAttackName,moveNumber,expectedBool",
        [(None, None, "Scald", 0, False), ("Taunted", 1, "Slack Off", 1, True)],
    )
    def testCheckTaunted(
        self,
        testPokemon,
        inputStatusName,
        inputStatusNumber,
        inputAttackName,
        moveNumber,
        expectedBool,
    ):
        p = testPokemon
        p.vStatus[inputStatusName] = inputStatusNumber
        assert (
            attack_verification.checkTaunted(p, inputAttackName, moveNumber)
            == expectedBool
        )

    @pytest.mark.parametrize(
        "inputStatusName,inputStatusNumber,inputAttackName,moveNumber,expectedBool",
        [
            (None, None, "Scald", 0, False),
            ("Disabled", (1, "Scald", 0), "Scald", 0, True),
            ("Disabled", (1, "Scald", 0), "Slack Off", 0, False),
        ],
    )
    def testCheckDisabled(
        self,
        testPokemon,
        inputStatusName,
        inputStatusNumber,
        inputAttackName,
        moveNumber,
        expectedBool,
    ):
        p = testPokemon
        p.vStatus[inputStatusName] = inputStatusNumber
        assert (
            attack_verification.checkDisabled(p, inputAttackName, moveNumber)
            == expectedBool
        )
