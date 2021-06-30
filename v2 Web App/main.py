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
from teams import p1, p2
import ui
import ai
import gameText

from flask import Flask, request, escape

app = Flask(__name__)

gameOverBool = False
w = Weather()
t = Terrain()


@app.route("/")
def index():
    playerInput = int(escape(request.args.get("playerInput", "")))
    gameText.output = ""

    if playerInput:
        frame1, frame2 = applyPreInputPreparations(p1, p2, w, t)
        callAppropriateFunctionBasedOnChoice(frame1, playerInput)
        ai.chooseHighestDamagingAttack(frame2)
        if applyTurn(frame1, frame2):
            return (
                """<form action="" method="get">
                <input type="text" name="playerInput">
                <input type="submit" value="Enter Input">
            </form>"""
                + gameText.output
            )
        else:
            return "Game Over"

    else:
        activateTurnOneSwitchAbilities(p1, p2, w, t)
        return (
            """<form action="" method="get">
            <input type="text" name="playerInput">
            <input type="submit" value="Enter Input">
        </form>"""
            + gameText.output
        )


def callAppropriateFunctionBasedOnChoice(
    frame, choice, inputList=[], printTextBool=False
):
    if choice >= 0 and choice <= 3:
        if checkIfValidChoice(frame, choice, printTextBool):
            frame.attack = frame.user.moves[choice - 1]
            return True

    elif choice >= 4 and choice <= 9:
        if checkIfSwitchChoiceHasFainted(frame, inputList):
            frame.switchChoice = choice - 3
            return True
    return False


def checkIfValidChoice(frame, choice, printTextBool=False):
    if checkIfChoiceHasEnoughPP(
        frame, choice, printTextBool
    ) and checkIfUserHasMoveLock(frame, choice, printTextBool):
        return True
    return False


def checkIfChoiceHasEnoughPP(frame, choice, printTextBool=False):
    if frame.user.moves[choice - 1].pp <= 0:
        if printTextBool:
            gameText.output += f"{frame.user.moves[choice - 1].name} is out of PP.\n"
        return False
    return True


def checkIfUserHasMoveLock(frame, choice, printTextBool=False):
    if "Move Lock" in frame.user.vStatus and (
        frame.user.prevMove != None
        and frame.user.prevMove != frame.user.moves[choice - 1].name
    ):
        if printTextBool:
            gameText.output += f"{frame.user.name} must use {frame.user.prevMove}.\n"
        return False
    return True


def checkIfSwitchChoiceHasFainted(frame, switchChoice):
    switchChoice = switchChoice - 3

    if frame.attackingTeam[switchChoice].status[0] == "Fainted":
        return False
    return True


def applyTurn(frame1, frame2):
    # Determines which player goes first for the turn (based on speed, priority moves, etc.)
    frameOrder = getFrameOrder(frame1, frame2)

    for curFrame in frameOrder:
        if curFrame.switchChoice:
            applySwitch(curFrame, frame1, frame2)

        elif curFrame.user.status[0] != "Fainted":
            gameText.output += f"{curFrame.user.name} used {curFrame.attack.name}!\n"

            if checkIfCanAttackAndAttackLands(curFrame):
                applyAttack(curFrame)

    gameOverBool = applyEndOfTurnEffects(frameOrder, w, t, gameOverBool)

    if gameOverBool:
        return False
    return True


def activateTurnOneSwitchAbilities(p1, p2, w, t):
    #'Switches' leading pokemon with their respective selves in order to activate any abilities that activate on switch in.
    openingFrame1 = Frame(p1, p2, None, None, w, t)
    openingFrame1.switchChoice = 0
    openingFrame2 = Frame(p2, p1, None, None, w, t)
    openingFrame2.switchChoice = 0
    switch(openingFrame1, printSwitchText=False)
    switch(openingFrame2, printSwitchText=False)


def applyPreInputPreparations(p1, p2, w, t):
    frame1 = Frame(p1, p2, None, None, w, t)
    frame2 = Frame(p2, p1, None, None, w, t)

    gameTextList = []
    frame1.gameText = gameTextList
    frame2.gameText = gameTextList

    frame1.user.checkChoiceItem()
    frame2.user.checkChoiceItem()

    return frame1, frame2


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
                gameText.output += "Player 2 Wins!\n"
            elif player == p2:
                gameText.output += "Player 1 Wins!\n"
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
    app.run(host="127.0.0.1", port=8080, debug=True)