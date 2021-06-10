class Frame:
    """Frame class is used to specify the parameters for a player's "action" during a turn. Each turn consists of two frames, one frame is
    for player 1 with their chosen attack or, if switching, what pokemon on their team they'd like to switch into
    The other frame is for player 2 with the same parameters.
    Frame is used to simplfy passing data into various methods since all methods require some combination of the given inputs.
    For example, when calculating damage, the attacking pokemon's stats, defending pokemon's stats, and move data is taken into account.
    However, if there's a sandstorm, a rock type pokemon receives a special defense boost. In additional, if the defending team has
    light screens up, the defending pokemon also receives a speical defense boost."""

    def __init__(
        self,
        attacking_team=None,
        defending_team=None,
        attack=None,
        switch_choice=None,
        weather=None,
        terrain=None,
    ):
        self.attacking_team = attacking_team
        self.user = attacking_team.cur_pokemon
        self.defending_team = defending_team
        self.target = defending_team.cur_pokemon
        if attack:
            self.attack = self.user.moves[n]
        if switch_choice:
            self.switch_choice = switch_choice
        else:
            self.switch_choice = False
        self.weather = weather
        self.terrain = terrain
        self.can_attack = False
        self.attack_lands = False
        self.attack_damage = 0
        self.crit = False

    def update_cur_pokemon(self):
        "Whenever a switch occurs, updates the frames to switch the user/target to the current pokemon on the respective teams."
        self.user = self.attacking_team.cur_pokemon
        self.target = self.defending_team.cur_pokemon
