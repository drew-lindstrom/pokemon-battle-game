from post_attack import *
from switch_effects import *
from weather import *
from terrain import *
from random import *
import move_effects
from game_data import priority_moves, type_key, type_chart
from stat_calc import calc_speed


def get_frame_order(frame1, frame2):
    """Gets the turn order for the current turn of the game.
    Turn order is determined by the speeds of the current pokemon on the field.
    With the exception of the effects from certian moves, items, or abilities,
    the faster pokemon always switches or attacks before the slower pokemon.
    Switching to a different pokemon always occurs before a pokemon attacks (unless the opposing pokemon uses the move Pursuit)."""
    if frame1.attack_name == "Pursuit" and frame2.switch_choice:
        return [frame1, frame2]
    elif frame2.attack_name == "Pursuit" and frame1.switch_choice:
        return [frame1, frame2]

    if frame1.switch_choice and frame2.attack_name:
        return [frame1, frame2]
    elif frame2.switch_choice and frame1.attack_name:
        return [frame2, frame1]

    priority_p1 = check_priority(frame1)
    priority_p2 = check_priority(frame2)

    if priority_p1 == priority_p2:
        return check_speed(frame1, frame2)
    elif priority_p1 > priority_p2:
        return [frame1, frame2]
    else:
        return [frame2, frame1]


def check_speed(frame1, frame2):
    """Checks the speed of both pokemon on field to determine who moves first.
    Takes into account things like Choice Scarf, abilities that effect priority or speed, priority moves, paraylsis, etc."""
    p1_speed = calc_speed(frame1)
    p2_speed = calc_speed(frame2)

    if p1_speed > p2_speed:
        return [frame1, frame2]
    # If the speed check is a tie, its usually random who goes first, but for the sake of AI consistency, the opponent will always go first.
    else:
        return [frame2, frame1]


def check_priority(frame):
    """Calls priority_moves dictionary to see if the given attack has a priority number, if not returns 0.
    Attacks with a priority higher number will go before the opponent's attack regardless of speed.
    Standard moves have a prioirty of 0. If both pokemon use a move with the same priority, speed is used to determine who goes first."""

    if (
        frame.terrain.current_terrain == "Psychic Terrain"
        and frame.target.grounded == True
    ):
        return 0
    if (
        frame.terrain.current_terrain == "Grassy Terrain"
        and frame.attack_name == "Grassy Glide"
    ):
        return 1

    try:
        return priority_moves[frame.attack_name]
    except Exception:
        return 0


def roll_paralysis(user, i=None):
    """Rolls to determine if a paralyzed pokemon can successfully use an attack. 25% that pokemon won't be able to move due to paralysis."""
    if i == None or i < 1 or i > 4:
        i = randint(1, 4)

    if i == 1:
        print(f"{user.name} is paralyzed and can't move.")
        return False
    return True


def roll_frozen(user, i=None):
    """Rolls to determine if a frozen pokemon thaws out during it's attack. Frozen pokemon are not able to attack. 20% chance to thaw out.
    The pokemon can use it's attack on the turn that it thaws out."""
    if i == None or i < 1 or i > 5:
        i = randint(1, 5)

    if i == 1:
        print(f"{user.name} thawed out!")
        user.cure_status()
        return True
    print(f"{user.name} is frozen and cant attack!")
    print()
    return False


def roll_confusion(user, i=None):
    """Rolls to determine if a confused pokemon can successfully use an attack. 33% chance they will hit themselves in confusion."""
    if i == None or i < 1 or i > 2:
        i = randint(1, 2)

    if i == 1:
        # TODO: Implement confusion damage.
        print(f"{user.name} hit its self in confusion!")
        return False
    return True


