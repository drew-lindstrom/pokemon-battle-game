from player import Player


def print_pokemon_on_field(pokemon1, pokemon2):
    print(
        f"{pokemon1.name} - HP: {pokemon1.stat['hp']}/{pokemon1.stat['max_hp']}, Status: {pokemon1.status[0]}"
    )
    print(
        f"{pokemon2.name} - HP: {pokemon2.stat['hp']}/{pokemon2.stat['max_hp']}, Status: {pokemon2.status[0]}"
    )
    print()


def get_choice(f):
    choice = None

    while choice not in range(1, 7):
        print_options(f.attacking_team)

        choice = int(input())
        print()

        if choice >= 1 and choice <= 4:
            # TODO: Add struggle.
            if f.user.moves[choice - 1].pp > 0:
                f.attack = f.user.moves[choice - 1]
                f.attack_name = (f.user.moves[choice - 1].name,)
                return f
            else:
                print(f"{team.cur_pokemon.moves[choice-1].name} is out of PP.")
                choice = None

        elif choice == 5:
            return get_switch(team)

        elif choice == 6:
            f.user.show_stats()
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


def get_switch(frame):
    team_list = []
    switch_choice = ""

    print(f"Switch {frame.user.name} with...?")

    for n in range(1, len(frame.attacking_team)):
        print(
            f"({n}) {frame.attacking_team[n].name} - {frame.attacking_team[n].stat['hp']}/{frame.attacking_team[n].stat['max_hp']} HP, Status: {frame.attacking_team[n].status}"
        )
        team_list.append(str(n))

    while switch_choice not in team_list:
        switch_choice = input()
        print()

    frame.switch_choice = switch_choice
    return frame


def clear_screen():
    for n in range(17):
        print()
