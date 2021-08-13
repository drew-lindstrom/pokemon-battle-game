from game_data import naturesDict, pokemonDict, movesDict
from move import Move
import math
import random
import gameText
import json


class Pokemon:
    def __init__(
            self, name, level, gender, moves, ability, item, IVs, EVs, nature, typing=[], prevMove=None,
            stat={}, statMod={}, status=[], vStatus={}, grounded=True):
        self.name = name
        self.level = level
        self.gender = gender
        self.typing = list(pokemonDict[name][0])

        # TODO: Will probably need to add logic like this for all attributes besides name/level/etc.
        if isinstance(moves[0], str):
            self.moves = [None, None, None, None]
            for n in range(4):
                self.setMove(n, moves[n])
        else:
            self.moves = moves

        self.prevMove = None

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
        self.status = [None, 0]
        self.vStatus = {}
        self.grounded = True

    def __repr__(self):
        return self.name

    def initStat(self):
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
            if statName == "hp" or statName == "maxHp":
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

    def setMove(self, n, name):
        self.moves[n] = Move(name)

    def updateStatModifier(self, stat, n):
        self.statMod[stat] += n

        if n == 1:
            gameText.output.append(f"{self.name}s {stat} increased!")
            gameText.output.append("")
        if n > 1:
            gameText.output.append(f"{self.name}s {stat} greatly increased!")
            gameText.output.append("")
        if n == -1:
            gameText.output.append(f"{self.name}s {stat} decreased!")
            gameText.output.append("")
        if n < -1:
            gameText.output.append(f"{self.name}s {stat} greatly decreased!")
            gameText.output.append("")

        if self.statMod[stat] > 6:
            self.statMod[stat] = 6
        if self.statMod[stat] < -6:
            self.statMod[stat] = -6

    def resetStatModifier(self, printStatResetText=True):
        for stat in self.statMod:
            self.statMod[stat] = 0

        if printStatResetText and self.status[0] != "Fainted":
            gameText.output.append(f"{self.name}s stats were reset!")
            gameText.output.append("")

    def showStats(self):
        gameText.output.append(f"Pokemon: {self.name}")
        gameText.output.append(f"Type: {self.typing}")
        gameText.output.append(f"Level: {self.level}")
        gameText.output.append(f"Gender: {self.gender}")
        gameText.output.append(f"Ability: {self.ability}")
        gameText.output.append(f"Item: {self.item}")
        gameText.output.append(f"HP: {self.stat['hp']}/{self.stat['maxHp']}")
        gameText.output.append(
            f"Attack: {self.calcModifiedStat('attack')}/{self.stat['attack']}"
        )
        gameText.output.append(
            f"Defense: {self.calcModifiedStat('defense')}/{self.stat['defense']}"
        )
        gameText.output.append(
            f"Special Attack: {self.calcModifiedStat('spAttack')}/{self.stat['spAttack']}"
        )
        gameText.output.append(
            f"Special Defense: {self.calcModifiedStat('spDefense')}/{self.stat['spDefense']}"
        )
        gameText.output.append(
            f"Speed: {self.calcModifiedStat('speed')}/{self.stat['speed']}"
        )
        gameText.output.append("")

        for n in range(4):
            Move.showStats(self.moves[n])

    def calcModifiedStat(self, statName):
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
        if self.stat["hp"] <= 0:
            gameText.output.append(
                f"{self.name} has fainted and can't be healed.")
            gameText.output.append("")
            return

        if (n * self.stat["maxHp"]) > (self.stat["maxHp"] - self.stat["hp"]):
            healAmount = int(self.stat["maxHp"] - self.stat["hp"])
        else:
            healAmount = int(n * self.stat["maxHp"])

        self.stat["hp"] += healAmount
        gameText.output.append(f"{self.name} recovered {healAmount} HP!")
        gameText.output.append("")

    def applyDamage(self, amount=None, percentage=None):
        if self.stat["hp"] > 0:
            if amount:
                damage = int(amount)
            elif percentage:
                damage = int(percentage * self.stat["maxHp"])

            if damage > self.stat["hp"]:
                damage = int(self.stat["hp"])

            self.stat["hp"] -= damage

            gameText.output.append(f"{self.name} lost {damage} HP!")
            gameText.output.append("")

            self.checkFainted()

    def checkFainted(self):
        if self.status[0] == "Fainted":
            return True

        if self.stat["hp"] <= 0:
            gameText.output.append(f"{self.name} fainted!")
            gameText.output.append("")
            self.status = ["Fainted", 0]
            self.stat["hp"] = 0
            return True
        return False

    def struggleCheck(self):
        struggleBool = True
        for n in range(len(self.moves)):
            if self.moves[n].pp > 0:
                struggleBool = False
        return struggleBool

    def setStatus(self, statusName):
        if self.status[0] is None:
            if statusName == "Badly Poisoned":
                self.status = [statusName, 14]
            elif statusName == "Asleep":
                self.status = [statusName, random.randint(1, 3)]
            else:
                self.status = [statusName, 0]
            gameText.output.append(
                f"{self.name} was inflicted with {statusName}!")
            gameText.output.append("")

    def cureStatus(self):
        if self.status[0] != None:
            self.status = [None, 0]

    def setVStatus(self, statusName):
        if statusName == "Flinched":
            if statusName not in self.vStatus:
                self.vStatus["Flinched"] = [1]

        if statusName == "Confused":
            if statusName not in self.vStatus:
                gameText.output.append(f"{self.name} became confused!")
                gameText.output.append("")
                self.vStatus["Confused"] = [random.randint(2, 5)]

    def decrementStatuses(self):
        if self.status[0] == "Asleep" or self.status[0] == "Badly Poisoned":
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
        if self.status[0] == "Badly Poisoned":
            self.status[1] = 14
        self.vStatus = {}

    def checkGrounded(self):
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
        self.prevMove = moveName

    def resetPreviousMove(self):
        self.prevMove = None

    def checkChoiceItem(self):
        if (
            self.item == "Choice Scarf"
            or self.item == "Choice Band"
            or self.item == "Choice Specs"
        ):
            self.vStatus["Move Lock"] = [1]

    def checkMoveLock(self):
        if "Move Lock" in self.vStatus:
            return True
        return False

    @classmethod
    def deserializeAndUpdatePokemonFromJson(cls, data):
        moves = list(
            map(Move.deserializeAndUpdateMoveFromJson, data['moves']))
        return cls(name=data['name'], level=data['level'], gender=data['gender'], moves=moves, ability=data['ability'], item=data['item'],
                   IVs=data['IVs'], EVs=data['EVs'], nature=data['nature'], typing=data['typing'], prevMove=data['prevMove'], stat=data['stat'],
                   statMod=data['statMod'], status=data['status'], vStatus=data['vStatus'], grounded=data['grounded'])
