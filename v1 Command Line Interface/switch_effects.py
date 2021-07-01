from pokemon import Pokemon
from terrain import Terrain
from weather import Weather


def activateGrassySurge(user, terrain):
    """Sets terrain to grassy terrain, if possible, when pokemon with grassy surge ability switches in."""
    if user.ability == "Grassy Surge":
        terrain.setTerrain("Grassy Terrain", user)


def activateIntimidate(user, target):
    """Lowers target's attack by one when a pokemon with intimidate ability switches in."""
    if user.ability == "Intimidate":
        print(f"{target.name} was initimated!")
        print()
        target.updateStatModifier("attack", -1)


def activateRegenerator(user):
    """Heals a pokemon by 1/3 of it's max hp if it's ability is regenerator and switches out."""
    if user.ability == "Regenerator":
        user.applyHeal(1 / 3)


def activatePsychicSurge(user, terrain):
    """Sets terrain to psychic terrain, if possible, when pokemon with psychic surge ability switches in."""
    if user.ability == "Psychic Surge":
        terrain.setTerrain("Psychic Terrain", user)


def activateSandStream(user, weather):
    """Sets weather to sandstorm, if possible, when pokemon with sand stream ability switches in."""
    if user.ability == "Sand Stream":
        weather.setWeather("Sandstorm", user)