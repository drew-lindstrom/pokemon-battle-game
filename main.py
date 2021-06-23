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
    game_over_bool = False

    w = Weather()
    t = Terrain()

    #'Switches' leading pokemon with their respective selves in order to activate any abilities that activate on switch in.
    opening_frame_1 = Frame(p1, p2, None, None, w, t)
    opening_frame_1.switch_choice = 0
    opening_frame_2 = Frame(p2, p1, None, None, w, t)
    opening_frame_2.switch_choice = 0
    switch(opening_frame_1)
    switch(opening_frame_2)

    while game_over_bool is False:
        frame1 = Frame(p1, p2, None, None, w, t)
        frame2 = Frame(p2, p1, None, None, w, t)

        ui.printPokemonOnField(frame1, frame2)

        frame1.user.check_choice_item()
        frame2.user.check_choice_item()

        # Gets input on what each player wants to do before the given turn.
        ui.getChoice(frame1)
        ai.choose_highest_damaging_attack(frame2)

        ui.clearScreen()

        # Determines which player goes first for the turn (based on speed, priority moves, etc.)
        frame_order = get_frame_order(frame1, frame2)

        for cur_frame in frame_order:
            if cur_frame.switch_choice:
                switch(cur_frame)
                frame1.update_cur_pokemon()
                frame2.update_cur_pokemon()
            elif cur_frame.user.status[0] != "Fainted":
                print(f"{cur_frame.user.name} used {cur_frame.attack.name}!")
                print()

                cur_frame.can_attack = check_can_attack(cur_frame)
                check_attack_lands(cur_frame)
                if cur_frame.can_attack and cur_frame.attack_lands:
                    if (
                        cur_frame.attack.category == "Physical"
                        or cur_frame.attack.category == "Special"
                    ):
                        cur_frame.attack_damage = calc_damage(cur_frame)
                        cur_frame.target.apply_damage(cur_frame.attack_damage, None)

                    else:
                        apply_non_damaging_move(cur_frame)
                    apply_post_attack_effects(cur_frame)

        apply_end_of_turn_effects(frame_order)

        w.decrement_weather()
        t.decrement_terrain()

        for cur_frame in frame_order:
            player = cur_frame.attacking_team
            # Game over check
            if player.check_game_over():
                if player == p1:
                    print("Player 2 Wins!")
                elif player == p2:
                    print("Player 1 Wins!")
                game_over_bool = True
                break
            # Prompts player to switch any fainted pokemon at end of turn.
            if player.cur_pokemon.status[0] == "Fainted":
                if player == p1:
                    ui.getSwitch(cur_frame)
                    switch(cur_frame)
                if player == p2:
                    ai.choose_next_pokemon(cur_frame)
                    switch(cur_frame)


if __name__ == "__main__":

    main()
