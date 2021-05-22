from player import Player


def print_pokemon_on_field(pokemon1, pokemon2):
    print(
        f"{pokemon1.name} - HP: {pokemon1.stat['hp']}/{pokemon1.stat['max_hp']}, Status: {pokemon1.status[0]}"
    )
    print(
        f"{pokemon2.name} - HP: {pokemon2.stat['hp']}/{pokemon2.stat['max_hp']}, Status: {pokemon2.status[0]}"
    )
    print()


def get_choice(team):
    choice = None

    while choice not in range(1, 7):
        print_options(team)

        choice = int(input())
        print()

        if choice >= 1 and choice <= 4:
            if team.cur_pokemon.moves[choice - 1].pp > 0:
                return (team, team.cur_pokemon.moves[choice - 1].name, choice - 1)
            else:
                print("{team.cur_pokemon.moves[choice-1].name} is out of PP.")
                choice = None

        elif choice == 5:
            return get_switch(team)

        elif choice == 6:
            team.cur_pokemon.show_stats()
            choice = None
            continue


def print_options(team):
    print(f"What will {team.cur_pokemon.name} do?")
    print()
    for n in range(len(team.cur_pokemon.moves)):
        print(
            f"({n+1}) {team.cur_pokemon.moves[n].name} - {team.cur_pokemon.moves[n].pp}/{team.cur_pokemon.moves[n].max_pp} PP"
        )
    print()
    print("(5) Switch Pokemon")
    print("(6) Details")
    print()


def get_switch(team):
    # TODO: HP Check

    team_list = []
    switch_choice = ""

    print(f"Switch {team.cur_pokemon.name} with...?")

    for n in range(1, len(team)):
        print(
            f"({n}) {team[n].name} - {team[n].hp}/{team[n].max_hp} HP, Status: {team[n].status}"
        )
        team_list.append(str(n))

    while switch_choice not in team_list:
        switch_choice = input()
        print()

    return (team, "Switch", n)


def clear_screen():
    for n in range(17):
        print()
