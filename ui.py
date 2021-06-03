from player import Player


def print_pokemon_on_field(pokemon1, pokemon2):
    print(
        f"{pokemon1.name} - HP: {pokemon1.stat['hp']}/{pokemon1.stat['max_hp']}, Status: {pokemon1.status[0]}"
    )
    print(
        f"{pokemon2.name} - HP: {pokemon2.stat['hp']}/{pokemon2.stat['max_hp']}, Status: {pokemon2.status[0]}"
    )
    print()


def get_choice(frame, input_list=[]):
    choice = None

    while choice not in range(1, 7):
        print_options(frame.attacking_team)
        choice_options = ["1", "2", "3", "4", "5", "6"]
        choice = None
        while choice is None or choice not in choice_options:
            if len(input_list) == 0:
                choice = input()
            else:
                choice = input_list.pop(0)
            print()

        choice = int(choice)

        if choice >= 1 and choice <= 4:
            if frame.user.moves[choice - 1].pp <= 0:
                print(f"{frame.user.moves[choice-1].name} is out of PP.")
                print()
                choice = None
            elif "Move Lock" in frame.user.v_status and (
                frame.user.prev_move != None
                and frame.user.prev_move != frame.attack_name
            ):
                print(f"{frame.user.name} must use {frame.user.prev_move}.")
                print()
                choice = None
            else:
                frame.attack = frame.user.moves[choice - 1]
                frame.attack_name = frame.user.moves[choice - 1].name
                return frame

        elif choice == 5:
            if len(input_list) > 0:
                return get_switch(frame, input_list)
            return get_switch(frame)

        elif choice == 6:
            frame.user.show_stats()
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


def get_switch(frame, input_list=[]):
    team_list = []
    switch_choice = ""

    print(f"Switch {frame.user.name} with...?")

    for n in range(1, len(frame.attacking_team)):
        print(
            f"({n}) {frame.attacking_team[n].name} - {frame.attacking_team[n].stat['hp']}/{frame.attacking_team[n].stat['max_hp']} HP, Status: {frame.attacking_team[n].status[0]}"
        )
        team_list.append(str(n))
    print()

    while switch_choice not in team_list:
        if len(input_list) == 0:
            switch_choice = input()
        else:
            switch_choice = input_list.pop(0)
        print()

    frame.switch_choice = switch_choice
    return frame


def clear_screen():
    for n in range(17):
        print()
