import battle
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
    print(f"What will {pokemon.name} do?")
    print()
    for n in range(len(pokemon.moves)):
        print(
            f"({n}) {pokemon.moves[n].name} - {pokemon.moves[n].pp}/{pokemon.moves[n].max_pp} PP,",
            end=" ",
        )
    print("(5) Switch Pokemon")
    print("(6) for move details.")

    choice = None
    while choice not in ("0", "1", "2", "3", "4", "5", "6"):
        choice = input()
    return choice


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
    print_current_pokemon(player1.team[0], player2.team[0])
    player_1_choice = get_choice(player1.team[0])
    player_2_choice = get_choice(player2.team[0])
