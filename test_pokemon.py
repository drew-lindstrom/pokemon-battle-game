import pytest
from pokemon import Pokemon


class TestPokemon:
    def test_init_stats(self):
        test_pokemon = Pokemon(
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
        assert test_pokemon.hp == 394
        assert test_pokemon.max_hp == 394
        assert test_pokemon.attack == 186
        assert test_pokemon.defense == 350
        assert test_pokemon.sp_attack == 236
        assert test_pokemon.sp_defense == 197
        assert test_pokemon.speed == 86

    def test_heal(self):
        test_pokemon = Pokemon(
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
        test_pokemon.hp = 150
        test_pokemon.heal(0.5)
        assert test_pokemon.hp == 347
        test_pokemon.hp = 393
        test_pokemon.heal(0.5)
        assert test_pokemon.hp == 394
        test_pokemon.hp = 0
        test_pokemon.heal(0)
        assert test_pokemon.hp == 0

    def test_damage(self):
        test_pokemon = Pokemon(
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
        test_pokemon.damage(0.5)
        assert test_pokemon.hp == 197
        # TODO: What happens if resulting HP needs to round?
        test_pokemon.hp = 35
        test_pokemon.damage(0.5)
        assert test_pokemon.hp == 0

    def test_struggle_check(self):
        test_pokemon = Pokemon(
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
        assert test_pokemon.struggle_check() == False
        test_pokemon.moves[0].pp = 0
        assert test_pokemon.struggle_check() == False
        test_pokemon.moves[1].pp = 0
        assert test_pokemon.struggle_check() == False
        test_pokemon.moves[2].pp = 0
        assert test_pokemon.struggle_check() == False
        test_pokemon.moves[3].pp = 0
        assert test_pokemon.struggle_check() == True