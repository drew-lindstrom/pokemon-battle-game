from game_data import pokemon_dict, moves_dict
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
        self.stat_mods = {'attack': 0, 'defense': 0, 'sp_attack': 0,
                          'sp_defense': 0, 'speed': 0, 'accuracy': 0, 'evasion': 0}

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

    def init_stats(self):
        self.stats['max_hp'] = (int(((int(self.base_stats[0])+self.IVs[0])*2+int(
            math.sqrt(self.level)/4))*self.level)/100)+self.level+10


abomasnow = Pokemon('Abomasnow', 100, 'Male', None,
                    None, None, (31, 31, 31, 31, 31, 31), (255, 0, 0, 0, 0, 0), None)
abomasnow.init_stats()
Pokemon.show_stats(abomasnow)
