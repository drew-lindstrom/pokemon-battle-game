from player import Player
from pokemon import Pokemon
from move import Move
from terrain import Terrain


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


def set_stealth_rocks(frame):
    """Adds stealth rocks to the target player's side."""
    if frame.defending_team.stealth_rocks == False:
        frame.defending_team.stealth_rocks = True
        print("Stealth Rocks were placed on the opposing teams side!")
        print()


def set_spike(player):
    """Adds one spike to the player's spike count. Spike count max out at 3."""
    if player.spikes < 3:
        player.spikes += 1


def set_tspike(player):
    """Adds one toxic spike to the player's tspike count. Toxic spike count maxes out at 2."""
    if player.tspikes < 2:
        player.tspikes += 1


def set_sticky_web(player):
    """Adds sticky web to the target player's side."""
    player.sticky_web = True


def activate_defog(frame):
    """Using defog clears entry hazards from both sides of the field and lowers the opposing pokemon's evasion by 1."""
    player.clear_hazards(frame.user)
    player.clear_hazards(frame.target)
    print("The entry hazards were removed from the field!")
    frame.target.update_stat_modifier("evasion", -1)


def roost(attacker, defender):
    attacker.heal(0.5)
    # TODO: Need to add grounding


def slack_off(attacker, defender):
    attacker.heal(0.5)


def frost_breath():
    # check for battle armor
    pass


def storm_throw():
    # check for battle armor
    pass


def wicked_blow():
    # check for battle armor
    pass


def surging_strikes():
    # check for battle armor
    pass
