import random
from game_data import move_dict, type_key, type_chart

class Pokemon():
    def __init__(self, name, type1, type2, level, max_hp, attack, defense, sp_attack, sp_defense, speed, 
                    move1=None, move2=None, move3=None, move4=None):
        self.name = name
        self.typing = {'type1' : type1, 'type2' : type2} 
        self.level = level
        self.stats = {'current_hp' : max_hp, 'max_hp' : max_hp, 'attack' : attack, 'defense' : defense, 'sp_attack' : sp_attack,
                        'sp_defense' : sp_defense, 'speed' : speed}
        self.stat_modifiers = {'attack' : 0, 'defense' : 0, 'sp_attack' : 0, 'sp_defense' : 0, 'speed' : 0, 'accuracy' : 0, 'evasion' : 0} 
        self.status = None
        self.moves = [{'name' : move1, 'type' : '', 'category' : '', 'power' : 0, 'accuracy' : 0, 'current_pp' : 0, 'max_pp' : 0},
                        {'name' : move2, 'type' : '', 'category' : '', 'power' : 0, 'accuracy' : 0, 'current_pp' : 0, 'max_pp' : 0},
                        {'name' : move3, 'type' : '', 'category' : '', 'power' : 0, 'accuracy' : 0, 'current_pp' : 0, 'max_pp' : 0}, 
                        {'name' : move4, 'type' : '', 'category' : '', 'power' : 0, 'accuracy' : 0, 'current_pp' : 0, 'max_pp' : 0}]
        self.init_moves()

    def show_stats(self):
        """Prints the stats of the Pokemon with modifiers applied.""" # TO DO: Add modifiers
        print('Pokemon: ', self.name)
        if self.typing['type2'] != None:
            print(f'Type: {self.typing["type1"]}/{self.typing["type2"]}')
        else:
            print(f'Type: {self.typing["type1"]}')
        print(f'Level: {self.level}')
        print(f'HP: {self.stats["current_hp"]}/{self.stats["max_hp"]}')
        print(f'Attack: {self.stats["attack"]}')
        print(f'Defense: {self.stats["defense"]}')
        print(f'Special Attack: {self.stats["sp_attack"]}')
        print(f'Special Defense: {self.stats["sp_defense"]}')
        print(f'Speed: {self.stats["speed"]}')
        print()

    def show_moves(self):
        """Prints move information."""
        for n in range(0, 4):
            if self.moves[n]['name'] != None:
                print(f'Name: {self.moves[n]["name"]}')
                print(f'Type: {self.moves[n]["type"]}')
                print(f'Category: {self.moves[n]["category"]}')
                print(f'Power: {self.moves[n]["power"]}')
                print(f'Accuracy: {self.moves[n]["accuracy"]}')
                print(f'PP: {self.moves[n]["current_pp"]}/{self.moves[n]["max_pp"]}')
                print()

    def init_moves(self):
        """Adds move data from a dictionary to each of the Pokemon\'s moves"""

        for move_num in range(0, 4):
            try:
                current_move = self.moves[move_num]
                move_name = self.moves[move_num]['name']
                current_move['type'] = move_dict[move_name][0]
                current_move['category'] = move_dict[move_name][1]
                current_move['power'] = move_dict[move_name][2]
                current_move['accuracy'] = move_dict[move_name][3]
                current_move['current_pp'] = move_dict[move_name][4]
                current_move['max_pp'] = move_dict[move_name][4]

            except Exception:
                # If current move name is not in dictionary, that move is set to None and is no longer displayed.
                self.moves[move_num]['name'] = None

def next_turn(pokemon_1, action_1, pokemon_2, action_2):
    pass

def priority_check():
    """Checks to see which Pokemon attacks first. Checks both Pokemon's speed stat as well as if priority moves are being used."""
    pass

def crit_check():
    """Rolls to determine if a move lands a critical hit. Critical hits boost damage by 1.5 ignore the attacker's negative stat stages, 
    the defender's positive stat stages, and Light Screen/Reflect/Auorar Veil. Burn is not ignored."""
    # TO DO: add special moves/itesms/abilities.
    crit = random.randint(1, 24)
    if crit == 1:
        return 1.5
    else:
        return 1

