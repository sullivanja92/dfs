from scrapy import Field, Item


class GameItem(Item):
    """
    A Pro Football Reference game page model.
    """
    url = Field()
    home_team = Field()
    away_team = Field()
    home_score = Field()
    away_score = Field()
    datetime = Field()
    home_offense_stats = Field()
    away_offense_stats = Field()
    home_defense_stats = Field()
    away_defense_stats = Field()
    home_returns_stats = Field()
    away_returns_stats = Field()
    home_snap_counts = Field()
    away_snap_counts = Field()
    home_drives = Field()
    away_drives = Field()


class SalaryItem(Item):
    """
    A RotoGuru DFS site-specific salary page model.
    """
    url = Field()
    year = Field()
    week = Field()
    site = Field()
    salaries = Field()