def check_immunity(frame):
    """Returns boolean if current attack isn't able to land due to target being immune to the attack's type."""
    if (
        (frame.attack.type == "Poison" and "Steel" in frame.target.typing)
        or (frame.attack.type == "Dragon" and "Fairy" in frame.target.typing)
        or (
            (frame.attack.type == "Normal" or frame.attack.type == "Fighting")
            and "Ghost" in frame.target.typing
        )
        or (frame.attack.type == "Ghost" and "Normal" in frame.target.typing)
        or (frame.attack.type == "Electric" and "Ground" in frame.target.typing)
        or (frame.attack.type == "Psychic" and "Dark" in frame.target.typing)
    ):
        return False
    return True


def check_can_attack(frame, i=None):
    """Checks to make sure if an attacker is able to use a move based on any present status conditions.
    Calls functions that require a roll for an attack to be successful (like paralysis or confusion)."""
    if frame.user.status[0] == "Paralyzed":
        if not roll_paralysis(frame.user, i):
            return False

    if frame.user.status[0] == "Asleep" and frame.attack_name != "Sleep Talk":
        print(f"{frame.user.name} is asleep.")
        print()
        return False

    if frame.user.status[0] == "Frozen":
        if not roll_frozen(frame.user, i):
            return False

    if "Confusion" in frame.user.v_status:
        if not roll_confusion(frame.user, i):
            return False

    if "Flinched" in frame.user.v_status:
        print(f"{frame.user.name} flinched!")
        print()
        return False

    if not check_immunity(frame):
        print(f"It had no effect.")
        print()
        return False

    return True


def check_attack_lands(frame, i=None):
    """Calculates required accuracy for an attack to land based on the accuracy of the attack,
    accuracy of user, evasion of target, and any additional modifiers. Rolls i in range 0 to 100.
    If i is less than or equal to required accuracy, attack hits and function returns True."""
    if frame.attack.accuracy == 0:
        frame.attack_lands = True
        return

    additional_modifier = 1

    accuracy_evasion_stat = frame.user.calc_modified_stat(
        "accuracy"
    ) - frame.target.calc_modified_stat("evasion")

    if accuracy_evasion_stat < -6:
        accuracy_evasion_stat = -6

    if accuracy_evasion_stat < 0:
        accuracy_evasion_stat = 3 / (3 + accuracy_evasion_stat * -1)
    elif accuracy_evasion_stat > 0:
        accuracy_evasion_stat = (3 + accuracy_evasion_stat) / 3
    else:
        accuracy_evasion_stat = 1

    a = frame.attack.accuracy * accuracy_evasion_stat * additional_modifier

    if i is None or i < 0 or i > 100:
        i = randint(0, 100)

    if i <= a:
        frame.attack_lands = True
        return

    print(f"{frame.user.name}s attack missed!")

    # If high jump kick misses, it damages the user.
    if frame.attack_name == "High Jump Kick":
        print(f"{frame.user.name} came crashing down...")
        frame.user.apply_damage_percentage(0.5)


def apply_non_damaging_move(frame):
    """Applies effect of current non damaging move being used."""
    if frame.attack_name == "Stealth Rocks":
        move_effects.set_stealth_rocks(frame)

    if frame.attack_name == "Defog":
        move_effects.activate_defog(frame)


def switch(frame):
    """Switch current pokemon with another pokemon on player's team. Won't work if player's choice to switch into is already fainted.
    Ex: Player team order is [Tyranitar, Slowbro] -> player_team.switch(1) -> Player team order is [Slowbro, Tyranitar]"""
    n = int(frame.switch_choice)
    if frame.attacking_team.team[n].stat["hp"] == 0:
        print(f"{frame.attacking_team.team[n].name} has already fainted!")
    else:
        # try:
        frame.attacking_team.team[0], frame.attacking_team.team[n] = (
            frame.attacking_team.team[n],
            frame.attacking_team.team[0],
        )
        apply_switch_effect(frame, n, "Out")
        apply_switch_effect(frame, 0, "In")
        frame.user = frame.attacking_team[0]
        frame.attacking_team.cur_pokemon = frame.attacking_team.team[0]
        apply_entry_hazards(frame)
        frame.attacking_team.team[n].reset_previous_move()
        frame.attacking_team.team[n].reset_stat_modifier()
        frame.attacking_team.team[n].reset_statuses()
        print(
            f"{frame.attacking_team.team[n].name} switched with {frame.attacking_team.team[0].name}."
        )
        print()
        # except Exception:
        #     print(f"Can't switch out {frame.attacking_team.cur_pokemon.name}...")
    # Grounded Poision type pokemon remove toxic spikes when switched in even if wearing heavy duty boots.


