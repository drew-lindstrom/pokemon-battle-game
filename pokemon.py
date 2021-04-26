from game_data import natures_dict, pokemon_dict, moves_dict
from move import Move
import math
import random


class Pokemon:
    def __init__(
        self, name, level, gender, moves, ability, item, IVs, EVs, nature, grounded=True
    ):
        self.name = name
        self.level = level
        self.gender = gender
        self.typing = pokemon_dict[name][0]

        self.moves = [None, None, None, None]

        self.prev_move = None
        self.move_lock = -1

        for n in range(4):
            self.moves[n] = Move(moves[n])

        self.ability = ability
        self.item = item
        self.IVs = IVs
        self.EVs = EVs
        self.nature = nature
        self._hp = None
        self.stat = {
            "max_hp": 0,
            "hp": 0,
            "attack": 0,
            "defense": 0,
            "sp_attack": 0,
            "sp_defense": 0,
            "speed": 0,
        }
        self.init_stat()

        self.stat_mod = {
            "attack": 0,
            "defense": 0,
            "sp_attack": 0,
            "sp_defense": 0,
            "speed": 0,
            "accuracy": 0,
            "evasion": 0,
        }
        # Non-volatile status (Freeze, Poinsoned, Badly Poisoned, Burned, Asleep, Paralyzed).
        # With the exception of Frozen and Asleep, an ability, item, or move is required to remove the status.
        # Statuses are persistent even after switching out. A pokemon can only have one non-volatile status at a time
        # and can not be over written if already afflicted with a different status.
        self.status = [None, 0]
        # Volatile statuses (Leech Seeded, Confused, Flinched, etc.).
        # These statuses clear when the pokemon switches out. Some statuses go away after a set number of turns.
        # A pokemon can have any number of volatile statuses.
        self.v_status = {}
        self.grounded = True

    def init_stat(self):
        """Initializes the hp, max_hp, attack, defense, special attack, special defense, and speed stat for the given pokemon based on the pokemon's
        IVs, EVs, and nature."""

        def stats_formula(n):
            return int(
                (
                    2 * int(pokemon_dict[self.name][1][n])
                    + self.IVs[n]
                    + int(self.EVs[n] / 4)
                )
                * self.level
                / 100
            )

        for stat_name in self.stat:
            if stat_name is "hp" or stat_name is "max_hp":
                n = 0
                self.stat[stat_name] = int(stats_formula(n) + self.level + 10)
            else:
                stat_dictionary = {
                    "attack": 1,
                    "defense": 2,
                    "sp_attack": 3,
                    "sp_defense": 4,
                    "speed": 5,
                }
                n = stat_dictionary[stat_name]
                self.stat[stat_name] = int(
                    (stats_formula(n) + 5) * natures_dict[self.nature][n - 1]
                )

    def update_stat_modifier(self, stat, n):
        """Updates a given stat modifier by n. Stat modifieres can not be greater than 6 or less than -6."""
        self.stat_mod[stat] += n
        if self.stat_mod[stat] > 6:
            self.stat_mod[stat] = 6
        if self.stat_mod[stat] < -6:
            self.stat_mod[stat] = -6

    def reset_stat_modifier(self):
        """Resets all stat modifiers of a given pokemon back to 0.
        Switching a pokemon out always resets stat modifiers. Certian moves also remove all stat modifiers."""
        for stat in self.stat_mod:
            self.stat_mod[stat] = 0

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

    def calc_modified_stat(self, stat_name):
        """Calculates the modified stat of a Pokemomn if any stat modifiers are present.
        Accuracy and evasion are modified at a different scale (n = 3) than the other stats (n = 2). HP and max_hp do not have stat modifiers.
        Accuracy and evasion modifiers are also multipied by 100 while the other stats are multiplied by their respective base stats
        because accuracy/evasion is the chace out of 100% for an attack to hit/for a pokmeon to dodge a hit.
        Ex: A Pokemon with +6 attack modifier would have their attack stat multiplied by 4 (or (2 + 6)/2)."""

        def calc_modified_stat_helper(stat_name, n):

            if stat_name == "accuracy" or stat_name == "evasion":
                modified_stat = 100
            else:
                modified_stat = self.stat[stat_name]

            if self.stat_mod[stat_name] > 0:
                return int(modified_stat * ((n + self.stat_mod[stat_name]) / n))
            elif self.stat_mod[stat_name] < 0:
                return int(modified_stat * (n / (abs(self.stat_mod[stat_name]) + n)))
            else:
                return int(modified_stat)

        if stat_name == "accuracy" or stat_name == "evasion":
            return calc_modified_stat_helper(stat_name, 3)
        return calc_modified_stat_helper(stat_name, 2)

    def heal(self, n):
        """Heal pokemon by n percentage of it's max hp. Won't work on fainted Pokemon. HP won't exceed max hp.
        Ex: Slowbro's HP = 150 -> slowbro.heal(0.5) -> Slowbro's HP = 150 + 50% of max hp"""
        if self.stat["hp"] <= 0:
            print(f"{self.name} has fainted and can't be healed.")
            return
        self.stat["hp"] = min(
            self.stat["hp"] + int(self.stat["max_hp"] * n), self.stat["max_hp"]
        )

    def damage(self, n):
        """Damages pokemon by n percentage of it's max hp. HP won't fall below 0.
        Ex: Slowbro's HP = 150 -> slowbro.damage(0.5) -> Slowbro's HP = 150 - 50% of max hp"""
        self.stat["hp"] = max(0, int(self.stat["hp"] - self.stat["max_hp"] * n))

    def struggle_check(self):
        """Checks the pp of all of the attacking Pokemon's moves. If all moves have zero pp, struggle is used to attack instead."""
        struggle_bool = True
        for n in range(len(self.moves)):
            if self.moves[n].pp > 0:
                struggle_bool = False
        return struggle_bool

    def set_status(self, status_name):
        """Sets the non-volatile status for the Pokemon. Second index of status list is to count number of turns.
        Badly Poisoned deals more damage every turn. Sleep has a greater chance to be cured every turn."""
        if self.status[0] is None:
            self.status = [status_name, 0]

    def cure_status(self):
        """Cures the non-volatile status for the Pokemon."""
        self.status = [None, 0]

    def set_v_status(self, status_name):
        """Sets the volatile status for the Pokemon. First index of the dictionary key is to count number of turns until status is cured."""
        if status_name == "Flinched":
            if status_name not in self.v_status:
                v_status["Flinched"] = [1]

        if status_name == "Confused":
            if status_name not in self.v_status:
                print(f"{self.name} became confused!")
                v_status["Confused"] = [random.randint(2, 5)]

    def decrement_v_status(self):
        """Decrements the counter for all volatile statuses for the Pokemon at the end of the turn. If a counter reaches 0,
        the status is removed."""
        temp = []
        for status in self.v_status:
            self.v_status[status][0] -= 1
            if self.v_status[status][0] <= 0:
                temp.append(status)

        for status in temp:
            del self.v_status[status]

    def reset_v_status(self):
        """Clears the Pokemon's volatile statues when it switches out."""
        self.v_status = {}

    def check_grounded(self):
        """Checks to see if a pokemon is considered grounded at the start of a turn.
        Non grounded pokemon are immune to ground type moves and entry hazards with the exception of stealth rocks."""
        # TODO: Lot of additional conditions for checking grounded.
        if (
            "Flying" in self.typing
            or self.ability == "Levitate"
            or self.item == "Air Balloon"
            or "Magnet Rise" in self.v_status
            or "Telekinesis" in self.v_status
        ):
            if self.item == "Iron Ball" or "Ingrained" in self.v_status:
                self.grounded = True
            else:
                self.grounded = False
        else:
            self.grounded = True