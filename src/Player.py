from .logger import logger


class Player:
    def __init__(self, name: str, location: str, stats: dict, key_techniques: list, learnable_abilities: dict):
        self.name = name
        self.location = location
        self.stats = stats
        self.key_techniques = key_techniques
        self.learnable_abilities = learnable_abilities

    def get_stats(self, level: int) -> dict:
        if str(level) in self.stats:
            return self.stats[f"{level}"]
        else:
            available_levels = sorted(int(lvl) for lvl in self.stats.keys() if lvl.isdigit())
            closest_level = max((lvl for lvl in available_levels if lvl <= level), default=None)
            if closest_level is not None:
                logger.error(
                    f"Stats for level {level} not found for {self.name}; returning stats for level {closest_level}"
                )
                return self.stats[str(closest_level)]
        raise ValueError(f"Stats for {self.name} are unavailable.")

    def display_info(self):
        """Displays the player's information in a readable format."""
        try:
            self.validate_player_data()
            key_techs = self.format_key_techniques()
            starting_stats = self.format_starting_stats()
            learnable_techs = self.format_learnable_techs()

            print("*" * (len(self.name) + 4))
            print(f"* {self.name} *")
            print("*" * (len(self.name) + 4))
            print(f"Location: {self.location}\n"
                  f"Key Techniques:\n{key_techs}\n\n"
                  f"Starting Stats:\n{starting_stats}\n"
                  f"Learnable Techniques:\n{learnable_techs}")

        except (KeyError, ValueError) as e:
            logger.error(f"Error displaying player info: {e}")

    def validate_player_data(self):
        """Ensures that the player's data is correctly structured and contains necessary attributes."""
        if not self.stats:
            raise ValueError(f"Stats not initialized for {self.name}. Check the data file.")

        if "start" not in self.stats or "level" not in self.stats["start"]:
            raise KeyError(f"Stats data for {self.name} is missing a 'start' value. Check the data file.")

        if not self.key_techniques:
            self.key_techniques = []

        if "0" not in self.learnable_abilities:
            raise KeyError(f"Key '0' not found in learnable abilities for {self.name}. Check the data file.")

    def format_key_techniques(self) -> str:
        """Formats key techniques for display."""
        if not self.key_techniques:
            return "No Key Techniques"

        return "\n".join([f"{i + 1}. {tech}" for i, tech in enumerate(self.key_techniques)])

    def format_starting_stats(self) -> str:
        """Formats starting stats for display."""
        starting_level = self.stats["start"]["level"]

        if starting_level not in self.stats:
            raise KeyError(f"Key {starting_level} not found for {self.name}. Check the data file.")

        return "\n".join(f"{key}: {value}" for key, value in self.stats[starting_level].items())

    def format_learnable_techs(self) -> str:
        """Formats learnable techniques for display."""
        learnable_techs_list = sorted(self.learnable_abilities.get("0", []))
        return "\n".join(learnable_techs_list) if learnable_techs_list else "No Learnable Techniques"
