from pokemon import Pokemon
from terrain import Terrain
from weather import Weather


def activate_grassy_surge(user, terrain):
    """Sets terrain to grassy terrain, if possible, when pokemon with grassy surge ability switches in."""
    if user.ability == "Grassy Surge":
        terrain.set_terrain("Grassy Terrain")


def activate_intimidate(user, target):
    """Lowers target's attack by one when a pokemon with intimidate ability switches in."""
    if user.ability == "Intimidate":
        print(f"{target.name} was initimated!")
        print()
        target.update_stat_modifier("attack", -1)


def activate_regenerator(user):
    """Heals a pokemon by 1/3 of it's max hp if it's ability is regenerator and switches out."""
    if user.ability == "Regenerator":
        user.heal(1 / 3)


def activate_psychic_surge(user, terrain):
    """Sets terrain to psychic terrain, if possible, when pokemon with psychic surge ability switches in."""
    if user.ability == "Psychic Surge":
        terrain.set_terrain("Psychic Terrain")


def activate_sand_stream(user, weather):
    """Sets weather to sandstorm, if possible, when pokemon with sand stream ability switches in."""
    if user.ability == "Sand Stream":
        weather.set_weather("Sandstorm", user)