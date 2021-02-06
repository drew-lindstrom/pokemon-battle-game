from game_data import moves_dict

from player import set_stealth_rocks

# from terrain import Terrain, terrain
from copy import deepcopy


class Move:
    def __init__(self, name):
        self.name = name
        self.type = moves_dict[name][0]
        self.category = moves_dict[name][1]
        self.pp = None

        # Before attack effect?
        # After attack effect? (applying burn)
        # End of turn effect? (after both players go, like destiny bond or leech seed)

    @property
    def power(self):
        power = moves_dict[self.name][2]
        if power == None:
            return 0
        return int(power)

    @property
    def accuracy(self):
        accuracy = moves_dict[self.name][3]
        if accuracy == None:
            return 0
        return int(accuracy)

    @property
    def max_pp(self):
        max_pp = int(moves_dict[self.name][4])
        if max_pp <= 1:
            return max_pp
        return int(max_pp * 1.6)

    @property
    def pp(self):
        return self._pp

    @pp.setter
    def pp(self, n):
        if n == None or n > self.max_pp:
            self.pp = self.max_pp
        elif n <= 0:
            self._pp = 0
        else:
            self._pp = n

    def show_stats(self):

        print(f"Move: {self.name}")
        print(f"Type: {self.type}")
        print(f"Category: {self.category}")
        print(f"Power: {self.power}")
        print(f"Accuracy: {self.accuracy}")
        print(f"PP: {self.pp}/{self.max_pp}")
        print()

    def check_pp(self):
        """Returns True if a move has enough PP to be used (above 0 PP). Returns False otherwise.
        move.pp (int) -> Boolean
        Ex: move.pp == 0, return False.
        Ex: move.pp == 3, return True."""
        if self.pp <= 0:
            print(f"{self.name} is out of PP!")
            return False
        return True


def defog(attacker, defender):
    terrain.clear_terrain()


def roost(attacker, defender):
    attacker.heal(0.5)
    # TODO: Need to add grounding


def slack_off(attacker, defender):
    attacker.heal(0.5)


def stealth_rock(attacker, defender):
    set_stealth_rocks(defender)


def frost_breath():
    # check for battle armor
    pass


def storm_throw():
    # check for battle armor
    pass


def wicked_blow():
    # check for battle armor
    pass


def surging_strikes():
    # check for battle armor
    pass