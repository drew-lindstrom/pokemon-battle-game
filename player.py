from pokemon import Pokemon
from switch_effects import *
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
        """Shows stats of the pokemon on the player's team."""
        for n in range(len(self.team)):
            self.team[n].show_stats()

    def check_game_over(self):
        """Checks if there are any pokemon on the player's team who can still fight (HP greater than 0).
        Returns False if all Pokemon on team are fainted."""

        for pokemon in self.team:
            if pokemon.stat["hp"] > 0:
                return False
        return True

    def clear_hazards(self):
        """Clears the hazards on the player's side of the field."""
        # Rapid spin clears all entry hazards.
        self.stealth_rocks = False
        self.sticky_web = False
        self.spikes = 0
        self.tspikes = 0