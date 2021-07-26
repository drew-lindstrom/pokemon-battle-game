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
    """If the current attack is in the statAltAttack dictionary, rolls to see if the attack successfully
    alters a certain stat/stats of the user or target. Function then calls the updateStatModifier method to alter the approriate stat."""
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
                effectedPokemon.updateStatModifier(curMove[pos], curMove[pos + 1])
                pos += 2


def applyStatusInflictingAttack(attacker, defender, attackName, i=None):
    """If the current attack is in the statusInflictingAttack dictionary, rolls to see if the attack successfully
    applies the status to the user or target. Function then calls the setStatus method to update the pokemon's status."""
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
    """If the current attack is in the vStatusInflictingAttack dictionary, rolls to see if the attack successfully
    applies the volatile status to the user or target. Function then calls the setVStatus method to update the pokemon's status."""
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
    """Heals the user's HP at the end of the turn by 1/16 of it's max HP if holding leftovers."""
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
    """Damages a burned pokemon by 1/16 of its max HP. Fire type pokemon cannot be burned."""
    if pokemon.status[0] == "Burned":
        gameText.output.append(f"{pokemon.name} was damaged by its burn!")
        pokemon.applyDamage(None, 0.0625)


def applyPoison(pokemon):
    """Damages a baldy poison pokemon with increasingly higher damage at the end of every turn. Initially deals 1/16 of max HP
    but adds an addition 1/16 damage (up until 15 * floor(max hp/16)) every turn the pokemon is in. If the pokemon switches out,
    the damage resets to the original 1/16 of max HP.

    Damages a poisoned pokemon by 1/8 of their max hp."""
    if pokemon.status[0] == "Badly Poisoned" or pokemon.status[0] == "Poisoned":
        gameText.output.append(f"{pokemon.name} was hurt by the poison!")
        if pokemon.status[0] == "Badly Poisoned":
            pokemon.applyDamage(None, 0.0625 * (15 - pokemon.status[1]))
        if pokemon.status[0] == "Poisoned":
            pokemon.applyDamage(None, 0.125)


# TODO: incorporate with damage()?
def applyRecoil(pokemon, moveDamage, n):
    """Damages pokemon by n percentage of it's max hp. HP won't fall below 0."""
    if not pokemon.checkFainted():
        gameText.output.append(f"{pokemon.name} was damaged by recoil!")
        gameText.output.append("")
        pokemon.stat["hp"] = max(0, int(pokemon.stat["hp"] - moveDamage * n))


def applyStatic(frame, i=None):
    """30% to paralyze attacking pokemon if attack made contact."""
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
