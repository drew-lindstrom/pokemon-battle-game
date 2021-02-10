from game_data import natures_dict, pokemon_dict, moves_dict
from move import Move
import math


class Pokemon:
    def __init__(
        self, name, level, gender, moves, ability, item, IVs, EVs, nature, grounded=True
    ):
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
        self.hp = None
        self.status = None

    def init_stat(self, n):
        stats_formula = int(
            (
                2 * int(pokemon_dict[self.name][1][n])
                + self.IVs[n]
                + int(self.EVs[n] / 4)
            )
            * self.level
            / 100
        )
        if n == 0:
            stat = int(stats_formula + self.level + 10)
        else:
            stat = int((stats_formula + 5) * natures_dict[self.nature][n - 1])
        return stat

    @property
    def max_hp(self):
        return self.init_stat(0)

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, n):
        if n == None or n > self.max_hp:
            self.hp = self.max_hp
        elif n <= 0:
            self._hp = 0
        else:
            self._hp = n

    @property
    def attack(self):
        return self.init_stat(1)

    @property
    def defense(self):
        return self.init_stat(2)

    @property
    def sp_attack(self):
        return self.init_stat(3)

    @property
    def sp_defense(self):
        return self.init_stat(4)

    @property
    def speed(self):
        return self.init_stat(5)

    @property
    def stat_mods(self):
        return self.stat_mods[0, 0, 0, 0, 0, 0, 0]

    @stat_mods.setter
    def stat_mods(self, index, n):
        self.stat_mods[index] += n
        if self.stat_mods[index] > 6:
            self.stat_mods[index] = 6
        if self.stat_mods[index] < -6:
            self.stat_mods[index] = -6

    def show_stats(self):
        """Prints the stats of the Pokemon with modifiers applied."""  # TODO: Add modifiers
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

    # def calc_stat_boost(self, stat):
    #     stat_index = (('Attack', 0), ('Defense', 1), ('Speci')
    #     if stat == 'Attack':

    def heal(self, n):
        """Heal pokemon by n percentage of it's max hp. Won't work on fainted Pokemon. HP won't exceed max hp.
        Ex: Slowbro's HP = 150 -> slowbro.heal(0.5) -> Slowbro's HP = 150 + 50% of max hp"""
        if self.hp <= 0:
            print(f"{self.name} has fainted and can't be healed.")
            pass
        self.hp = self.hp + int(self.max_hp * n)

    def damage(self, n):
        """Damages pokemon by n percentage of it's max hp. HP won't fall below 0.
        Ex: Slowbro's HP = 150 -> slowbro.damage(0.5) -> Slowbro's HP = 150 - 50% of max hp"""
        self.hp = int(self.hp - self.max_hp * n)

        if self.hp <= 0:
            self.hp = 0

    def struggle_check(self):
        """Checks the pp of all of the attacking Pokemon's moves. If all moves have zero pp, struggle is used to attack instead."""
        struggle_bool = True
        for n in range(len(self.moves)):
            if self.moves[n].pp > 0:
                struggle_bool = False
        return struggle_bool
