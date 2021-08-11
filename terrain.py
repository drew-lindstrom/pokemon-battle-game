from pokemon import Pokemon
import gameText


class Terrain:
    def __init__(self, terrain=None, counter=0):
        self.currentTerrain = terrain
        self.counter = counter

    def setTerrain(self, terrainName, pokemon):
        if self.currentTerrain is None:
            self.currentTerrain = terrainName
            gameText.output.append(f"{terrainName} has been activated!")
            gameText.output.append("")
            if pokemon.item == "Terrain Extender":
                self.counter = 7
            else:
                self.counter = 4

    def decrementTerrain(self):
        if self.currentTerrain is not None:
            if self.counter == 0:
                self.clearTerrain()
            else:
                self.counter -= 1

    def clearTerrain(self):
        gameText.output.append(f"The {self.currentTerrain.lower()} subsided.")
        gameText.output.append("")
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
    if (
        terrain.currentTerrain == "Grassy Terrain"
        and pokemon.grounded == True
        and not pokemon.checkFainted()
    ):
        gameText.output.append(
            f"{pokemon.name} healed from the Grassy Terrain!")
        pokemon.applyHeal(0.0625)
