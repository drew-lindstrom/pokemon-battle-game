from pokemon import Pokemon
from terrain import Terrain
from weather import Weather


def activate_grassy_surge(user, terrain):
    if user.ability == "Grassy Surge":
        terrain.set_terrain("Grassy Terrain")


def activate_intimidate(user, target):
    if user.ability == "Intimidate":
        print(f"{target.name} was initimated!")
        target.update_stat_modifier("attack", -1)


def activate_regenerator(user):
    if user.ability == "Regenerator":
        user.heal(1 / 3)


def activate_psychic_surge(user, terrain):
    if user.ability == "Psychic Surge":
        terrain.set_terrain("Psychic Terrain")


def activate_sand_stream(user, weather):
    if user.ability == "Sand Stream":
        weater.set_weather("Sandstorm")