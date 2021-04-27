import pytest
import ui
from io import StringIO
from pokemon import Pokemon
from player import Player


# class TestUI:
#     def test_get_choice(self, monkeypatch):
#         slowbro = Pokemon(
#             "Slowbro",
#             100,
#             "Male",
#             ("Scald", "Slack Off", "Future Sight", "Teleport"),
#             None,
#             None,
#             (31, 31, 31, 31, 31, 31),
#             (252, 0, 252, 0, 4, 0),
#             "Relaxed",
#         )
#         team = Player([slowbro])
#         input_ = StringIO("0")
#         monkeypatch.setattr("builtins.input", input_)
#         assert ui.get_choice(team) == (team, "Scald", 0)

#     # def test_get_switch(self):