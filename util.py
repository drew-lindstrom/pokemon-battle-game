from post_attack import *
from switch_effects import *
from weather import *
from terrain import *
from random import *
import move_effects
from game_data import priorityMoves, typeKey, typeChart
from stat_calc import calcSpeed
import gameText


def getFrameOrder(frame1, frame2):
    if frame1.attack and frame1.attack.name == "Pursuit" and frame2.switchChoice:
        return [frame1, frame2]
    elif frame2.attack and frame2.attack.name == "Pursuit" and frame1.switchChoice:
        return [frame1, frame2]

    if frame1.switchChoice and frame2.attack:
        return [frame1, frame2]
    elif frame2.switchChoice and frame1.attack:
        return [frame2, frame1]

    priorityP1 = checkPriority(frame1)
    priorityP2 = checkPriority(frame2)

    if priorityP1 == priorityP2:
        return checkSpeed(frame1, frame2)
    elif priorityP1 > priorityP2:
        return [frame1, frame2]
    else:
        return [frame2, frame1]


def checkSpeed(frame1, frame2):
    p1Speed = calcSpeed(frame1)
    p2Speed = calcSpeed(frame2)

    if p1Speed > p2Speed:
        return [frame1, frame2]
    else:
        return [frame2, frame1]


def checkPriority(frame):
    if (
        frame.terrain.currentTerrain == "Psychic Terrain"
        and frame.target.grounded == True
    ):
        return 0
    if (
        frame.terrain.currentTerrain == "Grassy Terrain"
        and frame.attack.name == "Grassy Glide"
    ):
        return 1

    try:
        return priorityMoves[frame.attack.name]
    except Exception:
        return 0


def rollParalysis(user, i=None):
    if i == None or i < 1 or i > 4:
        i = randint(1, 4)

    if i == 1:
        gameText.output.append(f"{user.name} is paralyzed and can't move.")
        gameText.output.append("")
        return False
    return True


def rollFrozen(user, i=None):
    if i == None or i < 1 or i > 5:
        i = randint(1, 5)

    if i == 1:
        gameText.output.append(f"{user.name} thawed out!")
        gameText.output.append("")
        user.cureStatus()
        return True
    gameText.output.append(f"{user.name} is frozen and cant attack!")
    gameText.output.append("")
    return False


def rollConfusion(user, i=None):
    if i == None or i < 1 or i > 2:
        i = randint(1, 2)

    if i == 1:
        gameText.output.append(f"{user.name} hit its self in confusion!")
        gameText.output.append("")
        user.applyDamage(calcConfusionDamage(user), None)
        return False
    return True


def calcConfusionDamage(user):
    # TODO: Need to add random to damage calc. Probably better to combine this with calcDamage function.
    randomMod = 1

    damage = int(
        (
            int(
                (
                    (int(2 * user.level / 5) + 2)
                    * 40
                    * (user.stat["attack"] / user.stat["defense"])
                )
                / 50
            )
            + 2
        )
        * randomMod
    )

    return damage


def checkImmunity(frame):
    frame.target.checkGrounded()
    if (
        (frame.attack.type == "Poison" and "Steel" in frame.target.typing)
        or (frame.attack.type == "Dragon" and "Fairy" in frame.target.typing)
        or (
            (frame.attack.type == "Normal" or frame.attack.type == "Fighting")
            and "Ghost" in frame.target.typing
        )
        or (frame.attack.type == "Ghost" and "Normal" in frame.target.typing)
        or (frame.attack.type == "Electric" and "Ground" in frame.target.typing)
        or (frame.attack.type == "Psychic" and "Dark" in frame.target.typing)
        or (frame.attack.type == "Ground" and frame.target.grounded == False)
    ):
        return False
    return True


def checkCanAttack(frame, i=None):
    if frame.user.status[0] == "Paralyzed":
        if not rollParalysis(frame.user, i):
            frame.canAttack = False
            return

    if frame.user.status[0] == "Asleep" and frame.attack.name != "Sleep Talk":
        gameText.output.append(f"{frame.user.name} is asleep.")
        gameText.output.append("")
        frame.canAttack = False
        return

    if frame.user.status[0] == "Frozen":
        if not rollFrozen(frame.user, i):
            frame.canAttack = False
            return

    if "Confusion" in frame.user.vStatus:
        if not rollConfusion(frame.user, i):
            frame.canAttack = False
            return

    if "Flinched" in frame.user.vStatus:
        gameText.output.append(f"{frame.user.name} flinched!")
        gameText.output.append("")
        frame.canAttack = False
        return

    if not checkImmunity(frame):
        gameText.output.append(f"It had no effect.")
        gameText.output.append("")
        frame.canAttack = False
        return

    if frame.attack.type == "Fire" and frame.target.ability == "Flash Fire":
        gameText.output.append(
            f"{frame.target.name}s attack was boosted by Flash Fire!"
        )
        gameText.output.append("")
        frame.target.updateStatModifier("attack", 1)
        frame.target.updateStatModifier("spAttack", 1)
        frame.canAttack = False
        return
    frame.canAttack = True
    return


