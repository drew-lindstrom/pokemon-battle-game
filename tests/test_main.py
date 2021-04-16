import main
import pytest


class TestMain:
    def test_check_priority(self):
        assert main.check_priority("Ice Shard") == 1
        assert main.check_priority("Avalanche") == -4
        assert main.check_priority("Tackle") == 0
