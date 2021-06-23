from util import *
from player import Player
from move import Move
from pokemon import Pokemon
from weather import Weather
from terrain import Terrain
from frame import Frame

import pytest


class TestUtil:
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

    @pytest.fixture
    def testFrame(self):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            "Regenerator",
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        tyranitar = Pokemon(
            "Tyranitar",
            100,
            "Male",
            ("Crunch", "Stealth Rock", "Toxic", "Earthquake"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 0, 0, 216, 40),
            "Careful",
        )
        tapuLele = Pokemon(
            "Tapu Lele",
            100,
            None,
            ("Psychic", "Moonblast", "Focus Blast", "Psyshock"),
            "Psychic Surge",
            "Choice Specs",
            (31, 0, 31, 31, 31, 31),
            (0, 0, 0, 252, 4, 252),
            "Timid",
        )
        cinderace = Pokemon(
            "Cinderace",
            100,
            "Male",
            ("Pyro Ball", "U-turn", "Gunk Shot", "High Jump Kick"),
            "Libero",
            "Heavy Duty Boots",
            (31, 31, 31, 31, 31, 31),
            (0, 252, 0, 0, 4, 252),
            "Jolly",
        )
        p1 = Player([slowbro, tyranitar])
        p2 = Player([tapuLele, cinderace])
        w = Weather()
        t = Terrain()
        testFrame = Frame(p1, p2, None, None, w, t)
        return testFrame

    @pytest.fixture
    def testFrame2(self):
        slowbro = Pokemon(
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
        tyranitar = Pokemon(
            "Tyranitar",
            100,
            "Male",
            ("Crunch", "Stealth Rock", "Toxic", "Earthquake"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 0, 0, 216, 40),
            "Careful",
        )
        tapuLele = Pokemon(
            "Tapu Lele",
            100,
            None,
            ("Psychic", "Moonblast", "Focus Blast", "Psyshock"),
            "Psychic Surge",
            "Choice Specs",
            (31, 0, 31, 31, 31, 31),
            (0, 0, 0, 252, 4, 252),
            "Timid",
        )
        cinderace = Pokemon(
            "Cinderace",
            100,
            "Male",
            ("Pyro Ball", "U-turn", "Gunk Shot", "High Jump Kick"),
            "Libero",
            "Heavy Duty Boots",
            (31, 31, 31, 31, 31, 31),
            (0, 252, 0, 0, 4, 252),
            "Jolly",
        )

        p1 = Player([tapuLele, cinderace])
        p2 = Player([slowbro, tyranitar])
        w = Weather()
        t = Terrain()
        testFrame = Frame(p1, p2, None, None, w, t)
        return testFrame

    @pytest.mark.parametrize(
        "f1Move,f2Move,f1Switch,f2Switch,f1Status,terrain,expectedResult",
        [
            (0, None, None, 1, [None], None, ["f1", "f2"]),
            (1, 0, None, None, [None], None, ["f1", "f2"]),
            (None, None, 1, 1, [None], None, ["f1", "f2"]),
            (1, None, None, 1, [None], None, ["f2", "f1"]),
            (1, 3, None, None, [None], None, ["f2", "f1"]),
            (2, 1, None, None, [None], None, ["f2", "f1"]),
            (3, 3, None, None, [None], None, ["f1", "f2"]),
            (None, None, 1, 1, ["Paralyzed"], None, ["f2", "f1"]),
            (1, 1, None, None, ["Paralyzed"], None, ["f2", "f1"]),
        ],
    )
    def testGetFrameOrder(
        self,
        f1Move,
        f2Move,
        f1Switch,
        f2Switch,
        f1Status,
        terrain,
        expectedResult,
    ):
        testPokemon1 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Pursuit", "Tackle", "Teleport", "Extreme Speed"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 252, 0, 4, 252),
            "Relaxed",
        )

        testPokemon2 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Pursuit", "Tackle", "Teleport", "Extreme Speed"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        player1 = Player([testPokemon1])
        player2 = Player([testPokemon2])
        t = Terrain()
        f1 = Frame(player1, player2, None, None, None, t)
        f2 = Frame(player2, player1, None, None, None, t)

        if f1Move is not None:
            f1.attack = f1.user.moves[f1Move]
        f1.switchChoice = f1Switch

        if f2Move is not None:
            f2.attack = f2.user.moves[f2Move]
        f2.switchChoice = f2Switch

        f1.user.status = f1Status
        t.currentTerrain = terrain

        result = getFrameOrder(f1, f2)

        if result == [f1, f2]:
            result = ["f1", "f2"]
        else:
            result = ["f2", "f1"]

        assert result == expectedResult

    @pytest.mark.parametrize(
        "f1SpeedEv,f2SpeedEv,speedMod,status,expectedResult",
        [
            (0, 0, 0, None, ["f2", "f1"]),
            (0, 0, 0, "Paralyzed", ["f2", "f1"]),
            (0, 0, 4, None, ["f1", "f2"]),
            (0, 0, 4, "Paralyzed", ["f1", "f2"]),
            (0, 0, -4, None, ["f2", "f1"]),
            (252, 0, 0, None, ["f1", "f2"]),
            (252, 0, 0, "Paralyzed", ["f2", "f1"]),
            (252, 0, 4, None, ["f1", "f2"]),
            (252, 0, -4, None, ["f2", "f1"]),
            (0, 252, 0, None, ["f2", "f1"]),
            (0, 252, 4, None, ["f1", "f2"]),
            (0, 252, -4, None, ["f2", "f1"]),
        ],
    )
    def testCheckSpeed(self, f1SpeedEv, f2SpeedEv, speedMod, status, expectedResult):
        testPokemon1 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, f1SpeedEv),
            "Relaxed",
        )

        testPokemon2 = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, f2SpeedEv),
            "Relaxed",
        )

        player1 = Player([testPokemon1])
        player2 = Player([testPokemon2])
        f1 = Frame(player1, player2, None, None, None, None)
        f2 = Frame(player2, player1, None, None, None, None)

        f1.user.statMod["speed"] = speedMod
        f1.user.status[0] = status
        result = checkSpeed(f1, f2)

        if result == [f1, f2]:
            result = ["f1", "f2"]
        else:
            result = ["f2", "f1"]

        assert result == expectedResult

    @pytest.mark.parametrize(
        "terrainName,attackName,expected",
        [
            ("Grassy Terrain", "Ice Shard", 1),
            ("Grassy Terrain", "Avalanche", -4),
            ("Grassy Terrain", "Tackle", 0),
            ("Grassy Terrain", "Grassy Glide", 1),
            ("Psychic Terrain", "Ice Shard", 0),
        ],
    )
    def testCheckPriority(self, testFrame, terrainName, attackName, expected):
        testFrame.terrain.currentTerrain = terrainName
        testFrame.user.setMove(0, attackName)
        testFrame.attack = testFrame.user.moves[0]
        assert checkPriority(testFrame) == expected

    @pytest.mark.parametrize("inputInt,expectedBool", [(4, True), (1, False)])
    def testRollParalysis(self, testPokemon, inputInt, expectedBool):
        assert rollParalysis(testPokemon, inputInt) == expectedBool

    @pytest.mark.parametrize(
        "inputInt,expectedBool,expectedStatus",
        [(4, False, "Frozen"), (1, True, None)],
    )
    def testRollFrozen(self, testPokemon, inputInt, expectedBool, expectedStatus):
        testPokemon.status[0] = "Frozen"
        assert rollFrozen(testPokemon, inputInt) == expectedBool
        assert testPokemon.status[0] == expectedStatus

    @pytest.mark.parametrize(
        "inputInt,expectedBool,expectedHp", [(2, True, 394), (1, False, 375)]
    )
    def testRollConfusion(self, testPokemon, inputInt, expectedBool, expectedHp):
        assert rollConfusion(testPokemon, inputInt) == expectedBool
        assert testPokemon.stat["hp"] == expectedHp

    def testCalcConfusionDamage(self, testPokemon):
        assert calcConfusionDamage(testPokemon) == 19

    @pytest.mark.parametrize(
        "attackType,targetType,inputGrounded,expected",
        [
            ("Poison", "Steel", True, False),
            ("Dragon", "Fairy", True, False),
            ("Normal", "Ghost", True, False),
            ("Fighting", "Ghost", True, False),
            ("Ghost", "Normal", True, False),
            ("Electric", "Ground", True, False),
            ("Psychic", "Dark", True, False),
            ("Poison", "Fire", True, True),
            ("Ground", "Water", False, False),
            ("Ground", "Water", True, True),
        ],
    )
    def testCheckImmunity(
        self, testFrame, attackType, targetType, inputGrounded, expected
    ):
        testFrame.attack = testFrame.user.moves[0]
        testFrame.attack.type = attackType
        testFrame.target.typing[0] = targetType
        testFrame.target.grounded = inputGrounded
        assert checkImmunity(testFrame) == expected

    @pytest.mark.parametrize(
        "status,vStatus,vStatusValue,number,expectedBool,typing,ability,attackType,attackMod,spAttackMod",
        [
            (["Paralyzed", 2], None, None, 1, False, "Steel", None, "Steel", 0, 0),
            (["Paralyzed", 2], None, None, 2, True, "Steel", None, "Steel", 0, 0),
            (["Asleep", 3], None, None, 2, False, "Steel", None, "Steel", 0, 0),
            (["Frozen", 3], None, None, 2, False, "Steel", None, "Steel", 0, 0),
            ([None], "Flinched", [2], None, False, "Steel", None, "Steel", 0, 0),
            ([None], "Confusion", [1], 1, False, "Steel", None, "Steel", 0, 0),
            ([None], None, None, None, False, "Steel", None, "Poison", 0, 0),
            ([None], None, None, None, True, "Steel", None, "Water", 0, 0),
            ([None], None, None, None, False, "Steel", "Flash Fire", "Fire", 1, 1),
        ],
    )
    def testCheckCanAttack(
        self,
        testFrame,
        status,
        vStatus,
        vStatusValue,
        number,
        expectedBool,
        typing,
        ability,
        attackType,
        attackMod,
        spAttackMod,
    ):
        testFrame.attack = testFrame.user.moves[0]
        testFrame.user.status = status
        testFrame.user.vStatus[vStatus] = vStatusValue
        testFrame.target.ability = ability
        testFrame.target.typing[0] = typing
        testFrame.attack.type = attackType
        assert checkCanAttack(testFrame, number) == expectedBool
        assert testFrame.target.statMod["attack"] == attackMod
        assert testFrame.target.statMod["spAttack"] == spAttackMod

    def testCheckAttackLands(self, testFrame, testFrame2):
        testFrame.attack = testFrame.user.moves[1]
        checkAttackLands(testFrame)
        assert testFrame.attackLands == True
        testFrame2.attack = testFrame2.user.moves[2]
        checkAttackLands(testFrame2, 100)
        assert testFrame2.attackLands == False
        checkAttackLands(testFrame2, 20)
        assert testFrame2.attackLands == True
        testFrame2.user.setMove(0, "High Jump Kick")
        testFrame2.attack = testFrame2.user.moves[0]
        checkAttackLands(testFrame2, 100)
        assert testFrame2.user.stat["hp"] == 141

    @pytest.mark.parametrize(
        "moveName,stealthRocks,expectedBool,expectedStatus",
        [
            ("Stealth Rock", False, True, None),
            ("Defog", True, False, None),
            ("Toxic", False, False, "Badly Poisoned"),
        ],
    )
    def testApplyNonDamagingMove(
        self, testFrame, moveName, stealthRocks, expectedBool, expectedStatus
    ):
        testFrame.user.setMove(0, moveName)
        testFrame.attack = testFrame.user.moves[0]
        testFrame.defendingTeam.stealthRocks = stealthRocks
        applyNonDamagingMove(testFrame)
        assert testFrame.defendingTeam.stealthRocks == expectedBool
        assert testFrame.target.status[0] == expectedStatus

    def testSwitch(self, testFrame):
        testFrame.user.prevMove = "Scald"
        testFrame.user.statMod["attack"] = 6
        testFrame.user.vStatus["Confused"] = [0]
        testFrame.user.stat["hp"] = 50
        testFrame.attackingTeam.stealthRocks = True
        testFrame.switchChoice = 1
        switch(testFrame)
        testFrame.updateCurPokemon()
        assert testFrame.user.name == "Tyranitar"
        assert testFrame.user.stat["hp"] == 354
        assert testFrame.attackingTeam[1].prevMove == None
        assert testFrame.attackingTeam[1].statMod["attack"] == 0
        assert len(testFrame.attackingTeam[1].vStatus) == 0
        assert testFrame.attackingTeam[1].stat["hp"] == 181
        testFrame.attackingTeam[1].stat["hp"] = 0
        switch(testFrame)
        testFrame.updateCurPokemon()
        assert testFrame.user.name == "Tyranitar"

    @pytest.mark.parametrize(
        "abilityName,switchDirection,hp,expectedTerrain,expectedWeather,expectedAttackMod,expectedHp",
        [
            ("Grassy Surge", "In", 300, "Grassy Terrain", "Clear Skies", 0, 300),
            ("Psychic Surge", "In", 300, "Psychic Terrain", "Clear Skies", 0, 300),
            ("Intimidate", "In", 300, None, "Clear Skies", -1, 300),
            ("Sand Stream", "In", 300, None, "Sandstorm", 0, 300),
            ("Regenerator", "Out", 50, None, "Clear Skies", 0, 181),
        ],
    )
    def testApplySwitchEffect(
        self,
        testFrame,
        abilityName,
        switchDirection,
        hp,
        expectedTerrain,
        expectedWeather,
        expectedAttackMod,
        expectedHp,
    ):
        testFrame.user.ability = abilityName
        testFrame.user.stat["hp"] = hp
        applySwitchEffect(testFrame, 0, switchDirection)
        assert testFrame.terrain.currentTerrain == expectedTerrain
        assert testFrame.target.statMod["attack"] == expectedAttackMod
        assert testFrame.weather.currentWeather == expectedWeather
        assert testFrame.user.stat["hp"] == expectedHp

    @pytest.mark.parametrize(
        "item,expectedHp", [(None, 345), ("Heavy Duty Boots", 394)]
    )
    def testApplyEntryHazards(self, testFrame, item, expectedHp):
        testFrame.attackingTeam.stealthRocks = True
        testFrame.user.item = item
        applyEntryHazards(testFrame)
        assert testFrame.user.stat["hp"] == expectedHp

    @pytest.mark.parametrize(
        "position,expectedHp", [(0, 290), (1, 264), (2, 282), (3, 204), (4, 149)]
    )
    def testApplyStealthRocksDamage(self, position, expectedHp):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )

        charizard = Pokemon(
            "Charizard",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )

        fearow = Pokemon(
            "Fearow",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )

        aggron = Pokemon(
            "Aggron",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )

        steelix = Pokemon(
            "Steelix",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (0, 0, 0, 0, 0, 0),
            "Relaxed",
        )

        testPlayer = Player([slowbro, aggron, steelix, fearow, charizard])
        testFrame = Frame(testPlayer, testPlayer, None, None, None, None)
        testFrame.user = testFrame.attackingTeam[position]
        applyStealthRocksDamage(testFrame)
        assert testFrame.user.stat["hp"] == expectedHp

    def testApplyPostAttackEffects(self):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Close Combat", "Toxic", "Test Dark Pulse", "Teleport"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        tyranitar = Pokemon(
            "Tyranitar",
            100,
            "Male",
            ("Crunch", "Stealth Rock", "Toxic", "Earthquake"),
            None,
            None,
            (31, 31, 31, 31, 31, 31),
            (252, 0, 0, 0, 216, 40),
            "Careful",
        )
        team1 = Player([slowbro])
        team2 = Player([tyranitar])
        testFrame = Frame(team1, team2, None, None, None, None)
        testFrame.attack = testFrame.user.moves[0]
        assert testFrame.user.statMod["defense"] == 0
        assert testFrame.user.statMod["spDefense"] == 0
        applyPostAttackEffects(testFrame)
        assert testFrame.user.statMod["defense"] == -1
        assert testFrame.user.statMod["spDefense"] == -1
        testFrame.attack = testFrame.user.moves[1]
        assert testFrame.target.status[0] == None
        applyPostAttackEffects(testFrame)
        assert testFrame.target.status[0] == "Badly Poisoned"
        testFrame.attack = testFrame.user.moves[2]
        assert len(testFrame.target.vStatus) == 0
        applyPostAttackEffects(testFrame)
        assert testFrame.target.vStatus["Flinched"] == [1]
        testFrame.target.ability = "Static"
        testFrame.attack.name = "Close Combat"
        applyPostAttackEffects(testFrame, 20)
        assert testFrame.user.status[0] == "Paralyzed"

    def testApplyEndOfTurnEffects(self, testFrame, testFrame2):
        frameOrder = [testFrame, testFrame2]
        testFrame.attack = testFrame.user.moves[0]
        testFrame2.attack = testFrame2.user.moves[0]
        testFrame.weather.currentWeather = "Sandstorm"
        testFrame.user.status = ["Asleep", 3]
        testFrame.user.vStatus["Flinched"] = [2]
        applyEndOfTurnEffects(frameOrder)
        assert testFrame.user.moves[0].pp == 23
        assert testFrame.user.stat["hp"] == 370
        assert testFrame.user.status[1] == 2
        assert testFrame.user.vStatus["Flinched"] == [1]
        testFrame.user.stat["hp"] = 50
        testFrame.weather.currentWeather = None
        testFrame.terrain.currentTerrain = "Grassy Terrain"
        testFrame2.user.status = ["Burned", 1]
        applyEndOfTurnEffects(frameOrder)
        assert testFrame.user.stat["hp"] == 74
        assert testFrame2.user.stat["hp"] == 264
        testFrame.terrain.currentTerrain = None
        testFrame.user.item = "Leftovers"
        testFrame2.user.status = ["Badly Poisoned", 3]
        applyEndOfTurnEffects(frameOrder)
        assert testFrame.user.stat["hp"] == 98
        assert testFrame2.user.stat["hp"] == 36
        testFrame2.user.status = ["Poisoned", 4]
        testFrame2.user.stat["hp"] = 200
        applyEndOfTurnEffects(frameOrder)
        assert testFrame2.user.stat["hp"] == 165
        testFrame.user.setMove(0, "Wood Hammer")
        testFrame.attack = testFrame.user.moves[0]
        testFrame.attackDamage = 100
        assert testFrame.user.stat["hp"] == 122
        applyEndOfTurnEffects(frameOrder)
        assert testFrame.user.prevMove == "Wood Hammer"
