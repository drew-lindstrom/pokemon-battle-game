from game_data import moves_dict


class Move():
    def __init__(self, name):
        self.name = name
        self.type = moves_dict[name][0]
        self.category = moves_dict[name][1]
        self.power = moves_dict[name][2]
        self.accuracy = moves_dict[name][3]
        self.pp = moves_dict[name][4]
        self.max_pp = self.pp

    def show_stats(self):

        print(f'Move: {self.name}')
        print(f'Type: {self.type}')
        print(f'Category: {self.category}')
        print(f'Power: {self.power}')
        print(f'Accuracy: {self.accuracy}')
        print(f'PP: {self.pp}/{self.max_pp}')
        print()
