
class PFRTeamAbbreviationPipeline:
    """
    A pipeline used to correct team abbreviations found in PFR>
    """

    team_abbreviations = {
        'RAV': 'BAL',
        'NWE': 'NE',
        'GNB': 'GB',
        'JAX': 'JAC',
        'CLT': 'IND',
        'RAI': 'LV',
        'SDG': 'LAC',
        'CRD': 'ARI',
        'SFO': 'SF',
        'TAM': 'TB',
        'NOR': 'NO',
        'RAM': 'LAR',
        'OTI': 'TEN',
        'KAN': 'KC',
        'HTX': 'HOU',
        'LVR': 'LV'
    }

    def process_item(self, item, spider):
        """
        Corrects the team abbreviations scraped from PFR>

        :param item: the scraped game item
        :param spider: the game spider
        :return: the corrected game item
        """
        item['home_team'] = self.team_abbreviations.get(item['home_team'], item['home_team'])
        item['away_team'] = self.team_abbreviations.get(item['away_team'], item['away_team'])
        for player in item['home_offense_stats']:
            player['team'] = self.team_abbreviations.get(player['team'], player['team'])
        for player in item['away_offense_stats']:
            player['team'] = self.team_abbreviations.get(player['team'], player['team'])
        for player in item['home_defense_stats']:
            player['team'] = self.team_abbreviations.get(player['team'], player['team'])
        for player in item['away_defense_stats']:
            player['team'] = self.team_abbreviations.get(player['team'], player['team'])
        for player in item['home_returns_stats']:
            player['team'] = self.team_abbreviations.get(player['team'], player['team'])
        for player in item['away_returns_stats']:
            player['team'] = self.team_abbreviations.get(player['team'], player['team'])
        return item


class RotoGuruSalaryKeysPipeline:
    """
    A pipeline for correcting salary dictionary keys scraped from RotoGuru.
    """

    key_mapping = {
        'pos': 'position',
        'oppt': 'opponent',
        'dk points': 'points',
        'fd points': 'points',
        'dk salary': 'salary',
        'fd salary': 'salary'
    }

    def process_item(self, item, spider):  # TODO: why doesn't Year key update?
        """
        Normalizes dictionary keys scraped from RotoGuru.

        :param item: the salary item
        :param spider: the salary spider
        :return: the corrected salary item
        """
        for salary in item['salaries']:
            for k, v in salary.items():
                key = k.lower()
                key = self.key_mapping.get(key, key)
                salary[key] = salary.pop(k)
        return item


class RotoGuruTeamAbbreviationPipeline:
    """
    A pipeline used to correct team abbreviations found in RotoGuru.
    """

    team_abbreviations = {
        'GNB': 'GB',
        'KAN': 'KC',
        'LVR': 'LV',
        'NOR': 'NO',
        'NWE': 'NE',
        'SFO': 'SF',
        'TAM': 'TB'
    }

    def process_item(self, item, spider):
        """
        Corrects the RotoGuru team abbreviations for a salary item.

        :param item: the salary item
        :param spider: the salary spider
        :return: the salary item with corrected team abbreviations
        """
        for salary in item['salaries']:
            team = salary['team'].upper()
            opponent = salary['opponent'].upper()
            salary['team'] = self.team_abbreviations.get(team, team)
            salary['opponent'] = self.team_abbreviations.get(opponent, opponent)
        return item


class RotoGuruPlayerNameCorrectionPipeline:
    """
    A pipeline for normalizing and correcting player names found in RotoGuru.
    """

    normalized_names = {

    }

    def process_item(self, item, spider):
        """
        Normalizes and corrects the name for a player in a salary item.

        :param item: the salary item
        :param spider: the salary spider
        :return: the salary item with corrected player name
        """
        for salary in item['salaries']:
            try:
                split_name = salary['name'].split(',')
                normalized_name = f"{split_name[1].strip()} {split_name[0].strip()}"
            except IndexError:  # will occur for defense
                normalized_name = salary['name']
            salary['name'] = self.normalized_names.get(normalized_name, normalized_name)
        return item


class RotoGuruSiteAbbreviationPipeline:
    """
    Converts the RotoGuru site field to its abbreviation.
    """

    site_abbreviations = {
        'DraftKings': 'dk',
        'FanDuel': 'fd'
    }

    def process_item(self, item, spider):
        """
        Converts a salary item's site field to its abbreviation.

        :param item: the salary item
        :param spider: the salary spider
        :return: the salary item with site abbreviation
        """
        item['site'] = self.site_abbreviations.get(item['site'], item['site'])
        return item
