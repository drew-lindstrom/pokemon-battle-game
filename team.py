from pokemon import Pokemon


class Team:
    def __init__(self, pokemon):
        self.team_list = []
        for n in range(len(pokemon)):
            self.team_list.append(pokemon[n])
        self.current_pokemon = self.team_list[0]

    def __len__(self):
        return len(self.team_list)

    def __getitem__(self, index):
        return self.team_list[index]

    def show_team(self):
        for n in range(len(self.team_list)):
            self.team_list[n].show_stats()

    def switch(self, n):
        """Switch current pokemon with another pokemon on player's team. Won't work if player's choice to switch into is already fainted.
        Ex: Player team order is [Tyranitar, Slowbro] -> player_team.switch(1) -> Player team order is [Slowbro, Tyranitar]"""
        n = int(n)
        if self.team_list[n].hp == 0:
            print(f"{self.team_list[n].name} has already fainted!")
        else:
            try:
                self.current_pokemon, self.team_list[n] = (
                    self.team_list[n],
                    self.current_pokemon,
                )
                print(
                    f"{self.current_pokemon.name} switched with {self.team_list[n].name}."
                )
                print()
            except Exception:
                print(f"Can't switch out {self.current_pokemon}...")


def game_over_check(team):
    """Checks if there are any pokemon on the player's team who can still fight (HP greater than 0).
    Returns False if all Pokemon on team are fainted.
    pokemon.hp (int) -> bool"""
    non_fainted_pokemon_bool = 0

    for pokemon in team:
        if pokemon.hp > 0:
            non_fainted_pokemon_bool = 1

    return non_fainted_pokemon_bool
