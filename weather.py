from pokemon import Pokemon


class Weather:
    def __init__(self, weather_name="Clear Skies", counter=0):
        self.current_weather = weather_name
        self.counter = counter

    def set_weather(self, weather_name, pokemon):
        """Sets current_weather to the specified weather if currently Clear Skies and
        set weather_counter to 5 turns (or 8 turns if pokemon is holding the correct item)."""
        if self.current_weather == "Clear Skies":
            self.current_weather = weather_name
            if weather_name == "Sandstorm":
                print("A sandstorm kicked up!")
            if weather_name == "Rain":
                print("It started to rain!")
            if weather_name == "Harsh Sunlight":
                print("The sunlight turned harsh!")
            if weather_name == "Hail":
                print("It started to hail!")
            if (
                (pokemon.item == "Smooth Rock" and weather_name == "Sandstorm")
                or (pokemon.item == "Damp Rock" and weather_name == "Rain")
                or (pokemon.item == "Heat Rock" and weather_name == "Harsh Sunlight")
                or (pokemon.item == "Icy Rock" and weather_name == "Hail")
            ):
                self.counter = 7
            else:
                self.counter = 4

    def decrement_weather(self):
        """Decrements the weather counter by one at the end of each turn. If the counter equals 0, the weather is reset to Clear Skies."""
        if self.current_weather != "Clear Skies":
            if self.counter == 0:
                print(f"The {self.current_weather.lower()} subsided.")
                self.clear_weather()
            else:
                self.counter -= 1

    def clear_weather(self):
        """Resets the current weather to Clears Skies and sets the counter to None."""
        self.current_weather = "Clear Skies"
        self.counter = 0


def apply_weather_damage(weather, pokemon):
    """If weather is currently Sandstorm or Hail, damages all pokemon on the field at end of turn
    unless pokemon is of specific type, ability, or holding Safety Goggles."""
    if weather.current_weather not in ("Sandstorm", "Hail"):
        return False
    if weather.current_weather == "Sandstorm":
        for typing in pokemon.typing:
            if typing in ("Rock", "Steel", "Ground"):
                return False
        if pokemon.ability in (
            "Sand Force",
            "Sand Rush",
            "Sand Veil",
        ):
            return False
    if weather.current_weather == "Hail":
        for typing in pokemon.typing:
            if typing == "Ice":
                return False
            if pokemon.ability in ("Ice Body", "Snow Cloak"):
                return False
    if pokemon.ability in ("Magic Guard", "Overcoat"):
        return False
    if pokemon.item == "Safety Goggles":
        return False
    pokemon.apply_damage_percentage(1 / 16)
    print(f"{pokemon.name} was buffeted by the {weather.current_weather.lower()}!")
    return True


def check_sandstorm_sp_def_boost(weather, pokemon):
    """Increases special defense of Rock type pokemon while weather is Sandstorm."""
    if weather.current_weather == "Sandstorm" and (
        (pokemon.typing[0] == "Rock") or (pokemon.typing[1] == "Rock")
    ):
        return 1.5
    return 1


def check_damage_mod_from_weather(weather, pokemon, n):
    """Boosts power of fire type moves by 50% and lowers power of water type moves by 50% if weather is Harsh Sunlight.
    Boosts power of water type moves by 50% and lower power of fire types moves by 50% if weather is Rain."""
    if weather.current_weather == "Harsh Sunlight":
        if pokemon.moves[n].type == "Fire":
            return 1.5
        elif pokemon.moves[n].type == "Water":
            return 0.5

    elif weather.current_weather == "Rain":
        if pokemon.moves[n].type == "Water":
            return 1.5
        elif pokemon.moves[n].type == "Fire":
            return 0.5

    else:
        return 1