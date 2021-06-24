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

    #'Switches' leading pokemon with their respective selves in order to activate any abilities that activate on switch in.
    openingFrame1 = Frame(p1, p2, None, None, w, t)
    openingFrame1.switchChoice = 0
    openingFrame2 = Frame(p2, p1, None, None, w, t)
    openingFrame2.switchChoice = 0
    switch(openingFrame1)
    switch(openingFrame2)

    while gameOverBool is False:
        frame1 = Frame(p1, p2, None, None, w, t)
        frame2 = Frame(p2, p1, None, None, w, t)

        ui.printPokemonOnField(frame1, frame2)

        frame1.user.checkChoiceItem()
        frame2.user.checkChoiceItem()

        # Gets input on what each player wants to do before the given turn.
        ui.getChoice(frame1)
        ai.chooseHighestDamagingAttack(frame2)

        ui.clearScreen()

        # Determines which player goes first for the turn (based on speed, priority moves, etc.)
        frameOrder = getFrameOrder(frame1, frame2)

        for curFrame in frameOrder:
            if curFrame.switchChoice:
                switch(curFrame)
                frame1.updateCurPokemon()
                frame2.updateCurPokemon()
            elif curFrame.user.status[0] != "Fainted":
                print(f"{curFrame.user.name} used {curFrame.attack.name}!")
                print()

                curFrame.canAttack = checkCanAttack(curFrame)
                checkAttackLands(curFrame)
                if curFrame.canAttack and curFrame.attackLands:
                    if (
                        curFrame.attack.category == "Physical"
                        or curFrame.attack.category == "Special"
                    ):
                        curFrame.attackDamage = calcDamage(curFrame)
                        curFrame.target.applyDamage(curFrame.attackDamage, None)

                    else:
                        applyNonDamagingMove(curFrame)
                    applyPostAttackEffects(curFrame)

        applyEndOfTurnEffects(frameOrder)

        w.decrementWeather()
        t.decrementTerrain()

        for curFrame in frameOrder:
            player = curFrame.attackingTeam
            # Game over check
            if player.checkGameOver():
                if player == p1:
                    print("Player 2 Wins!")
                elif player == p2:
                    print("Player 1 Wins!")
                gameOverBool = True
                break
            # Prompts player to switch any fainted pokemon at end of turn.
            if player.curPokemon.status[0] == "Fainted":
                if player == p1:
                    ui.getSwitch(curFrame)
                    switch(curFrame)
                if player == p2:
                    ai.chooseNextPokemon(curFrame)
                    switch(curFrame)


if __name__ == "__main__":

    main()
