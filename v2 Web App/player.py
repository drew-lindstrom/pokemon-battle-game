from pokemon import Pokemon
from switch_effects import *
from game_data import typeKey, typeChart


class Player:
    def __init__(self, pokemon):
        self.team = []
        for n in range(len(pokemon)):
            self.team.append(pokemon[n])
        self.curPokemon = self.team[0]
        self.lightScreen = False
        self.lightScreenCounter = 0
        self.reflect = False
        self.reflectCounter = 0
        self.stealthRocks = False
        self.spikes = 0
        self.tspikes = 0
        self.stickyWeb = False

    def __len__(self):
        return len(self.team)

    def __getitem__(self, index):
        return self.team[index]

    def showTeam(self):
        """Shows stats of the pokemon on the player's team."""
        for n in range(len(self.team)):
            self.team[n].showStats()

    def checkGameOver(self):
        """Checks if there are any pokemon on the player's team who can still fight (HP greater than 0).
        Returns False if all Pokemon on team are fainted."""

        for pokemon in self.team:
            if pokemon.stat["hp"] > 0:
                return False
        return True

    def clearHazards(self):
        """Clears the hazards on the player's side of the field."""
        self.stealthRocks = False
        self.stickyWeb = False
        self.spikes = 0
        self.tspikes = 0