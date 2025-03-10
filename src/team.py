from data_manager import DataManager
from src.player import *


class Team:
    DEFAULT_PLAYERS = ["Tidus", "Datto", "Letty", "Jassu", "Botta", "Keepa"]

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
