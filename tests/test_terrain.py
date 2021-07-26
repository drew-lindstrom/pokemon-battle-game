from pokemon import Pokemon
from frame import Frame
from player import Player
from terrain import Terrain, checkDamageModFromTerrain, healFromGrassyTerrain
import gameText
import pytest

gameText.output = []


class TestTerrain:
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
        "terrainName1,terrainName2,item,expectedTerrain,expectedInt",
        [
            (None, "Psychic Terrain", None, "Psychic Terrain", 4),
            ("Psychic Terrain", "Grassy Terrain", None, "Psychic Terrain", 4),
            (None, "Grassy Terrain", "Terrain Extender", "Grassy Terrain", 7),
        ],
    )
    def testSetTerrain(
        self,
        testPokemon,
        terrainName1,
        terrainName2,
        item,
        expectedTerrain,
        expectedInt,
    ):
        slowbro = testPokemon
        terrain = Terrain()
        slowbro.item = item
        terrain.setTerrain(terrainName1, slowbro)
        terrain.setTerrain(terrainName2, slowbro)
        terrain.setTerrain("Psychic Terrain", slowbro)
        assert terrain.currentTerrain == expectedTerrain
        assert terrain.counter == expectedInt

    @pytest.mark.parametrize(
        "terrainName,counter,expectedTerrain,expectedInt",
        [("Psychic Terrain", 4, "Psychic Terrain", 3), ("Psychic Terrain", 0, None, 0)],
    )
    def testDecrementTerrain(
        self, testPokemon, terrainName, counter, expectedTerrain, expectedInt
    ):
        slowbro = testPokemon
        terrain = Terrain()
        terrain.setTerrain(terrainName, slowbro)
        terrain.counter = counter
        terrain.decrementTerrain()
        assert terrain.currentTerrain == expectedTerrain
        assert terrain.counter == expectedInt

    @pytest.mark.parametrize(
        "terrainName,counter,expectedTerrain",
        [
            ("Psychic Terrain", 3, None),
        ],
    )
    def testClearTerrain(self, testPokemon, terrainName, counter, expectedTerrain):
        slowbro = testPokemon
        terrain = Terrain()
        terrain.setTerrain(terrainName, slowbro)
        terrain.counter = counter
        terrain.clearTerrain()
        assert terrain.currentTerrain == expectedTerrain

    @pytest.mark.parametrize(
        "moveType,terrainName,expectedInt",
        [
            ("Electric", "Electric Terrain", 1.3),
            ("Grass", "Electric Terrain", 1),
            ("Grass", "Grassy Terrain", 1.3),
            ("Dragon", "Grassy Terrain", 1),
            ("Dragon", "Misty Terrain", 0.5),
            ("Psychic", "Misty Terrain", 1),
            ("Psychic", "Psychic Terrain", 1.3),
            ("Electric", "Psychic Terrain", 1),
        ],
    )
    def testCheckDamageModFromTerrain(
        self, testPokemon, moveType, terrainName, expectedInt
    ):
        slowbro = testPokemon
        terrain = Terrain()
        testPlayer = Player([slowbro])
        testFrame = Frame(testPlayer, testPlayer, None, None, None, terrain)

        testFrame.attack = slowbro.moves[0]
        testFrame.attack.type = moveType
        testFrame.terrain.currentTerrain = terrainName
        assert checkDamageModFromTerrain(testFrame) == expectedInt

    @pytest.mark.parametrize(
        "hp,terrainName,groundedBool,expectedInt",
        [(100, "Grassy Terrain", True, 124), (100, "Grassy Terrain", False, 100)],
    )
    def testHealFromGrassyTerrain(
        self, testPokemon, hp, terrainName, groundedBool, expectedInt
    ):
        slowbro = testPokemon
        t = Terrain()
        t.currentTerrain = terrainName
        slowbro.stat["hp"] = hp
        slowbro.grounded = groundedBool
        healFromGrassyTerrain(t, slowbro)
        assert slowbro.stat["hp"] == expectedInt
