from player import Player
from pokemon import Pokemon
from move import Move
from game_data import priority_moves
from stat_calc import calc_speed
import ui
import random


class Frame:
    """Frame class is used to specify the parameters for a player's "action" during a turn. Each turn consists of two frames, one frame is
    for player 1 with their chosen attack or, if switching, what pokemon on their team they'd like to switch into
    The other frame is for player 2 with the same parameters.
    Frame is used to simplfy passing data into various methods since all methods require some combination of the given inputs.
    For example, when calculating damage, the attacking pokemon's stats, defending pokemon's stats, and move data is taken into account.
    However, if there's a sandstorm, a rock type pokemon receives a special defense boost. In additional, if the defending team has
    light screens up, the defending pokemon also receives a speical defense boost."""

    def __init__(
        self,
        attacking_team=None,
        defending_team=None,
        attack=None,
        switch_choice=None,
        weather=None,
        terrain=None,
    ):
        self.attacking_team = attacking_team
        self.user = attacking_team.cur_pokemon
        self.defending_team = defending_team
        self.target = defending_team.cur_pokemon
        self.attack = self.user.moves[n]
        self.attack_name = self.attack.name
        self.switch_choice = switch_choice
        self.weather = weather
        self.terrain = terrain


def get_turn_order(frame1, frame2):
    """Gets the turn order for the current turn of the game.
    Turn order is determined by the speeds of the current pokemon on the field.
    With the exception of the effects from certian moves, items, or abilities,
    the faster pokemon always switches or attacks before the slower pokemon.
    Switching to a different pokemon always occurs before a pokemon attacks (unless the opposing pokemon uses the move Pursuit)."""
    if frame1.attack_name == "Pursuit" and frame2.switch_choice:
        return [frame1, frame2]
    elif frame2.attack_name == "Pursuit" and frame1.switch_choice:
        return [frame1, frame2]

    if frame1.switch_choice and frame2.attack:
        return [frame1, frame2]
    elif frame2.switch_choice and frame1.attack:
        return [frame2, frame1]

    priority_p1 = check_priority(frame1.attack_name, frame1.terrain)
    priority_p2 = check_priority(frame2.attack_name, frame2.terrain)

    if priority_p1 == priority_p2:
        return check_speed(frame1, frame2)
    elif priority_p1 > priority_p2:
        return [frame1, frame2]
    else:
        return [frame2, frame1]


def check_speed(frame1, frame2):
    """Checks the speed of both pokemon on field to determine who moves first.
    Takes into account things like Choice Scarf, abilities that effect priority or speed, priority moves, paraylsis, etc."""
    p1_speed = calc_speed(frame1.user)
    p2_speed = calc_speed(frame2.user)

    if p1_speed > p2_speed:
        return [frame1, frame2]
    # If the speed check is a tie, its usually random who goes first, but for the sake of AI consistency, the opponent will always go first.
    else:
        return [frame2, frame1]


def check_priority(attack_name, terrain):
    """Calls priority_moves dictionary to see if the given attack has a priority number, if not returns 0.
    Attacks with a priority higher number will go before the opponent's attack regardless of speed.
    Standard moves have a prioirty of 0. If both pokemon use a move with the same priority, speed is used to determine who goes first."""
    try:
        return priority_moves[attack_name]
    except Exception:
        if attack_name == "Grassy Glide" and terrain.current_terrain == "Grassy Terrain":
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

#     if check_flinched(attacker):
#         break

def check_attack_lands():

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