def checkAttackLands(frame, i=None):
    if frame.attack.accuracy == 0:
        frame.attackLands = True
        return

    additionalModifier = 1

    accuracyEvasionStat = frame.user.calcModifiedStat(
        "accuracy"
    ) - frame.target.calcModifiedStat("evasion")

    if accuracyEvasionStat < -6:
        accuracyEvasionStat = -6

    if accuracyEvasionStat < 0:
        accuracyEvasionStat = 3 / (3 + accuracyEvasionStat * -1)
    elif accuracyEvasionStat > 0:
        accuracyEvasionStat = (3 + accuracyEvasionStat) / 3
    else:
        accuracyEvasionStat = 1

    a = frame.attack.accuracy * accuracyEvasionStat * additionalModifier

    if i is None or i < 0 or i > 100:
        i = randint(0, 100)

    if i <= a:
        frame.attackLands = True
        return

    gameText.output.append(f"{frame.user.name}s attack missed!")
    gameText.output.append("")

    if frame.attack.name == "High Jump Kick":
        gameText.output.append(f"{frame.user.name} came crashing down...")
        gameText.output.append("")
        frame.user.applyDamage(None, 0.5)


def applyNonDamagingMove(frame):
    if frame.attack.name == "Stealth Rock":
        move_effects.setStealthRocks(frame)

    if frame.attack.name == "Defog":
        move_effects.activateDefog(frame)

    if frame.attack.name == "Toxic":
        frame.target.setStatus("Badly Poisoned")

    if frame.attack.name == "Roost":
        move_effects.activateRoost(frame)

    if frame.attack.name == "Slack Off":
        move_effects.activateSlackOff(frame)


def switch(frame, printSwitchText=True, printStatResetText=True):
    n = int(frame.switchChoice)
    if frame.attackingTeam.team[n].stat["hp"] == 0:
        gameText.output.append(
            f"{frame.attackingTeam.team[n].name} has already fainted!"
        )
        gameText.output.append("")
    else:
        frame.attackingTeam.team[0], frame.attackingTeam.team[n] = (
            frame.attackingTeam.team[n],
            frame.attackingTeam.team[0],
        )
        frame.user = frame.attackingTeam[0]
        frame.attackingTeam.curPokemon = frame.attackingTeam.team[0]
        if printSwitchText:
            gameText.output.append(
                f"{frame.attackingTeam.team[n].name} switched with {frame.attackingTeam.team[0].name}."
            )
            gameText.output.append("")
        frame.attackingTeam.team[n].resetPreviousMove()
        frame.attackingTeam.team[n].resetStatModifier(printStatResetText)
        frame.attackingTeam.team[n].resetStatuses()
        applySwitchEffect(frame, n, "Out")
        applySwitchEffect(frame, 0, "In")
        applyEntryHazards(frame)


def applySwitchEffect(frame, n, switchDir):
    user = frame.attackingTeam[n]
    if switchDir == "In":
        if user.ability == "Grassy Surge":
            activateGrassySurge(user, frame.terrain)

        if user.ability == "Intimidate":
            activateIntimidate(user, frame.target)

        if user.ability == "Psychic Surge":
            activatePsychicSurge(user, frame.terrain)

        if user.ability == "Sand Stream":
            activateSandStream(user, frame.weather)

    if switchDir == "Out":
        if user.ability == "Regenerator":
            activateRegenerator(user)


def applyEntryHazards(frame):
    if (
        frame.user.item != "Heavy Duty Boots"
        and frame.attackingTeam.stealthRocks == True
    ):
        applyStealthRocksDamage(frame)
    else:
        pass


def applyStealthRocksDamage(frame):
    atkId = typeKey.get("Rock")
    def1Id = typeKey.get(frame.user.typing[0])
    mult1 = typeChart[atkId][def1Id]
    try:
        def2Id = typeKey.get(frame.user.typing[1])
        mult2 = typeChart[atkId][def2Id]
    except:
        mult2 = 1

    gameText.output.append(f"Pointed stones dug into {frame.user.name}!")
    gameText.output.append("")

    frame.user.applyDamage(None, 0.125 * mult1 * mult2)


def applyPostAttackEffects(frame, i=None):
    applyStatAltAttack(frame.user, frame.target, frame.attack.name)
    applyStatusInflictingAttack(frame.user, frame.target, frame.attack.name)
    applyVStatusInflictingAttack(frame.user, frame.target, frame.attack.name)
    if frame.target.ability == "Static":
        applyStatic(frame, i)


def applyEndOfTurnAttackEffects(frameOrder):
    for frame in frameOrder:
        frame.user.decrementStatuses()
        if not frame.switchChoice:
            frame.attack.decrementPp()

    if (
        frameOrder[0].weather.currentWeather == "Sandstorm"
        or frameOrder[0].weather.currentWeather == "Hail"
    ):
        for frame in frameOrder:
            applyWeatherDamage(frame.weather, frame.user)

    if frameOrder[0].terrain.currentTerrain == "Grassy Terrain":
        for frame in frameOrder:
            healFromGrassyTerrain(frame.terrain, frame.user)

    for frame in frameOrder:
        if frame.user.item == "Leftovers":
            applyLeftovers(frame.user)

    for frame in frameOrder:
        if frame.user.status[0] == "Burned":
            applyBurn(frame.user)

    for frame in frameOrder:
        if (
            frame.user.status[0] == "Badly Poisoned"
            or frame.user.status[0] == "Poisoned"
        ):
            applyPoison(frame.user)

    for frame in frameOrder:
        if frame.attack and frame.attack.name == "Wood Hammer":
            applyRecoil(frame.user, frame.attackDamage, 0.33)

    for frame in frameOrder:
        if frame.attack:
            frame.user.setPreviousMove(frame.attack.name)
