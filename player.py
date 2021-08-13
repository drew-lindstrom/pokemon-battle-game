from pokemon import Pokemon
from switch_effects import *
from game_data import typeKey, typeChart
import json


class Player:
    def __init__(self, team, lightScreen=False, lightScreenCounter=0, reflect=False, reflectCounter=0, stealthRocks=False,
                 spikes=0, tspikes=0, stickyWeb=False):
        self.team = []
        for n in range(len(team)):
            self.team.append(team[n])
        self.curPokemon = self.team[0]
        self.lightScreen = lightScreen
        self.lightScreenCounter = lightScreenCounter
        self.reflect = reflect
        self.reflectCounter = reflectCounter
        self.stealthRocks = stealthRocks
        self.spikes = spikes
        self.tspikes = tspikes
        self.stickyWeb = stickyWeb

    def __len__(self):
        return len(self.team)

    def __getitem__(self, index):
        return self.team[index]

    def showTeam(self):
        for n in range(len(self.team)):
            self.team[n].showStats()

    def checkGameOver(self):
        for pokemon in self.team:
            if pokemon.stat["hp"] > 0:
                return False
        return True

    def clearHazards(self):
        self.stealthRocks = False
        self.stickyWeb = False
        self.spikes = 0
        self.tspikes = 0

    @classmethod
    def deserializeAndUpdatePlayerFromJson(cls, data):
        team = list(
            map(Pokemon.deserializeAndUpdatePokemonFromJson, data['team']))
        return cls(team=team, lightScreen=data['lightScreen'], lightScreenCounter=data['lightScreenCounter'],
                   reflect=data['reflect'], reflectCounter=data['reflectCounter'], stealthRocks=data['stealthRocks'],
                   spikes=data['spikes'], tspikes=data['tspikes'], stickyWeb=data['stickyWeb'])
