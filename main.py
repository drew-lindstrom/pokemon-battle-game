from battle import attack
from pokemon import Pokemon
from team import Team
from teams import player1, player2


def print_current_pokemon(pokemon1, pokemon2):
    print(
        f"{pokemon1.name} - HP: {pokemon1.hp}/{pokemon1.max_hp}, Status: {pokemon1.status}"
    )
    print(
        f"{pokemon2.name} - HP: {pokemon2.hp}/{pokemon2.max_hp}, Status: {pokemon2.status}"
    )
    print()


def get_choice(pokemon):
    # TODO: add pp check
    choice = None
    while choice not in ("0", "1", "2", "3", "4", "5", "6"):
        print(f"What will {pokemon.name} do?")
        print()
        for n in range(len(pokemon.moves)):
            print(
                f"({n+1}) {pokemon.moves[n].name} - {pokemon.moves[n].pp}/{pokemon.moves[n].max_pp} PP"
            )
        print("(5) Switch Pokemon")
        print("(6) Move Details")
        print()

        choice = str(int(input()) - 1)
        print()
    return choice


def get_switch_choice(team):
    choice_list = []
    choice = ""

    print(f"Switch {team.current_pokemon.name} with...?")

    for n in range(len(team)):
        if n == 0:
            continue
        print(
            f"({n}) {team[n].name} - {team[n].hp}/{team[n].max_hp} HP, Status: {team[n].status}"
        )
        choice_list.append(str(n))

    while choice not in choice_list:
        choice = input()
        print()

    team.switch(choice)
    return None


def turn_order_check(player1, player2):
    try:
        if player1.team_list[0].adj_speed > player2.team_list[0].adj_speed:
            return [player1, player2]
        # If the speed check is a tie, usually its random who goes first, but for the sake of consistency, the opponent will always go first.
        else:
            return [player2, player1]
    except:
        return None


def clear_screen():
    for n in range(17):
        print()


while True:
    clear_screen()
    turn_order = turn_order_check(player1, player2)
    switch_order = []
    attack_order = []
    attack_choice = []

    print_current_pokemon(player1.team_list[0], player2.team_list[0])

    for x in range(len(turn_order)):
        choice = get_choice(turn_order[x].team_list[0])
        clear_screen()
        if choice == "5":
            switch_order.append(turn_order[x])
            clear_screen()
        else:
            attack_order.append(turn_order[x])
            attack_choice.append(int(choice))
            clear_screen()
    for x in range(len(switch_order)):
        get_switch_choice(switch_order[x])
        clear_screen()

    for x in range(len(attack_order)):
        if attack_order[x] == player1:
            attack(player1.team_list[0], attack_choice[x], player2.team_list[0])
        else:
            attack(player2.team_list[0], attack_choice[x], player1.team_list[0])