def apply_switch_effect(frame, n, switch_dir):
    """Applies switch effect for current pokemon that's switched in or switched out."""
    user = frame.attacking_team[n]
    if switch_dir == "In":
        if user.ability == "Grassy Surge":
            activate_grassy_surge(user, frame.terrain)

        if user.ability == "Intimidate":
            activate_intimidate(user, frame.target)

        if user.ability == "Psychic Surge":
            activate_psychic_surge(user, frame.terrain)

        if user.ability == "Sand Stream":
            activate_sand_stream(user, frame.weather)

    if switch_dir == "Out":
        if user.ability == "Regenerator":
            activate_regenerator(user)


def apply_entry_hazards(frame):
    """Applies the appropriate entry hazards effects after a pokemon switches in.
    Calls funciton to clear toxic spikes if target if a grounded poison type."""
    if (
        frame.user.item != "Heavy Duty Boots"
        and frame.attacking_team.stealth_rocks == True
    ):
        apply_stealth_rocks_damage(frame)
    else:
        pass
        # if player.current_pokemon.grounded == True:
        # apply_spikes_damage(player.current_pokemon)
        # tspikes_clear_check(player.current_pokemon)
        # apply_tspikes_effect(player.current_pokemon)
        # apply_sticky_web_effect(player.current_pokemon)


def apply_stealth_rocks_damage(frame):
    """Applies stealth rock damage to the target depending on target's weakness to Rock."""
    atk_id = type_key.get("Rock")
    def1_id = type_key.get(frame.user.typing[0])
    mult_1 = type_chart[atk_id][def1_id]
    try:
        def2_id = type_key.get(frame.user.typing[1])
        mult_2 = type_chart[atk_id][def2_id]
    except:
        mult_2 = 1

    frame.user.apply_damage_percentage(0.125 * mult_1 * mult_2)
    print(f"Pointed stones dug into {frame.user.name}!")
    print()


def apply_post_attack_effects(frame):
    """Applies post attack effects (lowering or raising stats, applying a status, etc) to the user/target of the given frame."""
    apply_stat_alt_attack(frame.user, frame.target, frame.attack.name)
    apply_status_inflicting_attack(frame.user, frame.target, frame.attack.name)
    apply_v_status_inflicting_attack(frame.user, frame.target, frame.attack.name)


def apply_end_of_turn_effects(frame_order):
    """Applies end of turn events (recoil, leftovers healing, etc) to the user of the given frame."""
    for frame in frame_order:
        frame.user.decrement_statuses()
        if frame.attack.name:
            frame.attack.decrement_pp()

    if (
        frame_order[0].weather.current_weather == "Sandstorm"
        or frame_order[0].weather.current_weather == "Hail"
    ):
        for frame in frame_order:
            apply_weather_damage(frame.weather, frame.user)

    if frame_order[0].terrain.current_terrain == "Grassy Terrain":
        for frame in frame_order:
            heal_from_grassy_terrain(frame.terrain, frame.user)

    for frame in frame_order:
        if frame.user.item == "Leftovers":
            apply_leftovers(frame.user)

    for frame in frame_order:
        if frame.user.status[0] == "Burned":
            apply_burn(frame.user)

    for frame in frame_order:
        if (
            frame.user.status[0] == "Badly Poisoned"
            or frame.user.status[0] == "Poisoned"
        ):
            apply_poison(frame.user)

    for frame in frame_order:
        if frame.attack_name == "Wood Hammer":
            apply_recoil(frame.user, frame.attack_damage, 0.33)
