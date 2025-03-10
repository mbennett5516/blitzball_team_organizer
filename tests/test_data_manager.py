import os
import json
import unittest
from io import StringIO
from src.player import Player
from unittest.mock import patch
from src.data_manager import DataManager


class TestDataManager(unittest.TestCase):

    def setUp(self):
        """Set up test environment before each test."""
        self.manager = DataManager()
        self.sample_data = {
            "Tidus": {
                "location": "Besaid",
                "stats": {
                    "1": {
                        "SH": 20,
                        "EN": 15
                    },
                    "start": {
                        "level": 1
                    }
                },
                "key_techniques": ["Jecht Shot"],
                "learnable_abilities": {"0": ["Venom Tackle"]}
            },
            "Wakka": {
                "location": "Airship",
                "stats": {
                    "2": {
                        "SH": 17,
                        "EN": 15
                    },
                    "start": {
                        "level": 2
                    }
                },
                "key_techniques": ["Wither Shot", "Wither Pass", "Jecht Shot"],
                "learnable_abilities": {"0": ["Nap Pass, Nap Tackle"], "1": ["Drain Tackle"], "default": ["Venom Shot"]}
            }
        }
        self.correct_file_path = os.path.join(os.path.dirname(__file__), "../data/blitzball_players.json")

        self.incorrect_file_path = "wrong.json"

    def test_load_data_valid_json_parses_correctly(self):
        """Test that valid JSON data is correctly loaded into Player objects"""
        name = "Tidus"

        self.manager.players = {name: Player(name, **self.sample_data["Tidus"])}
        self.assertIn(name, self.manager.players)
        self.assertEqual(self.manager.players[name].location, "Besaid")
        self.assertIn("1", self.manager.players[name].stats)
        self.assertIn("start", self.manager.players[name].stats)
        self.assertIn("level", self.manager.players[name].stats["start"])
        self.assertEqual(self.manager.players[name].stats["start"]["level"], 1)

    def test_load_data_valid_file_path_loads_correctly(self):
        self.manager.players = {}  # Empty players dict
        self.manager.load_data(self.correct_file_path)
        self.assertTrue(self.manager.players)

    def test_load_data_file_not_found_exception(self):
        with self.assertRaises(FileNotFoundError):
            self.manager.load_data(self.incorrect_file_path)

    def test_load_data_permission_error(self):
        with self.assertRaises(IOError):
            self.manager.load_data('/etc/passwd')

    @patch("builtins.open", side_effect=IOError("Mocked I/O error"))
    def test_load_data_io_error(self, mock_file):
        """Test that an IOError is handled properly when loading data."""
        manager = DataManager()
        with self.assertRaises(IOError):
            manager.load_data(mock_file)

    @patch("builtins.open", side_effect=json.JSONDecodeError(
        "Mocked JSON Decode Error", "mock_file", 0))
    def test_load_data_invalid_json_raises_value_error(self, mock_file):
        with self.assertRaises(ValueError):
            self.manager.load_data(mock_file)

    @patch("builtins.open", side_effect=ValueError("Mocked Value Error"))
    def test_load_data_general_exception_raises_runtime_error(self, mock_file):
        with self.assertRaises(RuntimeError):
            self.manager.load_data(mock_file)

    def test_get_player_player_found(self):
        self.manager.players = {"Tidus": Player("Tidus", **self.sample_data["Tidus"])}
        tidus = self.manager.get_player("Tidus")
        self.assertIsInstance(tidus, Player)
        self.assertEqual(tidus.name, "Tidus")
        self.assertEqual(tidus.stats, {"1": {"SH": 20, "EN": 15}, "start": {"level": 1}})
        self.assertEqual(tidus.location, "Besaid")
        self.assertEqual(tidus.key_techniques, ["Jecht Shot"])
        self.assertEqual(tidus.learnable_abilities, {"0": ["Venom Tackle"]})

    def test_get_player_no_player_data_raises_runtime_error(self):
        self.manager.players = {}
        with self.assertRaises(RuntimeError):
            self.manager.get_player("Tidus")

    def test_get_player_player_not_found_raises_key_error(self):
        self.manager.players = {"Tidus": Player("Tidus", **self.sample_data["Tidus"])}
        with self.assertRaises(KeyError):
            self.manager.get_player("Wakka")

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_players_correctly_list_players(self, stdout_mock):
        self.manager.players = {"Tidus": Player("Tidus", **self.sample_data["Tidus"]),
                                "Wakka": Player("Wakka", **self.sample_data["Wakka"])}
        self.manager.list_players()
        output = stdout_mock.getvalue().strip().split("\n")
        self.assertIn("Tidus", output)
        self.assertIn("Wakka", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_list_players_no_player_data(self, stdout_mock):
        self.manager.players = {}
        self.manager.list_players()
        self.assertEqual(stdout_mock.getvalue(), "No player data available. Load data first.\n")
