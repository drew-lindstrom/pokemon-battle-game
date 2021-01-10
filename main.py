from battle import attack
from pokemon import Pokemon
from team import Team


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
                f"({n}) {pokemon.moves[n].name} - {pokemon.moves[n].pp}/{pokemon.moves[n].max_pp} PP,",
                end=" ",
            )
        print("(5) Switch Pokemon")
        print("(6) for move details.")
        print()

        choice = input()
    return choice


def get_switch_choice(team):
    choice_list = []
    choice = ""

    print(f"Switch {pokemon} with...?")

    for n, pokemon in enumerate(team):
        print(f"({n}) {pokemon.name} - {pokemon.name.hp}/{pokemon.name.max_hp} HP,")
        choice_list.append(n)

    while choice not in choice_list:
        choice = input()

    team.switch(n)


def turn_order_check(player1, player2):
    try:
        if player1.team[0].adj_speed > player2.team[0].adj_speed:
            return [player1, player2]
        # If the speed check is a tie, usually its random who goes first, but for the sake of consistency, the opponent will always go first.
        else:
            return [player2, player1]
    except:
        return None


slowbro = Pokemon(
    "Slowbro",
    100,
    "Male",
    ("Scald", "Slack Off", "Future Sight", "Teleport"),
    None,
    None,
    (31, 31, 31, 31, 31, 31),
    (252, 0, 252, 0, 4, 0),
    "Relaxed",
)
tyranitar = Pokemon(
    "Tyranitar",
    100,
    "Male",
    ("Crunch", "Stealth Rock", "Toxic", "Earthquake"),
    None,
    None,
    (31, 31, 31, 31, 31, 31),
    (252, 0, 0, 0, 216, 40),
    "Careful",
)

player1 = Team([slowbro])
player2 = Team([tyranitar])

while True:
    turn_order = turn_order_check(player1, player2)
    switch_order = []
    attack_order = []
    attack_choice = []

    print_current_pokemon(player1.team[0], player2.team[0])

    for x in range(len(turn_order)):
        choice = get_choice(turn_order[x].team[0])
        if choice == "5":
            switch_order.append(turn_order[x])
        else:
            attack_order.append(turn_order[x])
            attack_choice.append(int(choice))
    for x in range(len(switch_order)):
        get_switch_choice(switch_order[x])

    for x in range(len(attack_order)):
        if attack_order[x] == player1:
            attack(player1.team[0], attack_choice[x], player2.team[0])
        else:
            attack(player2.team[0], attack_choice[x], player1.team[0])