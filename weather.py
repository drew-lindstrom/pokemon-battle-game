from pokemon import Pokemon

# Need to add weather method descriptions
class Weather:
    def __init__(self, weather="Clear Skies", counter=None):
        self.current_weather = weather
        self.weather_counter = counter

    def set_weather(self, weather, counter):
        self.current_weather = weather
        self.weather_counter = counter
        if self.current_weather == "Sandstorm":
            print("A sandstorm kicked up!")

    def clear_weather(self):
        if self.weather_counter == 0:
            if self.current_weather == "Sandstorm":
                print("The sandstorm subsided.")
            self.current_weather = "Clear Skies"


def sandstorm_damage(weather, pokemon):
    if pokemon.typing[0] in ("Rock", "Steel", "Ground") or pokemon.typing[1] in (
        "Rock",
        "Steel",
        "Ground",
    ):
        return False
    elif pokemon.ability in (
        "Sand Force",
        "Sand Rush",
        "Sand Veil",
        "Magic Guard",
        "Overcoat",
    ):
        return False
    elif pokemon.item == "Safety Goggles":
        return False
    else:
        pokemon.damage(1 / 16)
        return True

    # Sandstorm To Do:
    #  Effect Text
    #  Ability activation
    #  Special defense boost for rock types
    #  Changes Weather Ball to a rock-type move and doubles its power
    #  Halves power of solar beam and solar blade
    #  Causes Shore Up to recover 2/3 of max HP instead of 1/2
    #  Causes Moonlight, Synthesis, and Morning Sun to recover 1/4 of max HP