def accuracy_check(attacker, move, defender):
    """Rolls to determine if a move lands or misses."""
    num = 3
    den = 3
    modifier = attacker.stat_modifiers['accuracy'] - defender.stat_modifiers['evasion']

    if modifier > 6:
        modifier = 6
    elif modifier < -6:
        modifier = -6
    if modifier > 0:
        num = num + modifier
    elif modifier < 0:
        den = den + (modifier * -1)

    accuracy = attacker.moves[move]['accuracy'] * (num / den)
    check = random.randint(1, 100)
    if check <= accuracy:
        return True
    else:
        return False

def weather_check():
    pass

def stab_check(attacker, move):
    """Checks to see if the attacking move is the same type as the attacker. If so, attack power is boosted by 50%."""
    if (attacker.typing['type1'] or attacker.typing['type2']) == attacker.moves[move]['type']:
        return 1.5
    else:
        return 1

def type_effectiveness_check(attacker, move, defender):
    """Return the damage multiplier for how super effective the move is. type_chart is a matrix showing how each type matches up between each
    other. X-axis is the defending type, y-axis is the attacking type. Top left corner is (0, 0). Each type corresponds to a number on the 
    x and y axis."""


    atk_id = type_key.get(attacker.moves[move]['type'])
    def1_id = type_key.get(defender.typing['type1'])
    mult_1 = type_chart[atk_id][def1_id]
    try:
        def2_id = type_key.get(defender.typing['type2'])
        mult_2 = type_chart[atk_id][def2_id]
    except:
        mult_2 = 1

    return mult_1 * mult_2

def burn_check(attacker, move):
    """Checks to see if the attacker is currently burned. If so and the attack is physical, damage is reduced by 50%."""
    if attacker.status == 'Burn' and attacker.moves[move]['category'] == 'Physical':
        return 0.5
    else:
        return 1

def sleep_check():
    pass

def frozen_check():
    pass

def pp_check():
    pass

def random()
    pass

def attack(attacker, move, defender):
    """Determines if a move hits and how much damage is dealt."""
#  TO DO: Critical hit ignore thes attacker's negative stat stages, the defender's positive stat stages, and Light Screen/Reflect/Auorar Veil.
    
    print(f'{attacker.name} used {attacker.moves[move]["name"]}!')

    if accuracy_check(attacker, move, defender) == True:
        crit = crit_check()
        stab = stab_check(attacker, move)
        typ = type_effectiveness_check(attacker, move, defender)
        burn = burn_check(attacker, move)

        if attacker.moves[move]['category'] == 'Physical':
            attack_stat = attacker.stats['attack']
            defense_stat = defender.stats['defense']
        elif attacker.moves[move]['category'] == 'Special':
            attack_stat = attacker.stats['sp_attack']
            defense_stat = defender.stats['sp_defense']

        damage = (((((2 * attacker.level / 5) + 2) * attacker.moves[move]['power'] * (attack_stat/defense_stat)) / 50) + 2) * crit * stab * typ * burn

        defender.stats['current_hp'] -= damage

        if typ > 1:
            print('It\'s super effective!')
        elif typ < 1 and typ > 0:
            print('It\'s not very effective...')
        # TO DO: Type immunity text.

    else:
        if attacker.name.endswith('s') == True:
            print(f'{attacker.name}\' attack missed!')
        else:
            print(f'{attacker.name}\'s attack missed!')

    attacker.moves[move]['current_pp'] -= 1

    print(f'{defender.name}\'s HP: {defender.stats["current_hp"]}/{defender.stats["max_hp"]}')
    print(f'{attacker.name}\'s PP for {attacker.moves[move]["name"]}: {attacker.moves[move]["current_pp"]}/{attacker.moves[move]["max_pp"]}')
    print()

garchomp = Pokemon('Garchomp', 'Dragon', 'Ground', 100, 108, 130, 95, 80, 85, 102, 'Earthquake', 'Dragon Claw', 'Fire Fang', 'Swords Dance')
mamoswine = Pokemon('Mamoswine', 'Ground', 'Ice', 100, 110, 130, 80, 70, 60, 80, 'Ice Shard', 'Earthquake', 'Icicle Crash', 'Knock Off')
attack(mamoswine, 2, garchomp)