import unittest
from pokemon import Pokemon


class TestPokemon(unittest.TestCase):
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
        self.assertEqual(testPokemon.hp, 394)
        self.assertEqual(testPokemon.max_hp, 394)
        self.assertEqual(testPokemon.attack, 186)
        self.assertEqual(testPokemon.defense, 350)
        self.assertEqual(testPokemon.sp_attack, 236)
        self.assertEqual(testPokemon.sp_defense, 197)
        self.assertEqual(testPokemon.speed, 86)


if __name__ == "__main__":
    unittest.main()