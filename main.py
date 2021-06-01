from player import Player
from pokemon import Pokemon
from move import Move

from terrain import Terrain
from weather import Weather
from damage_calc import *
from move_effects import *
from post_attack import *
from switch_effects import *
from util import *
import ui


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
        self.attack_name = None
        if attack:
            self.attack = self.user.moves[n]
            self.attack_name = self.attack.name
        if switch_choice:
            self.switch_choice = switch_choice
        else:
            self.switch_choice = False
        self.weather = weather
        self.terrain = terrain
        self.can_attack = False
        self.attack_lands = False

    def update_cur_pokemon(self):
        "Whenever a switch occurs, updates the frames to switch the user/target to the current pokemon on the respective teams."
        self.user = self.attacking_team.cur_pokemon
        self.target = self.defending_team.cur_pokemon


def main():
    """Main function of the program. Takes players' input for attacks, checks for win condition,
    and calls appropriate functions to apply damage and various effects."""
    w = Weather()
    t = Terrain()

    #'Switches' leading pokemon with their respective selves in order to activate any abilities that activate on switch in.
    opening_frame_1 = Frame(p1, p2, None, None, w, t)
    opening_frame_1.switch_choice = 0
    opening_frame_2 = Frame(p2, p1, None, None, w, t)
    opening_frame_2.switch_choice = 0
    switch(opening_frame_1)
    switch(opening_frame_2)

    while True:
        frame1 = Frame(p1, p2, None, None, w, t)
        frame2 = Frame(p2, p1, None, None, w, t)
        ui.print_pokemon_on_field(frame1.user, frame2.user)

        # Gets input on what each player wants to do before the given turn.
        frame1 = ui.get_choice(frame1)
        frame2 = ui.get_choice(frame2)

        # Determines which player goes first for the turn (based on speed, priority moves, etc.)
        frame_order = get_frame_order(frame1, frame2)

        for cur_frame in frame_order:
            if cur_frame.switch_choice:
                switch(cur_frame)
                frame1.update_cur_pokemon()
                frame2.update_cur_pokemon()
            else:
                if cur_frame.user.status != "Fainted":
                    cur_frame.can_attack = check_can_attack(cur_frame)
                    check_attack_lands(cur_frame)
                    if cur_frame.can_attack and cur_frame.attack_lands:
                        if (
                            cur_frame.attack.category == "Pysical"
                            or cur_frame.attack.category == "Special"
                        ):
                            cur_frame.target.apply_damage(calc_damage(cur_frame))
                            apply_post_attack_effects(cur_frame)
                        else:
                            apply_non_damaging_move(cur_frame)

        apply_end_of_turn_effects(frame_order)

        w.decrement_weather()
        t.decrement_terrain()

        for cur_frame in frame_order:
            player = cur_frame.attacking_team
            # Game over check
            if player.check_game_over():
                if player == p1:
                    print("Player 2 Wins!")
                    break
                elif player == p2:
                    print("Player 1 Wins!")
                    break
            # Prompts player to switch any fainted pokemon at end of turn.
            if player.cur_pokemon.status[0] == "Fainted":
                player.switch(ui.get_switch(cur_frame).switch_choice)


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
        "Heavy Duty Boots",
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
        "Heav Duty Boots",
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
        "Heavy Duty Boots",
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
    hydreigon = Pokemon(
        "Hydreigon",
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
        "Heavy Duty Boots",
        (31, 31, 31, 31, 31, 31),
        (176, 0, 188, 0, 0, 144),
        "Impish",
    )
    rillaboom = Pokemon(
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

    p1 = Player([tapu_lele, cinderace, excadrill, slowbro, tyranitar, zapdos])
    p2 = Player([heatran, tapu_lele_2, urshifu, hydreigon, landorus, rillaboom])
    main()
