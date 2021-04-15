from pokemon import Pokemon
from game_data import type_key, type_chart


class Player:
    def __init__(self, pokemon):
        self.team = []
        for n in range(len(pokemon)):
            self.team.append(pokemon[n])
        self.cur_pokemon = self.team[0]
        self.light_screen = False
        self.light_screen_counter = 0
        self.reflect = False
        self.reflect_counter = 0
        self.stealth_rocks = False
        self.spikes = 0
        self.tspikes = 0
        self.sticky_web = False

    def __len__(self):
        return len(self.team)

    def __getitem__(self, index):
        return self.team[index]

    def show_team(self):
        for n in range(len(self.team)):
            self.team[n].show_stats()

    def switch(self, n):
        """Switch current pokemon with another pokemon on player's team. Won't work if player's choice to switch into is already fainted.
        Ex: Player team order is [Tyranitar, Slowbro] -> player_team.switch(1) -> Player team order is [Slowbro, Tyranitar]"""
        n = int(n)
        if self.team[n].stat["hp"] == 0:
            print(f"{self.team[n].name} has already fainted!")
        else:
            try:
                self.team[0], self.team[n] = (
                    self.team[n],
                    self.team[0],
                )
                print(f"{self.cur_pokemon.name} switched with {self.team[n].name}.")
                self.cur_pokemon = self.team[0]
                print()
                # apply_entry_hazards(self.current_pokemon)
                self.team[n].move_lock = -1
                self.team[n].prev_move = None
            except Exception:
                print(f"Can't switch out {self.cur_pokemon.name}...")
        # Grounded Poision type pokemon remove toxic spikes when switched in even if wearing heavy duty boots.

    def game_over_check(self):
        """Checks if there are any pokemon on the player's team who can still fight (HP greater than 0).
        Returns False if all Pokemon on team are fainted."""

        for pokemon in self.team:
            if pokemon.stat["hp"] > 0:
                return False
        return True


def apply_entry_hazards(target):
    """Applies the appropriate entry hazards effects after a pokemon switches in.
    Calls funciton to clear toxic spikes if target if a grounded poison type."""
    if target.item != "Heavy Duty Boots":
        apply_stealth_rocks_damage(target)
    else:
        print("error")
        # if player.current_pokemon.grounded == True:
        # apply_spikes_damage(player.current_pokemon)
        # tspikes_clear_check(player.current_pokemon)
        # apply_tspikes_effect(player.current_pokemon)
        # apply_sticky_web_effect(player.current_pokemon)


def apply_stealth_rocks_damage(target):
    """Applies stealth rock damage to the target depending on target's weakness to Rock."""
    atk_id = type_key.get("Rock")
    def1_id = type_key.get(target.typing[0])
    mult_1 = type_chart[atk_id][def1_id]
    try:
        def2_id = type_key.get(target.typing[1])
        mult_2 = type_chart[atk_id][def2_id]
    except:
        mult_2 = 1

    target.damage(0.125 * mult_1 * mult_2)


def clear_hazards(player):
    """Clears the hazards on the player's side of the field."""
    # Rapid spin clears all entry hazards.
    player.stealth_rocks = False
    player.sticky_web = False
    player.spikes = 0
    player.tspikes = 0