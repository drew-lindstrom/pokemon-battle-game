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
dragonite = Pokemon(
    "Dragonite",
    100,
    "Male",
    ("Dragon Dance", "Dual Wingbeat", "Earthquake", "Extreme Speed"),
    None,
    None,
    (31, 31, 31, 31, 31, 31),
    (0, 252, 0, 0, 4, 252),
    "Adamant",
)
nidoking = Pokemon(
    "Nidoking",
    100,
    "Male",
    ("Sludge Wave", "Earth Power", "Flamethrower", "Ice Beam"),
    None,
    None,
    (31, 31, 31, 31, 31, 31),
    (0, 0, 0, 252, 4, 252),
    "Timid",
)

player1 = Team([slowbro, dragonite])
player2 = Team([tyranitar, nidoking])