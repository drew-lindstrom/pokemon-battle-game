from player import Player
from pokemon import Pokemon
from move import Move
from game_data import priority_moves
from stat_calc import calc_speed
import ui
import random


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

    priority_p1 = check_priority(p1_choice[1])
    priority_p2 = check_priority(p2_choice[1])

    if priority_p1 == priority_p2:
        return check_speed(p1_cur_pokemon, p1_choice, p2_cur_pokemon, p2_choice)
    elif priority_p1 > priority_p2:
        return [p1_choice, p2_choice]
    else:
        return [p2_choice, p1_choice]


def check_speed(p1_cur_pokemon, p1_choice, p2_cur_pokemon, p2_choice):
    """Checks the speed of both pokemon on field to determine who moves first.
    Takes into account things like Choice Scarf, abilities that effect priority or speed, priority moves, paraylsis, etc."""
    p1_speed = calc_speed(p1_choice[0])
    p2_speed = calc_speed(p2_choice[0])

    if p1_speed > p2_speed:
        return [p1_choice, p2_choice]
    # If the speed check is a tie, its usually random who goes first, but for the sake of AI consistency, the opponent will always go first.
    else:
        return [p2_choice, p1_choice]


def check_priority(attack, terrain):
    """Calls priority_moves dictionary to see if the given attack has a priority number, if not returns 0.
    Attacks with a priority higher number will go before the opponent's attack regardless of speed.
    Standard moves have a prioirty of 0. If both pokemon use a move with the same priority, speed is used to determine who goes first."""
    try:
        return priority_moves[attack]
    except Exception:
        if attack == "Grassy Glide" and terrain == "Grassy Terrain":
            return 1
        return 0


def roll_sleep():
    pass


def roll_frozen(user, i=None):
    """Rolls to determine if a frozen pokemon thaws out during it's attack. Frozen pokemon are not able to attack. 20% chance to thaw out.
    The pokemon can use it's attack on the turn that it thaws out."""
    if i == None or i < 1 or i > 5:
        i = random.randint(1, 5)

    if i == 1:
        print(f"{user.name} thawed out!")
        user.cure_status()
        return False
    return True


def roll_paralysis(user, i=None):
    """Rolls to determine if a paralyzed pokemon can successfully use an attack. 25% that pokemon won't be able to move due to paralysis."""
    if i == None or i < 1 or i > 4:
        i = random.randint(1, 4)

    if i == 1:
        print(f"{user.name} is paralyzed and can't move.")
        return True
    return False


def roll_accuracy():
    pass


def roll_evasion():
    pass


def roll_confusion():
    pass


# def roll_infatuation():
#     pass


# def check_semi_invulnerable_turn():
#     pass


# def check_recharging():
#     pass


# def check_charging_turn():
#     pass


# def check_can_attack():
#     """Checks to make sure if an attacker is able to use a move based on any present status conditions.
#     Calls functions that require a roll for an attack to be successful (like paralysis or confusion)."""
#     if attacker.status == "Paralyzed":
#         if roll_paralyzed(attacker):
#             break

#     if attacker.status == "Asleep" and attack != "Sleep Talk":
#         if roll_sleep(attacker):
#             break

#     if attacker.status == "Frozen":
#         moves_that_can_thaw_out = set(
#             "Burn Up",
#             "Flame Wheel",
#             "Flare Blitz",
#             "Fusion Flare",
#             "Pyro Ball",
#             "Sacred Fire",
#             "Scald",
#             "Scorching Sands",
#             "Steam Eruption",
#         )
#         if attack in moves_that_can_thaw_out:
#             pass
#             # TODO: Create thaw out function.
#         if roll_frozen(attacker):
#             break

#     if "Confusion" in attacker.volatile_statuses:
#         if roll_confusion(attacker):
#             break

#     if "Infatuation" in attacker.volatile_statuses:
#         if roll_infatuation(attacker):
#             break

#     if check_flinched(attacker):
#         break


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
            if player == "p1":
                target = "p2"
            else:
                target = "p1"

            if move_name == "Switch":
                player.switch[n]
            else:
                attack(player.cur_pokemon, move_name, n, target)

        for choice in turn_order:
            player = choice[0]
            if player.check_game_over():
                if player == p1:
                    print("Player 2 Wins!")
                    break
                elif player == p2:
                    print("Player 1 Wins!")
                    break

            if player.cur_pokemon.status[0] == "Fainted":
                player.get_switch()
                player.switch[n]


if __name__ == "__main__":
    main()
