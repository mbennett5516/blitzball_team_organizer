import unittest
from unittest.mock import patch
from io import StringIO
from src.Player import Player
from src.logger import logger


class TestPlayer(unittest.TestCase):

    def setUp(self):
        """Set up test environment before each test."""
        self.player = Player("Tidus", "N/A", {"2": {"HP": "130", "SH": "18"}, "start": {"level": "2"}},
                             ["Venom Tackle", "Drain Tackle 2"], {"0": ["Wither Shot"]})

    def test_get_stats_returns_correct_stats_with_correctly_formatted_player(self):
        result = self.player.get_stats(2)
        self.assertEqual(result, {"HP": '130', "SH": '18'})

    def test_get_stats_returns_closest_level_if_level_not_in_stats(self):
        result = self.player.get_stats(3)
        self.assertEqual(result, {"HP": '130', "SH": '18'})

    def test_get_stats_raises_value_error_with_wrong_level(self):
        with self.assertRaises(ValueError):
            self.player.get_stats(1)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_info_correctly_displays_player_info_with_good_player_data(self, stdout_mock):
        self.player.display_info()
        self.assertEqual(
            stdout_mock.getvalue(),
            "*********\n"
            "* Tidus *\n"
            "*********\n"
            "Location: N/A\n"
            "Key Techniques:\n"
            "1. Venom Tackle\n"
            "2. Drain Tackle 2\n\n"
            "Starting Stats:\n"
            "HP: 130\n"
            "SH: 18\n"
            "Learnable Techniques:\n"
            "Wither Shot\n")

    def test_display_info_logs_error_if_start_not_in_stats(self):
        self.player.stats = {"2": {"HP": "130", "SH": "18"}}
        with self.assertLogs(logger, level='ERROR') as context:
            self.player.display_info()
        self.assertEqual(context.output,
                         ['ERROR:blitzball:Error displaying player info: "Stats data for Tidus is '
                          'missing a \'start\' value. Check the data file."'])

    def test_display_info_logs_error_if_level_not_in_start(self):
        self.player.stats = {"2": {"HP": "130", "SH": "18"}, "start": {}}
        with self.assertLogs(logger, level='ERROR') as context:
            self.player.display_info()
        self.assertEqual(context.output,
                         ['ERROR:blitzball:Error displaying player info: "Stats data for Tidus is '
                          'missing a \'start\' value. Check the data file."'])

    def test_display_info_logs_error_if_zero_not_in_learnable_abilities(self):
        self.player.learnable_abilities = {"1": ["Wither Shot"]}
        with self.assertLogs(logger, level='ERROR') as context:
            self.player.display_info()
        self.assertEqual(context.output, ['ERROR:blitzball:Error displaying player info: "Key \'0\' not found '
                                          'in learnable abilities for Tidus. Check the data file."'])

    def test_display_info_logs_error_if_stats_not_initialized(self):
        self.player.stats = {}
        with self.assertLogs(logger, level='ERROR') as context:
            self.player.display_info()
        self.assertEqual(context.output, ['ERROR:blitzball:Error displaying player info: Stats not initialized '
                                          'for Tidus. Check the data file.'])

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_info_correctly_when_no_key_techniques(self, stdout_mock):
        self.player.key_techniques = []
        self.player.display_info()
        self.assertEqual(
            stdout_mock.getvalue(),
            "*********\n"
            "* Tidus *\n"
            "*********\n"
            "Location: N/A\n"
            "Key Techniques:\n"
            "No Key Techniques\n\n"
            "Starting Stats:\n"
            "HP: 130\n"
            "SH: 18\n"
            "Learnable Techniques:\n"
            "Wither Shot\n")

    def test_display_info_logs_error_if_start_level_not_in_stats(self):
        self.player.stats = {"1": {"HP": "130", "SH": "18"}, "start": {"level": "2"}}
        with self.assertLogs(logger, level='ERROR') as context:
            self.player.display_info()
        self.assertEqual(context.output, ["ERROR:blitzball:Error displaying player info: 'Key 2 not found "
                                          "for Tidus. Check the data file.'"])
