from pokemon import Pokemon
import gameText


class Terrain:
    def __init__(self, terrain=None, counter=0):
        self.currentTerrain = terrain
        self.counter = counter

    def setTerrain(self, terrainName, pokemon):
        """Sets currentTerrain to the specified terrain and terrainCounter to 5 turns (or 8 turns if pokemon is holding Terrain Extender)."""
        if self.currentTerrain is None:
            self.currentTerrain = terrainName
            gameText.output += f"{terrainName} has been activated!\n"
            if pokemon.item == "Terrain Extender":
                self.counter = 7
            else:
                self.counter = 4

    def decrementTerrain(self):
        """Decrements the terrain counter by one at the end of each turn. If the counter equals 0, clearTerrain() is called."""
        if self.currentTerrain is not None:
            if self.counter == 0:
                self.clearTerrain()
            else:
                self.counter -= 1

    def clearTerrain(self):
        """Resets terrain to None and resets counter to 0."""
        gameText.output += f"The {self.currentTerrain.lower()} subsided.\n"
        self.currentTerrain = None
        self.counter = 0


def checkDamageModFromTerrain(frame):
    if (
        (
            frame.terrain.currentTerrain == "Electric Terrain"
            and frame.attack.type == "Electric"
        )
        or (
            frame.terrain.currentTerrain == "Grassy Terrain"
            and frame.attack.type == "Grass"
        )
        or (
            frame.terrain.currentTerrain == "Psychic Terrain"
            and frame.attack.type == "Psychic"
        )
    ):
        return 1.3
    if (
        frame.terrain.currentTerrain == "Misty Terrain"
        and frame.attack.type == "Dragon"
    ):
        return 0.5
    else:
        return 1


def healFromGrassyTerrain(terrain, pokemon):
    """If the current terrain is Grassy Terrain and the pokemon is grounded, heals for 1/16 max HP at the end of the turn."""
    if (
        terrain.currentTerrain == "Grassy Terrain"
        and pokemon.grounded == True
        and not pokemon.checkFainted()
    ):
        gameText.output += f"{pokemon.name} healed from the Grassy Terrain!\n"
        pokemon.applyHeal(0.0625)
