from player import Player
from pokemon import Pokemon
from move import Move
from game_data import priority_moves
import ui


def get_turn_order(p1_cur_pokemon, p1_choice, p2_cur_pokemon, p2_choice):
    """Gets the turn order for the current turn of the game.
    Turn order is determined by the speeds of the current pokemon on the field.
    With the exception of the effects from certian moves, items, or abilities,
    the faster pokemon always switches or attacks before the slower pokemon.
    Switching to a different pokemon always occurs before a pokemon attacks (unless the opposing pokemon uses the move Pursuit)."""
    if p1_choice[1] == "Pursuit" and p2_choice[1] == "Switch":
        return [p1_choice, p2_choice]
    elif p2_choice[1] == "Pursuit" and p1_choice[1] == "Switch":
        return [p2_choice, p1_choice]

    if p1_choice[1] == "Switch" and p2_choice[1] != "Switch":
        return [p1_choice, p2_choice]
    elif p2_choice[1] == "Switch" and p1_choice[1] != "Switch":
        return [p2_choice, p1_choice]

    priority_p1 = check_priority(p1_choice)
    priority_p2 = check_priority(p2_choice)

    if priority_p1 == priority_p2:
        return check_speed(p1_cur_pokemon, p1_choice, p2_cur_pokemon, p2_choice)
    elif priority_p1 > priority_p2:
        return [p1_choice, p2_choice]
    else:
        return [p2_choice, p2_choice]


def check_speed(p1_cur_pokemon, p1_choice, p2_cur_pokemon, p2_choice):
    """Checks the speed of both pokemon on field to determine who moves first.
    Takes into account things like Choice Scarf, abilities that effect priority or speed, priority moves, paraylsis, etc."""
    p1_speed = p1_cur_pokemon.calc_modified_stat("speed")
    p2_speed = p2_cur_pokemon.calc_modified_stat("speed")

    if p1_cur_pokemon.status == "Paralyzed":
        p1_speed *= 0.5

    if p2_cur_pokemon.status == "Paralyzed":
        p2_speed *= 0.5

    if p1_speed > p2_speed:
        return [p1_choice, p2_choice]
    # If the speed check is a tie, its usually random who goes first, but for the sake of AI consistency, the opponent will always go first.
    else:
        return [p2_choice, p1_choice]


def check_priority(attack):
    """Calls priority_moves dictionary to see if the given attack has a priority number, if not returns 0.
    Attacks with a priority higher number will go before the opponent's attack regardless of speed.
    Standard moves have a prioirty of 0. If both pokemon use a move with the same priority, speed is used to determine who goes first."""
    try:
        return priority_moves[attack]
    except Exception:
        return 0


def main():
    """Main function of the program. Takes players' input for attacks, checks for win condition,
    and calls appropriate functions to apply damage and various effects."""
    while True:
        ui.print_pokemon_on_field(p1.cur_pokemon, p2.cur_pokemon)

        p1_choice = ui.get_choice(p1)
        p2_choice = ui.get_choice(p2)

        turn_order = get_turn_order(
            p1.cur_pokemon, p1_choice, p2.cur_pokemon, p2_choice
        )

        for choice in turn_order:
            player, move_name, n = choice
            if move_name == "Switch":
                player.switch[n]
            else:
                attack(player.cur_pokemon, move_name, n)

        if p1.game_over_check() and p2.game_over_check():
            print("Its a Draw!")
            break

        elif p1.game_over_check():
            print("Player 2 Wins!")
            break

        elif p2.game_over_check():
            print("Player 1 Wins!")
            break


if __name__ == "__main__":
    main()
