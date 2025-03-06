from src.DataManager import *

dm = DataManager()
dm.load_data("data/blitzball_players.json")


test_player = dm.get_player("Tidus")
test_player.display_info()