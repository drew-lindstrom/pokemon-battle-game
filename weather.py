from pokemon import Pokemon


class Weather:
    def __init__(self, weather="Clear Skies", counter=None):
        self.current_weather = weather
        self.weather_counter = counter

    def set_weather(self, weather, pokemon):
        """Sets current_weather to the specified weather and weather_counter to 5 turns (or 8 turns if pokemon is holding the correct item)."""
        assert weather in ("Sandstorm", "Hail", "Rain", "Harsh Sunlight")
        self.current_weather = weather
        if weather == "Sandstorm":
            print("A sandstorm kicked up!")
        if weather == "Rain":
            print("It started to rain!")
        if weather == "Harsh Sunlight":
            print("The sunlight turned harsh!")
        if weather == "Hail":
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
            print(f"The {self.current_weather.lower()} subsided.")
            self.current_weather = "Clear Skies"


# TODO: weather counterdowner
# TODO: What happens if pokemon uses Sandstorm while sandstorm is already up, does the count reset?
# TODO: Remove weather funciton


def weather_damage(weather, pokemon):
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


def weather_move_damage_mod(weather, pokemon, n):
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