from pokemon import Pokemon
from move import Move

#General notes, 
def adaptability(attacker, n):
    if attacker.type[0] == attacker.move[n].type or attacker.type[1] == attacker.move[n].type:
        #Stab *2 instead of 1.5

def aerilate(attacker, n):
    if attacker.move[n].type == 'Normal':
        #Attack type change to Flying
        #Power boost by 20% (Note: not overall damage boost)

def aftermath(attacker, n, defender):
    if attacker.ability == 'Damp':
        pass
    if time == "post_damage" and defender.hp == 0 and attacker.move[n].contact == True:
        #Damage attacker 1/4 of its max HP.

def airlock(attacker, n, defender):
    # Negates the effects of weather but doesn't eliminate the weather?

def analytic(attacker, n, defender):
    if attacker.turn == "Last":
        #Power boost by 30%

def anger_point(attacker, n, defender):
    if time == "post_damage":
        #Raise attack to +6 if hit with a critical hit.