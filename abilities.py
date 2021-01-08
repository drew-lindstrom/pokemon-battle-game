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
