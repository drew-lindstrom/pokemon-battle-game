from pokemon import Pokemon


class Team:
    def __init__(self, pokemon):
        self.team = []
        for n in range(len(pokemon)):
            self.team.append(pokemon[n])
        self.current_pokemon = self.team[0]

    def show_team(self):
        for n in range(len(self.team)):
            self.team[n].show_stats()

    def switch(self, n):
        if self.team[n].status == "Fainted":
            print(f"{self.team[n].name} has already fainted!")
        else:
            try:
                self.team[0], self.team[n] = self.team[n], self.team[0]
            except Exception:
                print(f"Can't switch out {self.team[0]}...")


slowbro = Pokemon(
    "Slowbro",
    100,
    "Male",
    ("Scald", "Slack Off", "Future Sight", "Teleport"),
    None,
    None,
    (31, 31, 31, 31, 31, 31),
    (252, 0, 252, 0, 4, 0),
    "Relaxed",
)
tyranitar = Pokemon(
    "Tyranitar",
    100,
    "Male",
    ("Crunch", "Stealth Rock", "Toxic", "Earthquake"),
    None,
    None,
    (31, 31, 31, 31, 31, 31),
    (252, 0, 0, 0, 216, 40),
    "Careful",
)

player1 = Team([slowbro, tyranitar])
player1.team[1].current_hp = 0
player1.switch(1)
player1.show_team()