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
        attackingTeam=None,
        defendingTeam=None,
        attack=None,
        switchChoice=None,
        weather=None,
        terrain=None,
    ):
        self.attackingTeam = attackingTeam
        self.user = attackingTeam.curPokemon
        self.defendingTeam = defendingTeam
        self.target = defendingTeam.curPokemon
        self.attack = None
        if switchChoice:
            self.switchChoice = switchChoice
        else:
            self.switchChoice = False
        self.weather = weather
        self.terrain = terrain
        self.canAttack = False
        self.attackLands = False
        self.attackDamage = 0
        self.crit = False

    def updateCurPokemon(self):
        "Whenever a switch occurs, updates the frames to switch the user/target to the current pokemon on the respective teams."
        self.user = self.attackingTeam.curPokemon
        self.target = self.defendingTeam.curPokemon
