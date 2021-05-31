from post_attack import *
from pokemon import Pokemon
import pytest


class TestPostAttack:
    @pytest.fixture
    def test_pokemon(self):
        test_pokemon = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            None,
            "Leftovers",
            (31, 31, 31, 31, 31, 31),
            (252, 0, 252, 0, 4, 0),
            "Relaxed",
        )
        return test_pokemon

    def test_apply_stat_alt_attack(self, test_pokemon):
        p = test_pokemon
        assert p.stat_mod["defense"] == 0
        assert p.stat_mod["sp_defense"] == 0
        apply_stat_alt_attack(p, None, "Close Combat", 50)
        assert p.stat_mod["defense"] == -1
        assert p.stat_mod["sp_defense"] == -1

    def test_apply_status_inflicting_attack(self, test_pokemon):
        p = test_pokemon
        assert p.status[0] == None
        apply_status_inflicting_attack(None, p, "Toxic", 50)
        assert p.status[0] == "Badly Poisoned"

    def test_apply_v_status_inflicting_attack(self, test_pokemon):
        p = test_pokemon
        assert len(p.v_status) == 0
        apply_v_status_inflicting_attack(None, p, "Dark Pulse", 20)
        assert p.v_status["Flinched"] == [1]

    def test_apply_leftovers(self, test_pokemon):
        slowbro = test_pokemon
        slowbro.stat["hp"] = 360
        apply_leftovers(slowbro)
        assert slowbro.stat["hp"] == 384
        slowbro.hp = 380
        apply_leftovers(slowbro)
        assert slowbro.stat["hp"] == 394

    def test_apply_burn(self, test_pokemon):
        p = test_pokemon
        apply_burn(p)
        assert p.stat["hp"] == 394
        p.status = ["Burned"]
        apply_burn(p)
        assert p.stat["hp"] == 369
        p.stat["hp"] = 5
        apply_burn(p)
        assert p.stat["hp"] == 0

    def test_apply_bad_poison(self, test_pokemon):
        p = test_pokemon
        apply_bad_poison(p)
        assert p.stat["hp"] == 394
        p.status = ["Badly Poisoned", 14]
        apply_bad_poison(p)
        assert p.stat["hp"] == 369
        p.status = ["Badly Poisoned", 13]
        apply_bad_poison(p)
        assert p.stat["hp"] == 319
        p.stat["hp"] = 394
        p.status = ["Badly Poisoned", 0]
        apply_bad_poison(p)
        assert p.stat["hp"] == 24