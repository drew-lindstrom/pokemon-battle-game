from player import Player
from pokemon import Pokemon
from move import Move
from game_data import priority_moves
from stat_calc import calc_speed
from terrain import Terrain
from weather import Weather
import post_attack
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
        self.successful_attack = False


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

    if frame1.switch_choice and frame2.attack:
        return [frame1, frame2]
    elif frame2.switch_choice and frame1.attack:
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
    p1_speed = calc_speed(frame1.user)
    p2_speed = calc_speed(frame2.user)

    if p1_speed > p2_speed:
        return [frame1, frame2]
    # If the speed check is a tie, its usually random who goes first, but for the sake of AI consistency, the opponent will always go first.
    else:
        return [frame2, frame1]


def check_priority(f):
    """Calls priority_moves dictionary to see if the given attack has a priority number, if not returns 0.
    Attacks with a priority higher number will go before the opponent's attack regardless of speed.
    Standard moves have a prioirty of 0. If both pokemon use a move with the same priority, speed is used to determine who goes first."""

    if f.terrain.current_terrain == "Psychic Terrain" and f.target.grounded == True:
        return 0
    if (
        f.terrain.current_terrain == "Grassy Terrain"
        and f.attack.name == "Grassy Glide"
    ):
        return 1

    try:
        return priority_moves[f.attack.name]
    except Exception:
        return 0


def roll_paralysis(user, i=None):
    """Rolls to determine if a paralyzed pokemon can successfully use an attack. 25% that pokemon won't be able to move due to paralysis."""
    if i == None or i < 1 or i > 4:
        i = random.randint(1, 4)

    if i == 1:
        print(f"{user.name} is paralyzed and can't move.")
        return True
    return False


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


def roll_confusion(user, i=None):
    """Rolls to determine if a confused pokemon can successfully use an attack. 33% chance they will hit themselves in confusion."""
    if i == None or i < 1 or i > 2:
        i = random.randint(1, 2)

    if i == 1:
        # TODO: Implement confusion damage.
        print(f"{user.name} hit its self in confusion!")
        return True
    return False


def check_can_attack(f):
    """Checks to make sure if an attacker is able to use a move based on any present status conditions.
    Calls functions that require a roll for an attack to be successful (like paralysis or confusion)."""
    if f.user.status[0] == "Paralyzed":
        if roll_paralyzed(user):
            return False

    if f.user.status[0] == "Asleep" and f.attack_name != "Sleep Talk":
        print(f"{frame.user.name} is asleep.")
        return False

    if f.user.status[0] == "Frozen":
        if roll_frozen(f.user):
            return False

    if "Confusion" in f.user.v_status:
        if roll_confusion(f.user):
            return False

    if "Flinched" in f.user.v_status:
        print(f"{f.user.name} flinched!")
        return False

    if check_immunity(f):
        print(f"It had no effect.")
        return False

    return True


def check_immunity(f):
    """Returns boolean if current attack isn't able to land due to target being immune to the attack's type."""
    if (
        (f.attack.type == "Poison" and "Steel" in f.target.typing)
        or (f.attack.type == "Dragon" and "Fairy" in f.target.typing)
        or (
            (f.attack.type == "Normal" or f.attack.type == "Fighting")
            and "Ghost" in f.target.typing
        )
        or (f.attack.type == "Ghost" and "Normal" in f.target.typing)
        or (f.attack.type == "Electric" and "Ground" in f.target.typing)
        or (f.attack.type == "Psychic" and "Dark" in f.target.typing)
    ):
        return True
    return False


def check_attack_lands(f, i=None):
    """Calculates required accuracy for an attack to land based on the accuracy of the attack,
    accuracy of user, evasion of target, and any additional modifiers. Rolls i in range 0 to 100.
    If i is less than or equal to required accuracy, attack hits and function returns True."""
    additional_modifier = 1

    a = (
        f.attack.accuracy
        * (
            f.user.calc_modified_stat_helper["accuracy"]
            - f.target.calc_modified_stat_helper["evasion"]
        )
        * additional_modifier
    )

    if i is None or i < 0 or i > 100:
        i = random.randint(0, 100)

    if i <= a:
        return True
    print(f"{f.user.name}s attack missed!")
    return False


def apply_post_attack_effects(frame):
    """Applies post attack effects (lowering or raising stats, applying a status, etc) to the user/target of the given frame."""
    post_attack.apply_stat_alt_attack(frame.user, frame.target, frame.attack)
    post_attack.apply_status_inflicting_attack(frame.user, frame.target, frame.attack)
    post_attack.apply_v_status_inflicting_attack(frame.user, frame.target, frame.attack)


def apply_end_of_turn_effects(frame_order):
    """Applies end of turn events (recoil, leftovers healing, etc) to the user of the given frame."""
    for frame in frame_order:
        frame.user.decrement_statuses()
        # TODO: decrement_pp()
        frame.attack.decrement_pp()

    if (
        frame_order[0].weather.current_weather == "Sandstorm"
        or frame_order[0].weather.current_weather == "Hail"
    ):
        for frame in frame_order:
            weather.apply_weather_damage(frame.weather, frame.user)

    if frame_order[0].terrain.current_terrain == "Grassy Terrain":
        for fram in frame_order:
            if frame.user == True:
                terrain.heal_from_grassy_terrain(frame.terrain, frame.user)

    for frame in frame_order:
        if frame.user.item == "Leftovers":
            apply_leftovers(frame.user)

    for frame in frame_order:
        if frame.user.status[0] == "Burned":
            apply_burn(frame.user)

    for frame in frame_order:
        if frame.user.status[0] == "Badly Poisoned":
            apply_bad_poison(frame.user)

    # for frame in frame_order:
    #     apply_recoil(frame.user)


