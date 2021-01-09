from pokemon import Pokemon
from move import Move

#General notes, 
def adaptability(user, n):
    if user.type[0] == user.moves[n].type or user.type[1] == user.moves[n].type:
        #Stab *2 instead of 1.5

def aerilate(user, n):
    if user.move[n].type == 'Normal':
        #Attack type change to Flying
        #Power boost by 20% (Note: not overall damage boost)

def aftermath(user, n, opponent):
    if user.ability == 'Damp':
        pass
    if time == "post_damage" and opponent.hp == 0 and user.moves[n].contact == True:
        #Damage user 1/4 of its max HP.

def airlock(user, n, opponent):
    # Negates the effects of weather but doesn't eliminate the weather?

def analytic(user, n, opponent):
    if user.turn == "Last":
        #Power boost by 30%

def anger_point(user, n, opponent):
    if attackPhase == "post_damage":
        #Raise attack to +6 if hit with a critical hit.

def anticipation(user, n, opponent):
    # Pokemon will shudder if the opponent has a super effective damaging move, a one hit knockout move, selfdestruct or explosion.
    pass

def arena_trap(user, n, opponent):
    if user.grounded == 'False' or 'Flying' in user.type or 'Ghost' in user.type:
        user.trapped == 'True'
    # Baton pass, u-turn, volt switch, flip turn, parting shot, shed shell allow switching out
    # Doesn't work on teleport or smoke ball
    # This ability won't work if opponent switches out at the same time this pokemon is brought in.

def aroma_veil(user, n, opponent):
    #Prevents this pokemon from being afflicted by taunt, torment, encore, disable, and cursed body, heal block, and infatuation.

def as_one(user, n, opponent):
    # Ability of Calyrex
    pass

def aura_break(user, n, opponent):
    # Signature ability of Zygrade

def bad_dreams(user, n, opponent):
    # Signature ability of Darkrai
    pass

def ball_fetch(user, n, opponent):
    pass

def battery(user, n, opponent):
    pass

def battle_armor(user, n, opponent):
    """Prevents the opponent from landing a critical hit, even if the attack is Frost Breath, Storm Throw, Wicked Blow
    Surging Strikes, or the ability is Merciless with user poisoned"""
    # opponent can't be hit with critical hits.

def battle_bond(user, n, opponent):
    """When Greninja directly causes another Pokemon to faint by using a damaging move, it changes into Ask-Greninja until it faints.
    Greninja cannot change into Ash-Greninja again during the same battle even after being revived.
    If a pokemon transforms into Ash-Greninja, Water Shuriken doesn't receive power boost.
    Gastro Acid, Worry Seed, Simple Beam, Entrainment will fail if the target has Battle Bond.
    Role Play and Skill Swap will fail if either Pokemon has Battle Bond.
    Battle Bond cannot be copied by Trace, Power of Alchemy, or Receiver.
    Battle Bond cannot be replaced by Mummy or suppressed by Core Enforcer.
    If a pokemon other than Greninja obtains Battle Bond with Imposter or Transform, the Pokemon cannot change form into Ash-Greninja."""

def beast_boost(user, n, opponent):
    """When a Pokemon with Beast Boost directly causes another POkemon to faint by using a damaging move, its highest stat (other than HP)
    is increased by one stage for each Pokemon knocked out. Determining highest stat doesn't take into account stat stages, held items, or
    reductions due to status conditions. Does consider effects of Power Split, Guard Split, Power Trick, Wonder Room, and Speed Swap.
    If there is a tie from multiple stats, it increases one stat in prioitized order of: Attack, Defense, Special Attack, Special Defense,
    and Speed. Beast boost activates after the POkemon gains Attack from Fell Stinger. The ability Mummy replaces Beast Boost before it has the ability to activate."""
    pass

def berserk(user, n, opponent):
    # Ability of Drampa and Galarian Moltres
    pass

def big_pecks(user, n, opponent):
    """Prevents other Pokemon from lowering the Defense stat stage of the user. Does not prevent user from lowering their own Defense.
    Ability is ignored by Pokemon with Mold Breaker, Teravolt, and Turboblaze."""
    pass

def blaze(user, n, opponent):
    """If the user's HP is less than or equal to 1/3 their max HP and a fire type move is used, the user's Attack and Special Attack is
    boosted by 50% during damage calculations."""
    if user.hp <= user.max_hp / 3 and user.moves[n].type == 'Fire':
        stat_boost('Attack', 50)
        stat_boost('Special Attack', 50)

def bullet_proof(user, n, opponent):
    """Pokemon with Bulletproof are not affected by ball and bomb moves."""
    move_list = ['Acid Spray', 'Aura Sphere', 'Barrage', 'Beak Blast', 'Bullet Seed', 'Egg Bomb', 'Electro Ball', 'Energy Ball', 'Focus Blast', 'Gryo Ball', 'Ice Ball', 'Magnet Bomb', 'Mist Ball', 'Mud Bomb', 'Octazooka', 'Pollen Puff', 'Pyro Ball', 'Rock Blast', 'Rock Wrecker', 'Searing Shot', 'Seed Bomb', 'Shadow Ball', 'Sludge Bomb', 'Weather Ball', 'Zap Cannon']
    if user.moves[n] in move_list:
        pass
