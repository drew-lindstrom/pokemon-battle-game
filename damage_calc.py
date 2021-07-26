import random
import time

from move import Move
from game_data import typeKey, typeChart, modifiedBaseDamageList
from pokemon import Pokemon
from player import Player
from terrain import checkDamageModFromTerrain
from stat_calc import *
import gameText


def rollCrit(frame, i=None):
    """Rolls to determine if a move lands a critical hit. Critical hits boost damage by 1.5 ignore the attacker's negative stat stages,
    the defender's positive stat stages, and Light Screen/Reflect/Auorar Veil. Burn is not ignored."""
    if i is None or i < 0 or i > 24:
        i = random.randint(1, 24)
    if i == 1:
        gameText.output.append("A critical hit!")
        gameText.output.append("")
        frame.crit = True
        return 1.5
    else:
        return 1


def checkStab(frame):
    """Checks to see if the attacking move is the same type as the attacker. If so, attack power is boosted by 50%."""
    if frame.attack.type in frame.user.typing:
        return 1.5
    else:
        return 1


def checkTypeEffectiveness(frame, ghostCalc=False):
    """Return the damage multiplier for how super effective the move is. typeChart is a matrix showing how each type matches up between each
    other. X-axis is the defending type, y-axis is the attacking type. Top left corner is (0, 0). Each type corresponds to a number on the
    x and y axis."""

    atkId = typeKey.get(frame.attack.type)
    def1Id = typeKey.get(frame.target.typing[0])
    mult1 = typeChart[atkId][def1Id]
    try:
        def2Id = typeKey.get(frame.target.typing[1])
        mult2 = typeChart[atkId][def2Id]
    except:
        mult2 = 1

    modifier = mult1 * mult2

    if not ghostCalc:
        if modifier > 1:
            gameText.output.append("It's super effective!")
            gameText.output.append("")
        elif modifier < 1 and modifier > 0:
            gameText.output.append("It's not very effective...")
            gameText.output.append("")
        elif modifier == 0:
            gameText.output.append("It had no effect...")
            gameText.output.append("")

    return modifier


def checkBurn(frame):
    """Returns damage modifer is user is burned and currently attacking with a physical move."""
    if frame.user.status[0] == "Burn" and frame.attack.category == "Physical":
        return 0.5
    return 1


def rollRandom(i=None):
    if i is None or i < 85 or i > 100:
        i = random.randint(85, 100)
    return float(i) / 100


def checkAttackingAndDefendingStats(frame):
    """Checks if the attack for the given frame is Physical or Special. If physical, returns Attack and Defense for stats used in damage calc.
    If special, returns Special Attack and Special Defense. If the attack is Psyshock, returns Special Attack and Defense."""
    if frame.attack.name == "Psyshock":
        attackStat = calcSpAttack(frame)
        defenseStat = calcDefense(frame)
    elif frame.attack.category == "Physical":
        attackStat = calcAttack(frame)
        defenseStat = calcDefense(frame)
    elif frame.attack.category == "Special":
        attackStat = calcSpAttack(frame)
        defenseStat = calcSpDefense(frame)

    return attackStat, defenseStat


def activateEruption(frame):
    """Returns base power for the move eruption based on the users hp."""
    return int(150 * frame.user.stat["hp"] / frame.user.stat["maxHp"])


def activateKnockOff(frame, ghostCalc=False):
    """Returns knock off base power raised by 50% if target is holding an item. Target then loses held item."""
    if frame.target.item:
        if not ghostCalc:
            gameText.output.append(
                f"{frame.target.name} lost their {frame.target.item}!"
            )
            gameText.output.append("")
            frame.target.item = None
        return int(65 * 1.5)

    else:
        return 65


def calcModifiedBaseDamage(frame, baseDamage, ghostCalc=False):
    """Returns base power for various moves that have varying base powers based on different parameters."""
    if frame.attack.name == "Eruption":
        baseDamage = activateEruption(frame)

    if frame.attack.name == "Knock Off" and frame.target.item:
        baseDamage = activateKnockOff(frame, ghostCalc)

    if frame.terrain.currentTerrain is not None:
        baseDamage *= checkDamageModFromTerrain(frame)

    return baseDamage


def calcModifiedDamage():
    pass


def calcDamage(frame, includeCrit=True, includeRandom=True, ghostCalc=False):
    """Returns damage from an attack for a given frame."""
    crit, randomMod = 1, 1

    if includeCrit == True:
        crit = rollCrit(frame)
    if includeRandom == True:
        randomMod = rollRandom()

    stab = checkStab(frame)
    typ = checkTypeEffectiveness(frame, ghostCalc)
    burn = checkBurn(frame)

    attackStat, defenseStat = checkAttackingAndDefendingStats(frame)

    baseDamage = frame.attack.power
    if frame.attack.name in modifiedBaseDamageList:
        baseDamage = calcModifiedBaseDamage(frame, baseDamage, ghostCalc)

    damage = int(
        (
            int(
                (
                    (int(2 * frame.user.level / 5) + 2)
                    * int(baseDamage)
                    * (attackStat / defenseStat)
                )
                / 50
            )
            + 2
        )
        * crit
        * stab
        * typ
        * burn
        * randomMod
    )

    return damage
