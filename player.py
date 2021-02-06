from pokemon import Pokemon


class Player:
    def __init__(self, pokemon):
        self.team_list = []
        for n in range(len(pokemon)):
            self.team_list.append(pokemon[n])
        self.current_pokemon = self.team_list[0]
        self.light_screen = False
        self.light_screen_counter = 0
        self.reflect = False
        self.reflect_counter = 0
        self.stealth_rocks = False
        self.sticky_web = False
        self.spikes = 0
        self.tspikes = 0

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
        # Grounded Poision type pokemon remove toxic spikes when switched in even if wearing heavy duty boots.


def game_over_check(player):
    """Checks if there are any pokemon on the player's team who can still fight (HP greater than 0).
    Returns False if all Pokemon on team are fainted.
    pokemon.hp (int) -> bool"""
    non_fainted_pokemon_bool = 0

    for pokemon in player.team_list:
        if pokemon.hp > 0:
            non_fainted_pokemon_bool = 1

    return non_fainted_pokemon_bool


def set_light_screen(player):
    """Sets reflect on user's team for 5 turns (8 turns if pokemon is holding light clay)."""
    # TODO: Does this set it for 5 or 6 turns?
    if player.light_screen == False:
        player.light_screen = True
        if player.current_pokemon.item == "Light Clay":
            player.light_screen_counter = 8
        else:
            player.light_screen_counter = 5


def set_reflect(player):
    """Sets reflect on user's team for 5 turns (8 turns if user is holding light clay)."""
    # TODO: Does this set it for 5 or 6 turns?
    if player.reflect == False:
        player.reflect = True
        if player.current_pokemon.item == "Light Clay":
            player.reflect_counter = 8
        else:
            player.reflect_counter = 5


def reset_light_screen(player):
    """Sets the user's light_screen attribute to False if timer is at 0."""
    if player.light_screen_counter == 0:
        player.light_screen = False


def reset_reflect(player):
    """Sets the user's reflect attribute to False if timer is at 0."""
    if player.reflect_counter == 0:
        player.reflect = False


def set_spike(player):
    """Adds one spike to the player's spike count. Spike count max out at 3."""
    if player.spikes < 3:
        player.spikes += 1


def set_tspike(player):
    """Adds one toxic spike to the player's tspike count. Toxic spike count maxes out at 2."""
    if player.tspikes < 2:
        player.tspikes += 1


def clear_hazards(player):
    """Clears the hazards on the player's side of the field."""
    # Rapid spin clears all entry hazards.
    player.stealth_rocks = False
    player.sticky_web = False
    player.spikes = 0
    player.tspikes = 0