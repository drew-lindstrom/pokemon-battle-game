from pokemon import Pokemon
from player import Player
from frame import Frame
import weather


def calcAttack(frame):
    """Calculates the attack stat of the given pokemon by calculating its modified attack stat and mulitplying it with any additional modifiers.
    If the given attack roled a critical hit, a negative attack statMod is ignored and calcModifiedStat is not called.
    Additional modifiers are still applied."""
    additionalModifier = 1

    if frame.user.item == "Choice Band":
        additionalModifier *= 1.5
    if frame.user.ability == "Blaze":
        additionalModifier *= checkBlaze(frame)
    if frame.crit == True and frame.user.statMod["attack"] < 0:
        return int(frame.user.stat["attack"] * additionalModifier)
    return int(frame.user.calcModifiedStat("attack") * additionalModifier)


def calcDefense(frame, pokemon=None):
    """Calculates the defense stat of the given pokemon by calculating its modified defense stat and mulitplying it with any additional modifiers.
    If the given attack roled a critical hit, a positive defense statMod is ignored and calcModifiedStat is not called.
    Additional modifiers are still applied."""
    additionalModifier = 1

    if pokemon == "user":
        pokemon = frame.user
    else:
        pokemon = frame.target

    if frame.crit == True and pokemon.statMod["defense"] > 0:
        return int(pokemon.stat["defense"] * additionalModifier)
    return int(pokemon.calcModifiedStat("defense") * additionalModifier)


def calcSpAttack(frame):
    """Calculates the special attack stat of the given pokemon by calculating its modified spAttack stat and mulitplying it with any additional modifiers.
    If the given attack roled a critical hit, a negative spAttack statMod is ignored and calcModifiedStat is not called.
    Additional modifiers are still applied."""
    additionalModifier = 1
    if frame.user.item == "Choice Spec":
        additionalModifier *= 1.5
    if frame.user.ability == "Blaze":
        additionalModifier *= checkBlaze(frame)
    if frame.crit == True and frame.user.statMod["spAttack"] < 0:
        return int(frame.user.stat["spAttack"] * additionalModifier)
    return int(frame.user.calcModifiedStat("spAttack") * additionalModifier)


def calcSpDefense(frame, pokemon=None):
    """Calculates the special defense stat of the given pokemon by calculating its modified spDefense stat and mulitplying it with any additional modifiers.
    If the given attack roled a critical hit, a positive spDefense statMod is ignored and calcModifiedStat is not called.
    Additional modifiers are still applied."""
    additionalModifier = 1
    additionalModifier *= weather.checkSandstormSpDefBoost(frame.weather, frame.user)

    if pokemon == "user":
        pokemon = frame.user
    else:
        pokemon = frame.target

    if frame.crit == True and pokemon.statMod["spDefense"] > 0:
        return int(pokemon.stat["spDefense"] * additionalModifier)
    return int(pokemon.calcModifiedStat("spDefense") * additionalModifier)


def calcSpeed(frame):
    """Calculates the speed stat of the given pokemon by calculating its modified speed stat and mulitplying it with any additional modifiers."""
    additionalModifier = 1
    if frame.user.item == "Choice Scarf":
        additionalModifier *= 1.5
    if frame.user.status and frame.user.status[0] == "Paralyzed":
        additionalModifier *= 0.5
    if (
        frame.user.ability == "Sand Rush"
        and frame.weather.currentWeather == "Sandstorm"
    ):
        additionalModifier *= 2

    return int(frame.user.calcModifiedStat("speed") * additionalModifier)


def checkBlaze(frame):
    """Returns 1.5 is user is using a fire type move and user's hp is below 1/3 of their max hp."""
    if (
        frame.attack.type == "Fire"
        and frame.user.stat["hp"] < frame.user.stat["maxHp"] // 3
    ):
        return 1.5
    return 1
