from pokemon import Pokemon
import gameText


class Weather:
    def __init__(self, weatherName="Clear Skies", counter=0):
        self.currentWeather = weatherName
        self.counter = counter

    def setWeather(self, weatherName, pokemon):
        """Sets currentWeather to the specified weather if currently Clear Skies and
        set weatherCounter to 5 turns (or 8 turns if pokemon is holding the correct item)."""
        if self.currentWeather == "Clear Skies":
            self.currentWeather = weatherName
            if weatherName == "Sandstorm":
                gameText.output += "A sandstorm kicked up!\n"
            if weatherName == "Rain":
                gameText.output += "It started to rain!\n"
            if weatherName == "Harsh Sunlight":
                gameText.output += "The sunlight turned harsh!\n"
            if weatherName == "Hail":
                gameText.output += "It started to hail!\n"
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
        """Decrements the weather counter by one at the end of each turn. If the counter equals 0, the weather is reset to Clear Skies."""
        if self.currentWeather != "Clear Skies":
            if self.counter == 0:

                self.clearWeather()
            else:
                self.counter -= 1

    def clearWeather(self):
        """Resets the current weather to Clears Skies and sets the counter to None."""
        gameText.output += f"The {self.currentWeather.lower()} subsided.\n"
        self.currentWeather = "Clear Skies"
        self.counter = 0


def applyWeatherDamage(weather, pokemon):
    """If weather is currently Sandstorm or Hail, damages all pokemon on the field at end of turn
    unless pokemon is of specific type, ability, or holding Safety Goggles."""
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

    gameText.output += (
        f"{pokemon.name} was buffeted by the {weather.currentWeather.lower()}!\n"
    )

    pokemon.applyDamage(None, 1 / 16)

    return True


def checkSandstormSpDefBoost(weather, pokemon):
    """Increases special defense of Rock type pokemon while weather is Sandstorm."""
    if weather.currentWeather == "Sandstorm" and (
        (pokemon.typing[0] == "Rock") or (pokemon.typing[1] == "Rock")
    ):
        return 1.5
    return 1


def checkDamageModFromWeather(weather, pokemon, n):
    """Boosts power of fire type moves by 50% and lowers power of water type moves by 50% if weather is Harsh Sunlight.
    Boosts power of water type moves by 50% and lower power of fire types moves by 50% if weather is Rain."""
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