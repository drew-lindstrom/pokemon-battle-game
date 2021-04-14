from battle import attack
from pokemon import Pokemon
from team import Team
from teams import player1, player2


def print_pokemon_on_field(pokemon1, pokemon2):
    print(
        f"{pokemon1.name} - HP: {pokemon1.hp}/{pokemon1.max_hp}, Status: {pokemon1.status}"
    )
    print(
        f"{pokemon2.name} - HP: {pokemon2.hp}/{pokemon2.max_hp}, Status: {pokemon2.status}"
    )
    print()


def get_choice(team):
    choice = None
    current_pokemon = team.current_pokemon

    while choice not in range(10):
        print(f"What will {current_pokemon.name} do?")
        print()
        for n in range(len(current_pokemon.moves)):
            print(
                f"({n+1}) {current_pokemon.moves[n].name} - {current_pokemon.moves[n].pp}/{current_pokemon.moves[n].max_pp} PP"
            )
        print()
        print("(5) Switch Pokemon")
        print("(6) Details")
        print()

        choice = int(input()) - 1
        print()

        if choice == 4:
            choice = get_switch_choice(team)
        elif choice == 5:
            current_pokemon.show_stats()
            choice = None
        else:
            if current_pokemon.moves[n].check_pp() == False:
                choice = None
    return int(choice)


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

    choice = int(choice) + 5
    return choice


def find_turn_order(player1, player2):
    try:
        if player1.current_pokemon.speed > player2.current_pokemon.speed:
            return [player1, player2]
        # If the speed check is a tie, its usually random who goes first, but for the sake of AI consistency, the opponent will always go first.
        else:
            return [player2, player1]
    except:
        return None


def clear_screen():
    for n in range(17):
        print()


clear_screen()

while True:
    turn_order = find_turn_order(player1, player2)
    switch_list = []
    attack_list = []

    print_pokemon_on_field(player1.current_pokemon, player2.current_pokemon)

    for x in range(len(turn_order)):
        choice = get_choice(turn_order[x])
        clear_screen()
        if choice >= 5:
            switch_list.append([turn_order[x], choice - 5])

        elif choice in range(4):
            attack_list.append([turn_order[x], choice])

    for x in range(len(switch_list)):
        switch_list[x][0].switch(switch_list[x][1])

    for x in range(len(attack_list)):
        if attack_list[x][0] == player1:
            attack(player1.current_pokemon, attack_list[x][1], player2.current_pokemon)
        else:
            attack(player2.current_pokemon, attack_list[x][1], player1.current_pokemon)