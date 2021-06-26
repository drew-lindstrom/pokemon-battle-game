from post_attack import *
from switch_effects import *
from weather import *
from terrain import *
from random import *
import move_effects
from game_data import priorityMoves, typeKey, typeChart
from stat_calc import calcSpeed


def getFrameOrder(frame1, frame2):
    """Gets the turn order for the current turn of the game.
    Turn order is determined by the speeds of the current pokemon on the field.
    With the exception of the effects from certian moves, items, or abilities,
    the faster pokemon always switches or attacks before the slower pokemon.
    Switching to a different pokemon always occurs before a pokemon attacks (unless the opposing pokemon uses the move Pursuit)."""
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
    """Checks the speed of both pokemon on field to determine who moves first.
    Takes into account things like Choice Scarf, abilities that effect priority or speed, priority moves, paraylsis, etc."""
    p1Speed = calcSpeed(frame1)
    p2Speed = calcSpeed(frame2)

    if p1Speed > p2Speed:
        return [frame1, frame2]
    # If the speed check is a tie, its usually random who goes first, but for the sake of AI consistency, the opponent will always go first.
    else:
        return [frame2, frame1]


def checkPriority(frame):
    """Calls priorityMoves dictionary to see if the given attack has a priority number, if not returns 0.
    Attacks with a priority higher number will go before the opponent's attack regardless of speed.
    Standard moves have a prioirty of 0. If both pokemon use a move with the same priority, speed is used to determine who goes first."""

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
    """Rolls to determine if a paralyzed pokemon can successfully use an attack. 25% that pokemon won't be able to move due to paralysis."""
    if i == None or i < 1 or i > 4:
        i = randint(1, 4)

    if i == 1:
        print(f"{user.name} is paralyzed and can't move.")
        return False
    return True


def rollFrozen(user, i=None):
    """Rolls to determine if a frozen pokemon thaws out during it's attack. Frozen pokemon are not able to attack. 20% chance to thaw out.
    The pokemon can use it's attack on the turn that it thaws out."""
    if i == None or i < 1 or i > 5:
        i = randint(1, 5)

    if i == 1:
        print(f"{user.name} thawed out!")
        user.cureStatus()
        return True
    print(f"{user.name} is frozen and cant attack!")
    print()
    return False


def rollConfusion(user, i=None):
    """Rolls to determine if a confused pokemon can successfully use an attack. 33% chance they will hit themselves in confusion."""
    if i == None or i < 1 or i > 2:
        i = randint(1, 2)

    if i == 1:
        print(f"{user.name} hit its self in confusion!")
        user.applyDamage(calcConfusionDamage(user), None)
        return False
    return True


def calcConfusionDamage(user):
    """Returns damage inflicted by a pokemon to itself if they hit themselves in confusion."""
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
    """Returns boolean if current attack isn't able to land due to target being immune to the attack's type."""
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
    """Checks to make sure if an attacker is able to use a move based on any present status conditions.
    Calls functions that require a roll for an attack to be successful (like paralysis or confusion)."""
    if frame.user.status[0] == "Paralyzed":
        if not rollParalysis(frame.user, i):
            frame.canAttack = False
            return

    if frame.user.status[0] == "Asleep" and frame.attack.name != "Sleep Talk":
        print(f"{frame.user.name} is asleep.")
        print()
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
        print(f"{frame.user.name} flinched!")
        print()
        frame.canAttack = False
        return

    if not checkImmunity(frame):
        print(f"It had no effect.")
        print()
        frame.canAttack = False
        return

    if frame.attack.type == "Fire" and frame.target.ability == "Flash Fire":
        print(f"{frame.target.name}s attack was boosted by Flash Fire!")
        print()
        frame.target.updateStatModifier("attack", 1)
        frame.target.updateStatModifier("spAttack", 1)
        frame.canAttack = False
        return
    frame.canAttack = True
    return


def checkAttackLands(frame, i=None):
    """Calculates required accuracy for an attack to land based on the accuracy of the attack,
    accuracy of user, evasion of target, and any additional modifiers. Rolls i in range 0 to 100.
    If i is less than or equal to required accuracy, attack hits and function returns True."""
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

    print(f"{frame.user.name}s attack missed!")
    print()

    # If high jump kick misses, it damages the user.
    if frame.attack.name == "High Jump Kick":
        print(f"{frame.user.name} came crashing down...")
        frame.user.applyDamage(None, 0.5)


def applyNonDamagingMove(frame):
    """Applies effect of current non damaging move being used."""
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


def switch(frame, printText=True):
    """Switch current pokemon with another pokemon on player's team. Won't work if player's choice to switch into is already fainted.
    Ex: Player team order is [Tyranitar, Slowbro] -> playerTeam.switch(1) -> Player team order is [Slowbro, Tyranitar]"""
    n = int(frame.switchChoice)
    if frame.attackingTeam.team[n].stat["hp"] == 0:
        if printText:
            print(f"{frame.attackingTeam.team[n].name} has already fainted!")
            print()
    else:
        frame.attackingTeam.team[0], frame.attackingTeam.team[n] = (
            frame.attackingTeam.team[n],
            frame.attackingTeam.team[0],
        )
        frame.user = frame.attackingTeam[0]
        frame.attackingTeam.curPokemon = frame.attackingTeam.team[0]
        if printText:
            print(
                f"{frame.attackingTeam.team[n].name} switched with {frame.attackingTeam.team[0].name}."
            )
            print()
        frame.attackingTeam.team[n].resetPreviousMove()
        frame.attackingTeam.team[n].resetStatModifier(printText)
        frame.attackingTeam.team[n].resetStatuses()
        applySwitchEffect(frame, n, "Out")
        applySwitchEffect(frame, 0, "In")
        applyEntryHazards(frame)


def applySwitchEffect(frame, n, switchDir):
    """Applies switch effect for current pokemon that's switched in or switched out."""
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
    """Applies the appropriate entry hazards effects after a pokemon switches in.
    Calls funciton to clear toxic spikes if target if a grounded poison type."""
    if (
        frame.user.item != "Heavy Duty Boots"
        and frame.attackingTeam.stealthRocks == True
    ):
        applyStealthRocksDamage(frame)
    else:
        pass


def applyStealthRocksDamage(frame):
    """Applies stealth rock damage to the target depending on target's weakness to Rock."""
    atkId = typeKey.get("Rock")
    def1Id = typeKey.get(frame.user.typing[0])
    mult1 = typeChart[atkId][def1Id]
    try:
        def2Id = typeKey.get(frame.user.typing[1])
        mult2 = typeChart[atkId][def2Id]
    except:
        mult2 = 1

    print(f"Pointed stones dug into {frame.user.name}!")
    print()

    frame.user.applyDamage(None, 0.125 * mult1 * mult2)


def applyPostAttackEffects(frame, i=None):
    """Applies post attack effects (lowering or raising stats, applying a status, etc) to the user/target of the given frame."""
    applyStatAltAttack(frame.user, frame.target, frame.attack.name)
    applyStatusInflictingAttack(frame.user, frame.target, frame.attack.name)
    applyVStatusInflictingAttack(frame.user, frame.target, frame.attack.name)
    if frame.target.ability == "Static":
        applyStatic(frame, i)


def applyEndOfTurnAttackEffects(frameOrder):
    """Applies end of turn events (recoil, leftovers healing, etc) to the user of the given frame."""
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