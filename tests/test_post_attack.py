from post_attack import *
from pokemon import Pokemon
from player import Player
from weather import Weather
from terrain import Terrain
from frame import Frame
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

    @pytest.fixture
    def test_frame(self):
        slowbro = Pokemon(
            "Slowbro",
            100,
            "Male",
            ("Scald", "Slack Off", "Future Sight", "Teleport"),
            "Regenerator",
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
            ("Pyro Ball", "U-turn", "Gunk Shot", "High Jump Kick"),
            "Libero",
            "Heavy Duty Boots",
            (31, 31, 31, 31, 31, 31),
            (0, 252, 0, 0, 4, 252),
            "Jolly",
        )
        p1 = Player([slowbro, tyranitar])
        p2 = Player([tapu_lele, cinderace])
        w = Weather()
        t = Terrain()
        test_frame = Frame(p1, p2, None, None, w, t)
        return test_frame

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

    @pytest.mark.parametrize("input_hp,expected_hp", [(360, 384), (380, 394)])
    def test_apply_leftovers(self, test_pokemon, input_hp, expected_hp):
        slowbro = test_pokemon
        slowbro.stat["hp"] = input_hp
        apply_leftovers(slowbro)
        assert slowbro.stat["hp"] == expected_hp

    @pytest.mark.parametrize("input_hp,expected_hp", [(394, 370), (5, 0)])
    def test_apply_burn(self, test_pokemon, input_hp, expected_hp):
        p = test_pokemon
        p.stat["hp"] = input_hp
        p.status = ["Burned"]
        apply_burn(p)
        assert p.stat["hp"] == expected_hp

    @pytest.mark.parametrize(
        "input_hp,input_status,expected_hp",
        [
            (394, ["Badly Poisoned", 14], 370),
            (370, ["Badly Poisoned", 13], 321),
            (394, ["Badly Poisoned", 0], 25),
            (300, ["Poisoned"], 251),
        ],
    )
    def test_apply_poison(self, test_pokemon, input_hp, input_status, expected_hp):
        p = test_pokemon
        apply_poison(p)
        p.stat["hp"] = input_hp
        p.status = input_status
        apply_poison(p)
        assert p.stat["hp"] == expected_hp

    @pytest.mark.parametrize("input_hp,expected_hp", [(394, 344), (35, 0)])
    def test_apply_recoil(self, test_pokemon, input_hp, expected_hp):
        p = test_pokemon
        p.stat["hp"] = input_hp
        apply_recoil(p, 100, 0.5)
        assert p.stat["hp"] == expected_hp

    @pytest.mark.parametrize(
        "input_name,i,item,expected_result",
        [
            ("Close Combat", 100, None, None),
            ("Close Combat", 20, "Protective Pads", None),
            ("Close Combat", 20, None, "Paralyzed"),
            ("Surf", 20, None, None),
        ],
    )
    def test_apply_static(self, test_frame, input_name, i, item, expected_result):
        test_frame.user.set_move(0, input_name)
        test_frame.attack = test_frame.user.moves[0]
        test_frame.user.item = item
        apply_static(test_frame, i)
        assert test_frame.user.status[0] == expected_result