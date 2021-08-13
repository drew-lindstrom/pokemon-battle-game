from pokemon import Pokemon
import gameText
import json


class Weather:
    def __init__(self, currentWeather="Clear Skies", counter=0):
        self.currentWeather = currentWeather
        self.counter = counter

    def setWeather(self, weatherName, pokemon):
        if self.currentWeather == "Clear Skies":
            self.currentWeather = weatherName
            if weatherName == "Sandstorm":
                gameText.output.append("A sandstorm kicked up!")
                gameText.output.append("")
            if weatherName == "Rain":
                gameText.output.append("It started to rain!")
                gameText.output.append("")
            if weatherName == "Harsh Sunlight":
                gameText.output.append("The sunlight turned harsh!")
                gameText.output.append("")
            if weatherName == "Hail":
                gameText.output.append("It started to hail!")
                gameText.output.append("")
            if (
                (pokemon.item == "Smooth Rock" and weatherName == "Sandstorm")
                or (pokemon.item == "Damp Rock" and weatherName == "Rain")
                or (pokemon.item == "Heat Rock" and weatherName == "Harsh Sunlight")
                or (pokemon.item == "Icy Rock" and weatherName == "Hail")
            ):
                self.counter = 7
            else:
                self.counter = 4

    def decrementWeather(self):
        if self.currentWeather != "Clear Skies":
            if self.counter == 0:

                self.clearWeather()
            else:
                self.counter -= 1

    def clearWeather(self):
        gameText.output.append(f"The {self.currentWeather.lower()} subsided.")
        gameText.output.append("")
        self.currentWeather = "Clear Skies"
        self.counter = 0

    @classmethod
    def deserializeAndUpdateWeatherFromJson(cls, data):
        return cls(**data)


def applyWeatherDamage(weather, pokemon):
    if weather.currentWeather not in ("Sandstorm", "Hail"):
        return False
    if weather.currentWeather == "Sandstorm":
        for typing in pokemon.typing:
            if typing in ("Rock", "Steel", "Ground"):
                return False
        if pokemon.ability in (
            "Sand Force",
            "Sand Rush",
            "Sand Veil",
        ):
            return False
    if weather.currentWeather == "Hail":
        for typing in pokemon.typing:
            if typing == "Ice":
                return False
            if pokemon.ability in ("Ice Body", "Snow Cloak"):
                return False
    if pokemon.ability in ("Magic Guard", "Overcoat"):
        return False
    if pokemon.item == "Safety Goggles":
        return False

    if not pokemon.checkFainted():
        gameText.output.append(
            f"{pokemon.name} was buffeted by the {weather.currentWeather.lower()}!"
        )
        gameText.output.append("")

        pokemon.applyDamage(None, 1 / 16)

    return True


def checkSandstormSpDefBoost(weather, pokemon):
    if weather.currentWeather == "Sandstorm" and (
        (pokemon.typing[0] == "Rock") or (pokemon.typing[1] == "Rock")
    ):
        return 1.5
    return 1


def checkDamageModFromWeather(weather, pokemon, n):
    if weather.currentWeather == "Harsh Sunlight":
        if pokemon.moves[n].type == "Fire":
            return 1.5
        elif pokemon.moves[n].type == "Water":
            return 0.5

    elif weather.currentWeather == "Rain":
        if pokemon.moves[n].type == "Water":
            return 1.5
        elif pokemon.moves[n].type == "Fire":
            return 0.5

    else:
        return 1
