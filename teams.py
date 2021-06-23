from pokemon import Pokemon
from player import Player

tapu_lele = Pokemon(
    "Tapu Lele",
    100,
    None,
    ("Psychic", "Moonblast", "Focus Blast", "Psyshock"),
    "Psychic Surge",
    "Choice Specs",
    (31, 0, 31, 31, 31, 31),
    (0, 0, 0, 252, 4, 252),
    "Timid",
)
cinderace = Pokemon(
    "Cinderace",
    100,
    "Male",
    ("Pyro Ball", "Blaze Kick", "Gunk Shot", "High Jump Kick"),
    "Libero",
    "Heavy Duty Boots",
    (31, 31, 31, 31, 31, 31),
    (0, 252, 0, 0, 4, 252),
    "Jolly",
)
excadrill = Pokemon(
    "Excadrill",
    100,
    "Male",
    ("Earthquake", "Iron Head", "Swords Dance", "Toxic"),
    "Sand Rush",
    "Leftovers",
    (31, 31, 31, 31, 31, 31),
    (0, 252, 0, 0, 4, 252),
    "Jolly",
)
slowbro = Pokemon(
    "Slowbro",
    100,
    "Male",
    ("Surf", "Slack Off", "Ice Beam", "Psychic"),
    "Regenerator",
    "Heav Duty Boots",
    (31, 31, 31, 31, 31, 31),
    (248, 0, 252, 8, 0, 0),
    "Relaxed",
)
tyranitar = Pokemon(
    "Tyranitar",
    100,
    "Male",
    ("Stealth Rock", "Crunch", "Stone Edge", "Fire Blast"),
    "Sand Stream",
    "Leftovers",
    (31, 31, 31, 31, 31, 31),
    (240, 16, 0, 0, 252, 0),
    "Sassy",
)
zapdos = Pokemon(
    "Zapdos",
    100,
    None,
    ("Discharge", "Hurricane", "Roost", "Defog"),
    "Static",
    "Heavy Duty Boots",
    (31, 31, 31, 31, 31, 31),
    (248, 0, 124, 0, 0, 136),
    "Bold",
)

heatran = Pokemon(
    "Heatran",
    100,
    None,
    ("Earth Power", "Eruption", "Fire Blast", "Flash Cannon"),
    "Flash Fire",
    "Choice Specs",
    (31, 0, 31, 31, 31, 31),
    (0, 0, 0, 252, 4, 252),
    "Modest",
)
tapu_lele_2 = Pokemon(
    "Tapu Lele",
    100,
    None,
    ("Psychic", "Moonblast", "Focus Blast", "Psyshock"),
    "Psychic Surge",
    "Choice Specs",
    (31, 0, 31, 31, 31, 31),
    (0, 0, 0, 252, 4, 252),
    "Timid",
)
urshifu = Pokemon(
    "Urshifu - Rapid Strike Style",
    100,
    None,
    ("Waterfall", "Close Combat", "Thunder Punch", "Aqua Jet"),
    "Unseen Fist",
    "Protective Pads",
    (31, 31, 31, 31, 31, 31),
    (0, 252, 0, 0, 4, 252),
    "Jolly",
)
hydreigon = Pokemon(
    "Hydreigon",
    100,
    "Male",
    ("Defog", "Roost", "Dark Pulse", "Earth Power"),
    "Levitate",
    "Leftovers",
    (31, 0, 31, 31, 31, 31),
    (252, 0, 0, 0, 4, 252),
    "Timid",
)
landorus = Pokemon(
    "Landorus - Therian Forme",
    100,
    "Male",
    ("Toxic", "Earthquake", "Stone Edge", "Knock Off"),
    "Intimidate",
    "Heavy Duty Boots",
    (31, 31, 31, 31, 31, 31),
    (176, 0, 188, 0, 0, 144),
    "Impish",
)
rillaboom = Pokemon(
    "Rillaboom",
    100,
    "Male",
    ("Grassy Glide", "Wood Hammer", "Knock Off", "Swords Dance"),
    "Grassy Surge",
    "Choice Band",
    (31, 31, 31, 31, 31, 31),
    (0, 252, 0, 0, 4, 252),
    "Adamant",
)

p1 = Player([tapu_lele, cinderace, excadrill, slowbro, tyranitar, zapdos])
p2 = Player([heatran, tapu_lele_2, urshifu, hydreigon, landorus, rillaboom])