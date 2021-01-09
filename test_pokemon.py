import pytest
from pokemon import Pokemon


class TestPokemon:
    def test_init_stats(self):
        testPokemon = Pokemon(
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
        assert testPokemon.hp == 394
        assert testPokemon.max_hp == 394
        assert testPokemon.attack == 186
        assert testPokemon.defense == 350
        assert testPokemon.sp_attack == 236
        assert testPokemon.sp_defense == 197
        assert testPokemon.speed == 86
