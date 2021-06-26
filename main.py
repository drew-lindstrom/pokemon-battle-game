from player import Player
from pokemon import Pokemon
from move import Move
from frame import Frame
from terrain import Terrain
from weather import Weather
from damage_calc import *
from move_effects import *
from post_attack import *
from switch_effects import *
from util import *
import ui
import ai

from teams import p1, p2


def main():
    """Main function of the program. Takes players' input for attacks, checks for win condition,
    and calls appropriate functions to apply damage and various effects."""
    ui.clearScreen()
    gameOverBool = False

    w = Weather()
    t = Terrain()

    activateTurnOneSwitchAbilities(p1, p2, w, t)

    while gameOverBool is False:

        frame1, frame2 = applyPreInputPreparations(p1, p2, w, t)
        getPlayerInputs(frame1, frame2)
        ui.clearScreen()
        # Determines which player goes first for the turn (based on speed, priority moves, etc.)
        frameOrder = getFrameOrder(frame1, frame2)

        for curFrame in frameOrder:
            if curFrame.switchChoice:
                applySwitch(curFrame, frame1, frame2)

            elif curFrame.user.status[0] != "Fainted":
                print(f"{curFrame.user.name} used {curFrame.attack.name}!")
                print()

                if checkIfCanAttackAndAttackLands(curFrame):
                    applyAttack(curFrame)

        gameOverBool = applyEndOfTurnEffects(frameOrder, w, t, gameOverBool)

        if gameOverBool:
            break


def activateTurnOneSwitchAbilities(p1, p2, w, t):
    #'Switches' leading pokemon with their respective selves in order to activate any abilities that activate on switch in.
    openingFrame1 = Frame(p1, p2, None, None, w, t)
    openingFrame1.switchChoice = 0
    openingFrame2 = Frame(p2, p1, None, None, w, t)
    openingFrame2.switchChoice = 0
    switch(openingFrame1, printText=False)
    switch(openingFrame2, printText=False)


def applyPreInputPreparations(p1, p2, w, t):
    frame1 = Frame(p1, p2, None, None, w, t)
    frame2 = Frame(p2, p1, None, None, w, t)

    ui.printPokemonOnField(frame1, frame2)

    frame1.user.checkChoiceItem()
    frame2.user.checkChoiceItem()

    return frame1, frame2


def getPlayerInputs(frame1, frame2):
    ui.getChoice(frame1)
    ai.chooseHighestDamagingAttack(frame2)


def applySwitch(curFrame, frame1, frame2):
    switch(curFrame)
    frame1.updateCurPokemon()
    frame2.updateCurPokemon()


def checkIfCanAttackAndAttackLands(frame):
    checkCanAttack(frame)
    checkAttackLands(frame)
    return frame.canAttack and frame.attackLands


def applyAttack(frame):
    category = frame.attack.category

    if category == "Physical" or category == "Special":
        frame.attackDamage = calcDamage(frame)
        frame.target.applyDamage(frame.attackDamage, None)
    else:
        applyNonDamagingMove(frame)

    applyPostAttackEffects(frame)


def applyEndOfTurnEffects(frameOrder, w, t, gameOverBool):
    applyEndOfTurnAttackEffects(frameOrder)

    w.decrementWeather()
    t.decrementTerrain()

    if checkForGameOver(frameOrder):
        gameOverBool = True
        return gameOverBool

    checkForFaintedPokemon(frameOrder)
    return gameOverBool


def checkForGameOver(frameOrder):
    for curFrame in frameOrder:
        player = curFrame.attackingTeam
        if player.checkGameOver():
            if player == p1:
                print("Player 2 Wins!")
            elif player == p2:
                print("Player 1 Wins!")
            return True
    return False


def checkForFaintedPokemon(frameOrder):
    for curFrame in frameOrder:
        player = curFrame.attackingTeam
        if player.curPokemon.status[0] == "Fainted":
            getAppropriateSwitchChoice(curFrame)
            switch(curFrame, printSwitchText=True, printStatResetText=False)


def getAppropriateSwitchChoice(frame):
    player = frame.attackingTeam
    if player == p1:
        ui.getSwitch(frame)
    if player == p2:
        ai.chooseNextPokemon(frame)


if __name__ == "__main__":
    main()
