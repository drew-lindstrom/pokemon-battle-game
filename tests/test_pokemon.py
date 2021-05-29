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

    def test_apply_damage(self):
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
        test_pokemon.stat["hp"] = 200
        test_pokemon.apply_damage(50)
        assert test_pokemon.stat["hp"] == 150
        test_pokemon.stat["hp"] = 35
        test_pokemon.apply_damage(50)
        assert test_pokemon.stat["hp"] == 0
        assert test_pokemon.status[0] == "Fainted"

    def test_apply_damage_percentage(self):
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
        test_pokemon.apply_damage_percentage(0.5)
        assert test_pokemon.stat["hp"] == 197
        test_pokemon.stat["hp"] = 35
        test_pokemon.apply_damage_percentage(0.5)
        assert test_pokemon.stat["hp"] == 0

    def test_apply_recoil(self):
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
        test_pokemon.apply_recoil(0.5)
        assert test_pokemon.stat["hp"] == 197
        test_pokemon.stat["hp"] = 35
        test_pokemon.apply_recoil(0.5)
        assert test_pokemon.stat["hp"] == 0

    def test_check_fainted(self):
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
        assert p.check_fainted() == False
        p.stat["hp"] = 0
        assert p.check_fainted() == True
        assert p.status[0] == "Fainted"
        p.stat["hp"] = -4
        assert p.check_fainted() == True
        assert p.stat["hp"] == 0

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

    def test_set_status(self):
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
        assert p.status == [None, 0]
        p.set_status("Paralyzed")
        assert p.status == ["Paralyzed", 0]
        p.set_status("Asleep")
        assert p.status == ["Paralyzed", 0]
        p.status = [None, 0]
        p.set_status("Badly Poisoned")
        assert p.status == ["Badly Poisoned", 14]

    def test_cure_status(self):
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
        assert p.status == [None, 0]
        p.status = ["Paralyzed", 0]
        p.cure_status()
        assert p.status == [None, 0]

    def test_set_v_status(self):
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
        p.set_v_status("Flinched")
        assert "Flinched" in p.v_status
        p.set_v_status("Confused")
        assert "Confused" in p.v_status

    def test_decrement_statuses(self):
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
        p.v_status["Flinched"] = [1]
        p.v_status["Leech Seeded"] = [float("inf")]
        p.v_status["Confused"] = [2]
        p.v_status["Infatuated"] = [-4]
        p.status = ["Badly Poisoned", 14]
        p.decrement_statuses()
        assert p.v_status["Leech Seeded"] == [float("inf")]
        assert p.v_status["Confused"] == [1]
        assert len(p.v_status) == 2
        assert p.status == ["Badly Poisoned", 13]

    def test_reset_statuses(self):
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
        p.v_status["Flinched"] = [3]
        p.v_status["Leech Seeded"] = [float("inf")]
        p.status = ["Badly Poisoned", 5]
        p.reset_statuses()
        assert p.status == ["Badly Poisoned", 14]
        assert len(p.v_status) == 0

    def test_check_grounded(self):
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
        assert p.grounded == True
        p.ability = "Levitate"
        p.check_grounded()
        assert p.grounded == False
        p.item = "Iron Ball"
        p.check_grounded()
        assert p.grounded == True
        p.item = "Air Balloon"
        p.ability = None
        p.check_grounded()
        assert p.grounded == False
        p.v_status["Ingrained"] = [3]
        p.check_grounded()
        assert p.grounded == True
        del p.v_status["Ingrained"]
        p.v_status["Magnet Rise"] = [4]
        p.check_grounded()
        assert p.grounded == False
        del p.v_status["Magnet Rise"]
        p.v_status["Telekinesis"] = [3]
        p.check_grounded()
        assert p.grounded == False

    def test_set_prev_move(self):
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
        assert p.prev_move == None
        p.set_prev_move("Scald")
        assert p.prev_move == "Scald"

    def test_reset_prev_move(self):
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
        p.prev_move = "Scald"
        p.reset_prev_move()
        assert p.prev_move == None

    # TODO: test set_v_status
