from src.data_manager import DataManager
from src.player import *
from pathlib import Path
import json
import os


class Team:
    DEFAULT_PLAYERS = ["Tidus", "Datto", "Letty", "Jassu", "Botta", "Keepa"]
    BASE_DIR = Path(__file__).resolve().parent.parent
    SAVE_DIR = BASE_DIR / "saved_data"
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    def __new__(cls, data_manager: DataManager):
        if not data_manager.players:
            print("Error: Can't create a team before loading data. Use data_manager's load_data function first.")
            return None
        else:
            return super().__new__(cls)

    def __init__(self, data_manager: DataManager):

        self.players = []
        self.positions = {
            "LF": None, "RF": None, "MF": None,
            "LD": None, "RD": None, "GL": None,
            "Bench1": None, "Bench2": None
        }

        # Recruit the default players
        for name in self.DEFAULT_PLAYERS:
            try:
                player = data_manager.get_player(name)
                self.recruit(player)
            except KeyError:
                logger.error(f"Error: Player {name} not found. Check the data file.")
                raise KeyError(f"Player {name} not found. Check the data file.")

    def recruit(self, player: Player):
        """Adds a player to the team"""
        if player in self.players:
            logger.error(f"Error: {player.name} is already on the team.")
            raise ValueError(f"{player.name} is already on the team.")
        if len(self.players) >= 8:
            print("Team is full")
            player_to_release = self.release_prompt()
            self.release(player_to_release)
        self.players.append(player)

    def release_prompt(self) -> Player:
        print("Please select a player to release:")
        self.list_team()
        print("0. Exit")
        quit_loop = False
        while not quit_loop:
            user_input = input("Input the number of the player you would like to release: ").strip()
            try:
                index = int(user_input) - 1
                if index == -1:
                    quit_loop = True
                else:
                    return self.players[index]
            except (ValueError, IndexError):
                print("Using the numbers next to the names of the players, please only input a number from the list.")

    def release(self, player: Player):
        if player in self.players:
            self.players.remove(player)
        else:
            logger.info(f"Info: Attempted to release {player} from team, but {player} was not on the team.")
            raise ValueError(f"Attempted to release {player} from team, but {player} was not on the team.")

    def list_team(self):
        if self.players:
            for i, player in enumerate(self.players):
                print(f"{i + 1}. {player.name}")
        else:
            print("Team currently empty. Add some players!")

    def json_format_team(self) -> str:
        data = {
            "players": [player.__dict__ for player in self.players],
            "positions": self.positions}
        return json.dumps(data)

    def save_team(self):
        filename = input("Name your team: ")
        if os.path.exists(self.SAVE_DIR / filename):
            print(f"Team named {filename} already exists. Do you want to overwrite it?")
            invalid_choice = True
            while invalid_choice:
                choice = input("Type 'y' to overwrite, 'n' to cancel.")
                if choice == 'y':
                    break
                if choice == 'n':
                    self.save_team()
                    return
                print("You must enter a valid option to continue.")
        with open(self.SAVE_DIR / filename, 'w') as file:
            file.write(self.json_format_team())
