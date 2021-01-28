from pokemon import Pokemon

# Need to add weather method descriptions
class Weather:
    def __init__(self, weather="Clear Skies", counter=None):
        self.current_weather = weather
        self.weather_counter = counter

    def set_weather(self, weather, pokemon):
        """Sets current_weather to the specified weather and weather_counter to 5 turns (or 8 turns if pokemon is holding the correct item)."""
        self.current_weather = weather
        if weather == "Sandstorm":
            self.current_weather = "Sandstorm"
            print("A sandstorm kicked up!")
        if weather == "Rain":
            self.current_weather = "Rain"
            print("It started to rain!")
        if weather == "Harsh Sunlight":
            self.current_weather = "Harsh Sunlight"
            print("The sunlight turned harsh!")
        if weather == "Hail":
            self.current_weather = "Hail"
            print("It started to hail!")
        if (
            (pokemon.item == "Smooth Rock" and weather == "Sandstorm")
            or (pokemon.item == "Damp Rock" and weather == "Rain")
            or (pokemon.item == "Heat Rock" and weather == "Harsh Sunlight")
            or (pokemon.item == "Icy Rock" and weather == "Hail")
        ):
            self.weather_counter = 8
        else:
            self.weather_counter = 5

    def clear_weather(self):
        """Checks the weather counter at the end of the turn and resets current_weather to 'Clear Skies' if 0."""
        # TODO does making weather reset at 0 cause the weather to last for 6/9 turns?
        if self.weather_counter == 0:
            if self.current_weather == "Sandstorm":
                print("The sandstorm subsided.")
            if self.current_weather == "Rain":
                print("The rain subsided.")
            if self.current_weather == "Harsh Sunlight":
                print("The harsh sunlight ended.")
            if self.current_weather == "Hail":
                print("The hail subsided.")
            self.current_weather = "Clear Skies"


def sandstorm_damage(weather, pokemon):
    """Damages all pokemon on the field at end of turn unless specific type, ability, or hold Safety Goggles."""
    if weather.current_weather == "Sandstorm":
        for typing in pokemon.typing:
            if typing in ("Rock", "Steel", "Ground"):
                return False
        if pokemon.ability in (
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
            print(f"{pokemon.name} was buffeted by the sandstorm!")
            return True


def sandstorm_sp_def_boost(weather, pokemon):
    """Increases special defense of Rock type pokemon while weather is Sandstorm."""
    if weather.current_weather == "Sandstorm" and (
        (pokemon.typing[0] == "Rock") or (pokemon.typing[1] == "Rock")
    ):
        return 1.5
    return 1
    # Sandstorm To Do:
    #  Effect Text
    #  Ability activation
    #  Special defense boost for rock types
