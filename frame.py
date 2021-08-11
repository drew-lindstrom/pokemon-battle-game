class Frame:
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
