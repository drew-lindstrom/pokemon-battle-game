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
        assert test_pokemon.stat["hp"] == 394
        assert test_pokemon.stat["max_hp"] == 394
        assert test_pokemon.stat["attack"] == 186
        assert test_pokemon.stat["defense"] == 350
        assert test_pokemon.stat["sp_attack"] == 236
        assert test_pokemon.stat["sp_defense"] == 197
        assert test_pokemon.stat["speed"] == 86

    def test_update_stat_modifier(self):
        p = Pokemon(
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
        p.update_stat_modifier("attack", 4)
        assert p.stat_mod["attack"] == 4
        p.update_stat_modifier("attack", 4)
        assert p.stat_mod["attack"] == 6
        p.update_stat_modifier("attack", -7)
        assert p.stat_mod["attack"] == -1
        p.update_stat_modifier("attack", -7)
        assert p.stat_mod["attack"] == -6

    def test_reset_stat_modifier(self):
        p = Pokemon(
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

        p.stat_mod["attack"] == 5
        p.stat_mod["defense"] == -4
        p.reset_stat_modifier()
        assert p.stat_mod["attack"] == 0
        assert p.stat_mod["defense"] == 0
        assert p.stat_mod["speed"] == 0

    def test_calc_modified_stat(self):
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
        slowbro.stat_mod["sp_attack"] = 6
        slowbro.stat_mod["attack"] = -6
        slowbro.stat_mod["accuracy"] = 4
        slowbro.stat_mod["evasion"] = -4
        assert slowbro.calc_modified_stat("sp_attack") == int(
            slowbro.stat["sp_attack"] * 4
        )
        assert slowbro.calc_modified_stat("attack") == int(slowbro.stat["attack"] / 4)
        assert slowbro.calc_modified_stat("accuracy") == int(7 / 3 * 100)
        assert slowbro.calc_modified_stat("evasion") == int(3 / 7 * 100)

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
        test_pokemon.stat["hp"] = 150
        test_pokemon.heal(0.5)
        assert test_pokemon.stat["hp"] == 347
        test_pokemon.stat["hp"] = 393
        test_pokemon.heal(0.5)
        assert test_pokemon.stat["hp"] == 394
        test_pokemon.stat["hp"] = 0
        test_pokemon.heal(0)
        assert test_pokemon.stat["hp"] == 0

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
        assert test_pokemon.stat["hp"] == 197
        test_pokemon.stat["hp"] = 35
        test_pokemon.damage(0.5)
        assert test_pokemon.stat["hp"] == 0

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