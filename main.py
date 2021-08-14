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
from teams import createNewTeams
import ui
import ai
import gameText

from flask import Flask, request, render_template, session

import json

app = Flask(__name__)
app.secret_key = b'k6gzLIwYia'


@app.route("/")
def index():
    playerInput = request.args.get("playerInput", "")
    gameText.output = []

    if not playerInput or playerInput == "reset":
        p1, p2, gameWeather, gameTerrain = createNewGame()
        frame1, frame2 = activateTurnOneSwitchAbilities(
            p1, p2, gameWeather, gameTerrain)

    else:
        p1, p2, gameWeather, gameTerrain = loadDataFromJson()
        playerInput = int(playerInput)
        frame1, frame2 = applyPreInputPreparations(
            p1, p2, gameWeather, gameTerrain)

        if ui.validateIfPlayerChoiceIsPossible(frame1, playerInput, printTextBool=True):
            if frame1.user.checkFainted() == False:
                ai.chooseHighestDamagingAttack(frame2)

                frameOrder = getFrameOrder(frame1, frame2)

                applyTurn(frameOrder, frame1, frame2)
                applyEndOfTurnEffects(
                    frameOrder, gameWeather, gameTerrain)

                ai.checkForFaintedPokemon(frame2)
                if frame2.switchChoice:
                    applySwitch(frame2, frame1, frame2)

            # TODO: Clean up frameOrder and clean up applySwitch method.
            else:
                ai.checkForFaintedPokemon(frame2)

                frameOrder = getFrameOrder(frame1, frame2)

                for frame in frameOrder:
                    if frame.switchChoice:
                        applySwitch(frame, frame1, frame2)

        frameOrder = getFrameOrder(frame1, frame2)
        if checkForGameOver(frameOrder, p1, p2):
            return render_template("gameOver.html", player1=frame1, player2=frame2, gameText=gameText)

    updateDataToJson(p1, p2, gameWeather, gameTerrain)

    return render_template("home.html", player1=frame1, player2=frame2, gameText=gameText)


def createNewGame():
    p1, p2 = createNewTeams()
    gameWeather = Weather()
    gameTerrain = Terrain()
    return p1, p2, gameWeather, gameTerrain


def loadDataFromJson():
    p1 = Player.deserializeAndUpdatePlayerFromJson(
        json.loads(session['p1']))
    p2 = Player.deserializeAndUpdatePlayerFromJson(
        json.loads(session['p2']))
    gameWeather = Weather.deserializeAndUpdateWeatherFromJson(
        json.loads(session['weather']))
    gameTerrain = Terrain.deserializeAndUpdateTerrainFromJson(
        json.loads(session['terrain']))
    return p1, p2, gameWeather, gameTerrain


def updateDataToJson(p1, p2, gameWeather, gameTerrain):
    session['p1'] = json.dumps(p1, default=lambda o: o.__dict__, indent=4)
    session['p2'] = json.dumps(p2, default=lambda o: o.__dict__, indent=4)
    session['weather'] = json.dumps(
        gameWeather, default=lambda o: o.__dict__, indent=4)
    session['terrain'] = json.dumps(
        gameTerrain, default=lambda o: o.__dict__, indent=4)


def applyTurn(frameOrder, frame1, frame2):
    for curFrame in frameOrder:
        if curFrame.switchChoice:
            applySwitch(curFrame, frame1, frame2)

        elif curFrame.user.status[0] != "Fainted":
            gameText.output.append(
                f"{curFrame.user.name} used {curFrame.attack.name}!")
            gameText.output.append("")

            if checkIfCanAttackAndAttackLands(curFrame):
                applyAttack(curFrame)


def activateTurnOneSwitchAbilities(p1, p2, w, t):
    openingFrame1 = Frame(p1, p2, None, None, w, t)
    openingFrame1.switchChoice = 0
    openingFrame2 = Frame(p2, p1, None, None, w, t)
    openingFrame2.switchChoice = 0
    switch(openingFrame1, printSwitchText=False, printStatResetText=False)
    switch(openingFrame2, printSwitchText=False, printStatResetText=False)
    return openingFrame1, openingFrame2


def applyPreInputPreparations(p1, p2, w, t):
    frame1 = Frame(p1, p2, None, None, w, t)
    frame2 = Frame(p2, p1, None, None, w, t)

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


def applyEndOfTurnEffects(frameOrder, w, t):
    applyEndOfTurnAttackEffects(frameOrder)

    w.decrementWeather()
    t.decrementTerrain()


def checkForGameOver(frameOrder, p1, p2):
    for curFrame in frameOrder:
        player = curFrame.attackingTeam
        if player.checkGameOver():
            if player == p1:
                gameText.output.append("Player 2 Wins!")
            elif player == p2:
                gameText.output.append("Player 1 Wins!")
            return True
    return False


if __name__ == "__main__":
    app.run(debug=True)
