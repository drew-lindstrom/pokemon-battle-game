from pokemon import Pokemon
from terrain import Terrain
from weather import Weather
import gameText


def activateGrassySurge(user, terrain):
    if user.ability == "Grassy Surge":
        terrain.setTerrain("Grassy Terrain", user)


def activateIntimidate(user, target):
    if user.ability == "Intimidate":
        gameText.output.append(f"{target.name} was initimated!")
        gameText.output.append("")
        target.updateStatModifier("attack", -1)


def activateRegenerator(user):
    if user.ability == "Regenerator" and not user.checkFainted():
        user.applyHeal(1 / 3)


def activatePsychicSurge(user, terrain):
    if user.ability == "Psychic Surge":
        terrain.setTerrain("Psychic Terrain", user)


def activateSandStream(user, weather):
    if user.ability == "Sand Stream":
        weather.setWeather("Sandstorm", user)