def main():
    """Main function of the program. Takes players' input for attacks, checks for win condition,
    and calls appropriate functions to apply damage and various effects."""
    w = Weather()
    t = Terrain()

    while True:
        ui.print_pokemon_on_field(p1.cur_pokemon, p2.cur_pokemon)
        # TODO: Add in struggle check.
        p1_choice = ui.get_choice(p1)
        p2_choice = ui.get_choice(p2)

        frame_order = get_frame_order(frame1, frame2)

        for cur_frame in frame_order:
            if cur_frame.switch_choice:
                cur_frame.attacking_team.switch(cur_frame.switch_choice)
            else:
                if cur_frame.target.status != "Fainted":
                    if check_can_attack(cur_frame) and check_attack_lands(cur_frame):
                        damage_calc(cur_frame)
                        apply_post_attack_effects(cur_frame)

        apply_end_of_turn_effects(frame_order)

        w.decrement_weather()
        t.decrement_terrain()

        for cur_frame in frame_order:
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
    tapu_lele = Pokemon(
        "Tapu Lele",
        100,
        None,
        ("Psychic", "Moonblast", "Focus Blast", "Psyshock"),
        "Psychic Surge",
        "Choice Specs",
        (31, 0, 31, 31, 31, 31),
        (0, 0, 0, 252, 4, 252),
        "Timid",
    )
    cinderace = Pokemon(
        "Cinderace",
        100,
        "Male",
        ("Pyro Ball", "U-turn", "Gunk Shot", "High Jump Kick"),
        "Libero",
        "Heavy-Duty Boots",
        (31, 31, 31, 31, 31, 31),
        (0, 252, 0, 0, 4, 252),
        "Jolly",
    )
    excadrill = Pokemon(
        "Excadrill",
        100,
        "Male",
        ("Earthquake", "Iron Head", "Swords Dance", "Toxic"),
        "Sand Rush",
        "Leftovers",
        (31, 31, 31, 31, 31, 31),
        (0, 252, 0, 0, 4, 252),
        "Jolly",
    )
    slowbro = Pokemon(
        "Slowbro",
        100,
        "Male",
        ("Teleport", "Slack Off", "Ice Beam", "Psychic"),
        "Regenerator",
        "Heav-Duty Boots",
        (31, 31, 31, 31, 31, 31),
        (248, 0, 252, 8, 0, 0),
        "Relaxed",
    )
    tyranitar = Pokemon(
        "Tyranitar",
        100,
        "Male",
        ("Stealth Rock", "Crunch", "Rock Blast", "Fire Blast"),
        "Sand Stream",
        "Leftovers",
        (31, 31, 31, 31, 31, 31),
        (240, 16, 0, 0, 252, 0),
        "Sassy",
    )
    zapdos = Pokemon(
        "Zapdos",
        100,
        None,
        ("Discharge", "Hurricane", "Roost", "Defog"),
        "Static",
        "Heavy-Duty Boots",
        (31, 31, 31, 31, 31, 31),
        (248, 0, 124, 0, 0, 136),
        "Bold",
    )

    heatran = Pokemon(
        "Heatran",
        100,
        None,
        ("Earth Power", "Eruption", "Fire Blast", "Flash Cannon"),
        "Flash Fire",
        "Choice Specs",
        (31, 0, 31, 31, 31, 31),
        (0, 0, 0, 252, 4, 252),
        "Modest",
    )
    tapu_lele_2 = Pokemon(
        "Tapu Lele",
        100,
        None,
        ("Psychic", "Moonblast", "Focus Blast", "Psyshock"),
        "Psychic Surge",
        "Choice Specs",
        (31, 0, 31, 31, 31, 31),
        (0, 0, 0, 252, 4, 252),
        "Timid",
    )
    urshifu = Pokemon(
        "Urshifu - Rapid Strike Style",
        100,
        None,
        ("Surging Strikes", "Close Combat", "Thunder Punch", "U-turn"),
        "Unseen Fist",
        "Protective Pads",
        (31, 31, 31, 31, 31, 31),
        (0, 252, 0, 0, 4, 252),
        "Jolly",
    )
    hydregion = Pokemon(
        "Hydregion",
        100,
        "Male",
        ("Defog", "Roost", "Dark Pulse", "Earth Power"),
        "Levitate",
        "Leftovers",
        (31, 0, 31, 31, 31, 31),
        (252, 0, 0, 0, 4, 252),
        "Timid",
    )
    landorus = Pokemon(
        "Landorus - Therian Forme",
        100,
        "Male",
        ("Toxic", "Earthquake", "U-turn", "Knock Off"),
        "Intimidate",
        "Heavy-Duty Boots",
        (31, 31, 31, 31, 31, 31),
        (176, 0, 188, 0, 0, 144),
        "Impish",
    )
    rilladoom = Pokemon(
        "Rillaboom",
        100,
        "Male",
        ("Grassy Glide", "Wood Hammer", "Knock Off", "U-turn"),
        "Grassy Surge",
        "Choice Band",
        (31, 31, 31, 31, 31, 31),
        (0, 252, 0, 0, 4, 252),
        "Adamant",
    )

    p1 = Player(tapu_lele, cinderace, excadrill, slowbro, tyranitar, zapdos)
    p2 = Player(heatran, tapu_lele_2, urshifu, hydregion, landorus, rillaboom)
    main()
