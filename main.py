from src.data_manager import *
from src.team import *

dm = DataManager()
dm.load_data("data/blitzball_players.json")


team = Team(dm)
team.save_team()
