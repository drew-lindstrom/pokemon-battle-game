from game_data import natures_dict, pokemon_dict, moves_dict
from move import Move
import math
import pytest


class Pokemon:
    def __init__(self, name, level, gender, moves, ability, item, IVs, EVs, nature):
        self.name = name
        self.level = level
        self.gender = gender
        self.typing = pokemon_dict[name][0]
        self.moves = [None, None, None, None]
        for n in range(4):
            self.moves[n] = Move(moves[n])
        self.ability = ability
        self.item = item
        self.IVs = IVs
        self.EVs = EVs
        self.nature = nature
        self.base_stats = pokemon_dict[name][1]
        # attack, defense, sp attack, sp defense, speed, accuracy, evasion
        # need to update to use 1s instead
        self.stat_mods = [0, 0, 0, 0, 0, 0, 0]
        self.status = None
        self.max_hp = self.init_stat(0)
        self.hp = self.max_hp
        self.attack = self.init_stat(1)
        self.defense = self.init_stat(2)
        self.sp_attack = self.init_stat(3)
        self.sp_defense = self.init_stat(4)
        self.speed = self.init_stat(5)

    def init_stat(self, n):
        stats_formula = int(
            (2 * int(self.base_stats[n]) + self.IVs[n] + int(self.EVs[n] / 4))
            * self.level
            / 100
        )
        if n == 0:
            stat = int(stats_formula + self.level + 10)
        else:
            stat = int((stats_formula + 5) * natures_dict[self.nature][n - 1])
        return stat

    def show_stats(self):
        """Prints the stats of the Pokemon with modifiers applied."""  # TO DO: Add modifiers
        print(f"Pokemon: {self.name}")
        print(f"Type: {self.typing}")
        print(f"Level: {self.level}")
        print(f"Gender: {self.gender}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Special Attack: {self.sp_attack}")
        print(f"Special Defense: {self.sp_defense}")
        print(f"Speed: {self.speed}")
        print()

        for n in range(4):
            Move.show_stats(self.moves[n])

    def update_stats(self):
        pass
