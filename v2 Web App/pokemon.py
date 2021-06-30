from game_data import naturesDict, pokemonDict, movesDict
from move import Move
import math
import random
import gameText


class Pokemon:
    def __init__(
        self, name, level, gender, moves, ability, item, IVs, EVs, nature, grounded=True
    ):
        self.name = name
        self.level = level
        self.gender = gender
        self.typing = list(pokemonDict[name][0])

        self.moves = [None, None, None, None]

        self.prevMove = None

        for n in range(4):
            self.setMove(n, moves[n])

        self.ability = ability
        self.item = item
        self.IVs = IVs
        self.EVs = EVs
        self.nature = nature
        self.stat = {
            "maxHp": 0,
            "hp": 0,
            "attack": 0,
            "defense": 0,
            "spAttack": 0,
            "spDefense": 0,
            "speed": 0,
        }
        self.initStat()

        self.statMod = {
            "attack": 0,
            "defense": 0,
            "spAttack": 0,
            "spDefense": 0,
            "speed": 0,
            "accuracy": 0,
            "evasion": 0,
        }
        # Non-volatile status (Freeze, Poinsoned, Badly Poisoned, Burned, Asleep, Paralyzed).
        # With the exception of Frozen and Asleep, an ability, item, or move is required to remove the status.
        # Statuses are persistent even after switching out. A pokemon can only have one non-volatile status at a time
        # and can not be over written if already afflicted with a different status.
        self.status = [None, 0]
        # Volatile statuses (Leech Seeded, Confused, Flinched, etc.).
        # These statuses clear when the pokemon switches out. Some statuses go away after a set number of turns.
        # A pokemon can have any number of volatile statuses.
        self.vStatus = {}
        self.grounded = True

    def __repr__(self):
        return self.name

    def initStat(self):
        """Initializes the hp, maxHp, attack, defense, special attack, special defense, and speed stat for the given pokemon based on the pokemon's
        IVs, EVs, and nature."""

        def statsFormula(n):
            return int(
                (
                    2 * int(pokemonDict[self.name][1][n])
                    + self.IVs[n]
                    + int(self.EVs[n] / 4)
                )
                * self.level
                / 100
            )

        for statName in self.stat:
            if statName is "hp" or statName is "maxHp":
                n = 0
                self.stat[statName] = int(statsFormula(n) + self.level + 10)
            else:
                statDictionary = {
                    "attack": 1,
                    "defense": 2,
                    "spAttack": 3,
                    "spDefense": 4,
                    "speed": 5,
                }
                n = statDictionary[statName]
                self.stat[statName] = int(
                    (statsFormula(n) + 5) * naturesDict[self.nature][n - 1]
                )

    def setMove(self, n, moveName):
        """Sets the move of the given name for the move slot 'n' of the pokemon."""
        self.moves[n] = Move(moveName)

    def updateStatModifier(self, stat, n):
        """Updates a given stat modifier by n. Stat modifieres can not be greater than 6 or less than -6."""
        self.statMod[stat] += n

        if n == 1:
            gameText.output += f"{self.name}s {stat} increased!\n"
        if n > 1:
            gameText.output += f"{self.name}s {stat} greatly increased!\n"
        if n == -1:
            gameText.output += f"{self.name}s {stat} decreased!\n"
        if n < -1:
            gameText.output += f"{self.name}s {stat} greatly decreased!\n"

        if self.statMod[stat] > 6:
            self.statMod[stat] = 6
        if self.statMod[stat] < -6:
            self.statMod[stat] = -6

    def resetStatModifier(self, printStatResetText=True):
        """Resets all stat modifiers of a given pokemon back to 0.
        Switching a pokemon out always resets stat modifiers. Certian moves also remove all stat modifiers."""
        for stat in self.statMod:
            self.statMod[stat] = 0

        if printStatResetText:
            gameText.output += f"{self.name}s stats were reset!\n"

    def showStats(self):
        """Prints the stats of the Pokemon with modifiers applied."""
        print(f"Pokemon: {self.name}")
        print(f"Type: {self.typing}")
        print(f"Level: {self.level}")
        print(f"Gender: {self.gender}")
        print(f"Ability: {self.ability}")
        print(f"Item: {self.item}")
        print(f"HP: {self.stat['hp']}/{self.stat['maxHp']}")
        print(f"Attack: {self.calcModifiedStat('attack')}/{self.stat['attack']}")
        print(f"Defense: {self.calcModifiedStat('defense')}/{self.stat['defense']}")
        print(
            f"Special Attack: {self.calcModifiedStat('spAttack')}/{self.stat['spAttack']}"
        )
        print(
            f"Special Defense: {self.calcModifiedStat('spDefense')}/{self.stat['spDefense']}"
        )
        print(f"Speed: {self.calcModifiedStat('speed')}/{self.stat['speed']}")
        print()

        for n in range(4):
            Move.showStats(self.moves[n])

    def calcModifiedStat(self, statName):
        """Calculates the modified stat of a Pokemomn if any stat modifiers are present.
        Accuracy and evasion are modified at a different scale (n = 3) than the other stats (n = 2). HP and maxHp do not have stat modifiers.
        Accuracy and evasion modifiers are also multipied by 100 while the other stats are multiplied by their respective base stats
        because accuracy/evasion is the chace out of 100% for an attack to hit/for a pokmeon to dodge a hit.
        Ex: A Pokemon with +6 attack modifier would have their attack stat multiplied by 4 (or (2 + 6)/2)."""

        def calcModifiedStatHelper(statName, n):

            if statName == "accuracy" or statName == "evasion":
                modifiedStat = 100
            else:
                modifiedStat = self.stat[statName]

            if self.statMod[statName] > 0:
                return int(modifiedStat * ((n + self.statMod[statName]) / n))
            elif self.statMod[statName] < 0:
                return int(modifiedStat * (n / (abs(self.statMod[statName]) + n)))
            else:
                return int(modifiedStat)

        if statName == "accuracy" or statName == "evasion":
            return calcModifiedStatHelper(statName, 3)
        return calcModifiedStatHelper(statName, 2)

    def applyHeal(self, n):
        """Heal pokemon by n percentage of it's max hp. Won't work on fainted Pokemon. HP won't exceed max hp.
        Ex: Slowbro's HP = 150 -> slowbro.heal(0.5) -> Slowbro's HP = 150 + 50% of max hp"""
        if self.stat["hp"] <= 0:
            gameText.output += f"{self.name} has fainted and can't be healed.\n"
            return

        if (n * self.stat["maxHp"]) > (self.stat["maxHp"] - self.stat["hp"]):
            healAmount = int(self.stat["maxHp"] - self.stat["hp"])
        else:
            healAmount = int(n * self.stat["maxHp"])

        self.stat["hp"] += healAmount
        gameText.output += f"{self.name} recovered {healAmount} HP!\n"

    def applyDamage(self, amount=None, percentage=None):
        """Damages pokemon by a specified amount or percentage. HP won't fall below 0. If HP is at 0, sets status to Fainted."""
        if self.stat["hp"] > 0:
            if amount:
                damage = int(amount)
            elif percentage:
                damage = int(percentage * self.stat["maxHp"])

            if damage > self.stat["hp"]:
                damage = int(self.stat["hp"])

            self.stat["hp"] -= damage

            gameText.output += f"{self.name} lost {damage} HP!\n"

            self.checkFainted()

    def checkFainted(self):
        """Checks if the pokemon is fainted (0 HP), and if True sets the pokemon's status to Fainted."""
        if self.status[0] == "Fainted":
            return True

        if self.stat["hp"] <= 0:
            gameText.output += f"{self.name} fainted!\n"
            self.status = ["Fainted", 0]
            self.stat["hp"] = 0
            return True
        return False

    def struggleCheck(self):
        """Checks the pp of all of the attacking Pokemon's moves. If all moves have zero pp, struggle is used to attack instead."""
        struggleBool = True
        for n in range(len(self.moves)):
            if self.moves[n].pp > 0:
                struggleBool = False
        return struggleBool

    def setStatus(self, statusName):
        """Sets the non-volatile status for the Pokemon. Second index of status list is to count number of turns.
        Badly Poisoned deals more damage every turn. Sleep has a greater chance to be cured every turn."""
        if self.status[0] is None:
            if statusName == "Badly Poisoned":
                self.status = [statusName, 14]
            elif statusName == "Asleep":
                self.status = [statusName, random.randint(1, 3)]
            else:
                self.status = [statusName, 0]
            gameText.output += f"{self.name} was inflicted with {statusName}!\n"

    def cureStatus(self):
        """Cures the non-volatile status for the Pokemon."""
        if self.status[0] != None:
            self.status = [None, 0]

    def setVStatus(self, statusName):
        """Sets the volatile status for the Pokemon. First index of the dictionary key is to count number of turns until status is cured."""
        if statusName == "Flinched":
            if statusName not in self.vStatus:
                self.vStatus["Flinched"] = [1]

        if statusName == "Confused":
            if statusName not in self.vStatus:
                print(f"{self.name} became confused!")
                self.vStatus["Confused"] = [random.randint(2, 5)]

    def decrementStatuses(self):
        """Decrements the counter for all volatile statuses and the counter for Sleep or Badly Poisoned for the Pokemon
        at the end of the turn. With the exception of Badly Poisoned, if a counter reaches 0, the status is removed."""
        if self.status[0] is "Asleep" or "Badly Poisoned":
            if self.status[1] > 0:
                self.status[1] -= 1

        temp = []
        for status in self.vStatus:
            self.vStatus[status][0] -= 1
            if self.vStatus[status][0] <= 0:
                temp.append(status)

        for status in temp:
            del self.vStatus[status]

    def resetStatuses(self):
        """Clears the Pokemon's volatile statues and resets the Badly Poison counter when it switches out."""
        if self.status[0] == "Badly Poisoned":
            self.status[1] = 14
        self.vStatus = {}

    def checkGrounded(self):
        """Checks to see if a pokemon is considered grounded at the start of a turn.
        Non grounded pokemon are immune to ground type moves and entry hazards with the exception of stealth rocks."""
        if (
            "Flying" in self.typing
            or self.ability == "Levitate"
            or self.item == "Air Balloon"
            or "Magnet Rise" in self.vStatus
            or "Telekinesis" in self.vStatus
        ):
            if self.item == "Iron Ball" or "Ingrained" in self.vStatus:
                self.grounded = True
            else:
                self.grounded = False
        else:
            self.grounded = True

    def setPreviousMove(self, moveName):
        """Updates the prevMove attribute whenever a pokemon uses a move."""
        self.prevMove = moveName

    def resetPreviousMove(self):
        """Resets a pokemon's prevMove attribute, typically when they switch out."""
        self.prevMove = None

    def checkChoiceItem(self):
        """Checks if pokemon is holding a choice item, and if so, adds Move Lock to vStatus if not already there."""
        if (
            self.item == "Choice Scarf"
            or self.item == "Choice Band"
            or self.item == "Choice Specs"
        ):
            self.vStatus["Move Lock"] = [1]

    def checkMoveLock(self):
        """Checks if move lock is currently in the pokemons vStatus dictionary."""
        if "Move Lock" in self.vStatus:
            return True
        return False