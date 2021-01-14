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
        n = int(n)
        if self.team_list[n].status == "Fainted":
            print(f"{self.team_list[n].name} has already fainted!")
        else:
            try:
                self.team_list[0], self.team_list[n] = (
                    self.team_list[n],
                    self.team_list[0],
                )
            except Exception:
                print(f"Can't switch out {self.team_list[0]}...")
