from game_data import natures_dict, pokemon_dict, moves_dict
import math


class Pokemon():
    def __init__(self, name, level, gender, moves, ability, item, IVs, EVs, nature):
        self.name = name
        self.level = level
        self.gender = gender
        self.typing = pokemon_dict[name][0]
        self.nature = nature
        self.ability = ability
        self.item = item
        self.IVs = IVs
        self.EVs = EVs
        self.base_stats = pokemon_dict[name][1]
        self.stats = {'current_hp': 0, 'max_hp': 0, 'attack': 0, 'defense': 0, 'sp_attack': 0,
                      'sp_defense': 0, 'speed': 0}
        self.stat_mods = [1, 1, 1, 1, 1, 1, 1]
        self.status = None
        # HP stat calculation is wrong for some reason.
        self.stats['max_hp'] = int(((2*int(self.base_stats[0])+self.IVs[0]+int(
            self.EVs[0]/4))*self.level)/100)+self.level+10
        self.stats['current_hp'] = self.stats['max_hp']

        stats_list = [0, 0, 0, 0, 0]
        for n in range(5):
            stats_list[n] = int((int(((2*int(self.base_stats[n+1])+self.IVs[n+1]+int(
                self.EVs[n+1]/4))*self.level)/100)+5)*natures_dict[self.nature][n])

        self.stats["attack"] = stats_list[0]
        self.stats["defense"] = stats_list[1]
        self.stats["sp_attack"] = stats_list[2]
        self.stats["sp_defense"] = stats_list[3]
        self.stats["speed"] = stats_list[4]

    def show_stats(self):
        """Prints the stats of the Pokemon with modifiers applied."""  # TO DO: Add modifiers
        print('Pokemon: ', self.name)
        print(f'Type: {self.typing}')
        print(f'Level: {self.level}')
        print(f'Gender: {self.gender}')
        print(f'HP: {self.stats["current_hp"]}/{self.stats["max_hp"]}')
        print(f'Attack: {self.stats["attack"]}')
        print(f'Defense: {self.stats["defense"]}')
        print(f'Special Attack: {self.stats["sp_attack"]}')
        print(f'Special Defense: {self.stats["sp_defense"]}')
        print(f'Speed: {self.stats["speed"]}')
        print()


abomasnow = Pokemon('Abomasnow', 100, 'Male', None,
                    None, None, (31, 31, 31, 31, 31, 31), (252, 0, 0, 0, 0, 0), 'Adamant')
Pokemon.show_stats(abomasnow)
