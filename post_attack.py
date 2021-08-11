from pokemon import Pokemon
from game_data import (
    statAltAttacks,
    statusInflictingAttacks,
    vStatusInflictingAttacks,
    contactAttacks,
)
import random
import gameText


def applyStatAltAttack(attacker, defender, attackName, i=None):
    if attackName in statAltAttacks:
        curMove = statAltAttacks[attackName]
        if i is None:
            i = random.randint(1, 100)

        if i <= curMove[1]:
            if curMove[0] == "user":
                effectedPokemon = attacker
            else:
                effectedPokemon = defender
            pos = 2
            while pos < len(curMove):
                effectedPokemon.updateStatModifier(
                    curMove[pos], curMove[pos + 1])
                pos += 2


def applyStatusInflictingAttack(attacker, defender, attackName, i=None):
    if attackName in statusInflictingAttacks:
        curMove = statusInflictingAttacks[attackName]
        if i is None:
            i = random.randint(1, 100)

        if i <= curMove[1]:
            if curMove[0] == "user":
                effectedPokemon = attacker
            else:
                effectedPokemon = defender
            effectedPokemon.setStatus(curMove[2])


def applyVStatusInflictingAttack(attacker, defender, attackName, i=None):
    if attackName in vStatusInflictingAttacks:
        curMove = vStatusInflictingAttacks[attackName]
        if i is None:
            i = random.randint(1, 100)

        if i <= curMove[1]:
            if curMove[0] == "user":
                effectedPokemon = attacker
            else:
                effectedPokemon = defender
            effectedPokemon.setVStatus(curMove[2])


def applyLeftovers(pokemon):
    if (
        pokemon.item == "Leftovers"
        and pokemon.stat["hp"] != pokemon.stat["maxHp"]
        and not pokemon.checkFainted()
    ):
        gameText.output.append(
            f"{pokemon.name} healed some of it's HP with it's leftovers."
        )
        pokemon.applyHeal(0.0625)


def applyBurn(pokemon):
    if pokemon.status[0] == "Burned":
        gameText.output.append(f"{pokemon.name} was damaged by its burn!")
        pokemon.applyDamage(None, 0.0625)


def applyPoison(pokemon):
    if pokemon.status[0] == "Badly Poisoned" or pokemon.status[0] == "Poisoned":
        gameText.output.append(f"{pokemon.name} was hurt by the poison!")
        if pokemon.status[0] == "Badly Poisoned":
            pokemon.applyDamage(None, 0.0625 * (15 - pokemon.status[1]))
        if pokemon.status[0] == "Poisoned":
            pokemon.applyDamage(None, 0.125)


def applyRecoil(pokemon, moveDamage, n):
    if not pokemon.checkFainted():
        gameText.output.append(f"{pokemon.name} was damaged by recoil!")
        gameText.output.append("")
        pokemon.stat["hp"] = max(0, int(pokemon.stat["hp"] - moveDamage * n))


def applyStatic(frame, i=None):
    if (
        frame.user.item != "Protective Pads"
        and frame.attack.name in contactAttacks
        and frame.user.status[0] == None
    ):
        if i is None:
            i = random.randint(1, 100)

        if i <= 30:
            gameText.output.append(
                f"{frame.user.name} was paralyzed by {frame.target.name}s Static!"
            )
            gameText.output.append("")
            frame.user.setStatus("Paralyzed")
