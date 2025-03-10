import json

from src.player import *


class DataManager:
    def __init__(self):
        self.players = {}

    def load_data(self, file_path: str):
        try:
            with open(file_path, mode='r') as data_file:
                data = json.load(data_file)
                for player_name, player_data in data.items():
                    new_player = Player(player_name, player_data["location"], player_data["stats"],
                                        player_data["key_techniques"], player_data["learnable_abilities"])
                    if player_name not in self.players:
                        self.players[player_name] = new_player
        except FileNotFoundError:
            logger.error(f"Error: The file '{file_path}' was not found")
            raise FileNotFoundError(f"The file '{file_path}' was not found. Ensure it exists and try again.")
        except IOError:
            logger.error(f"Error: An I/O error occurred while reading '{file_path}'.")
            raise IOError(f"An error occurred while reading '{file_path}'.")
        except json.JSONDecodeError:
            logger.error(f"Error: The file '{file_path}' contains invalid JSON.")
            raise ValueError(f"The file '{file_path}' contains invalid JSON. Check for formatting errors.")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise RuntimeError(f"Unexpected error: {e}")

    def get_player(self, name: str) -> Player:
        if not self.players:
            raise RuntimeError(f"Player data not initialized. Check the data file.")
        if name not in self.players:
            raise KeyError(f"Key {name} not found in data. Check the data file.")
        return self.players[name]

    def list_players(self):
        if not self.players:
            print(f"No player data available. Load data first.")
            return
        for name, _ in self.players.items():
            print(name)
