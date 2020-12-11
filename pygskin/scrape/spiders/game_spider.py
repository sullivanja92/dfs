from datetime import datetime
from string import Template
from typing import Dict, List

import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import Selector

from pygskin.scrape.items import GameItem

GAME_URL_XPATH_TEMPLATE = Template('//h2[contains(text(),"$year Week $week")]/parent::*/following-sibling::div[@class="game_summaries"]//a[contains(@href,"boxscores")]/@href')
HOME_TEAM_XPATH = '(//a[@itemprop="name"]/@href)[1]'
AWAY_TEAM_XPATH = '(//a[@itemprop="name"]/@href)[2]'
HOME_SCORE_XPATH = '(//div[@class="score"]/text())[1]'
AWAY_SCORE_XPATH = '(//div[@class="score"]/text())[2]'
DATE_XPATH = '//div[@class="scorebox_meta"]/div/text()'
TIME_XPATH = '//div[@class="scorebox_meta"]/div[2]/text()'
DATETIME_FORMAT = '%A %b %d, %Y %I:%M%p'
HOME_PASSING_RUSHING_RECEIVING_ROWS_XPATH = \
    '//table[@id="player_offense"]/tbody/tr[contains(@class,"over_header")]/following-sibling::tr[not(@class="thead")]'
AWAY_PASSING_RUSHING_RECEIVING_ROWS_XPATH = \
    '//table[@id="player_offense"]/tbody/tr[contains(@class,"over_header")]/preceding-sibling::tr'
HOME_DEFENSE_ROWS_XPATH = \
    '//table[@id="player_defense"]/tbody/tr[contains(@class,"over_header")]/following-sibling::tr[not(@class="thead")]'
AWAY_DEFENSE_ROWS_XPATH = \
    '//table[@id="player_defense"]/tbody/tr[contains(@class,"over_header")]/preceding-sibling::tr'
HOME_RETURNS_ROWS_XPATH = \
    '//table[@id="returns"]/tbody/tr[contains(@class,"over_header")]/following-sibling::tr[not(@class="thead")]'
AWAY_RETURNS_ROWS_XPATH = \
    '//table[@id="returns"]/tbody/tr[contains(@class,"over_header")]/preceding-sibling::tr'
HOME_SNAP_COUNTS_ROWS_XPATH = '//table[@id="home_snap_counts"]/tbody/tr[not(contains(@class,"thead"))]'
AWAY_SNAP_COUNTS_ROWS_XPATH = '//table[@id="vis_snap_counts"]/tbody/tr[not(contains(@class,"thead"))]'
HOME_DRIVES_TABLE_XPATH = '//table[@id="home_drives"]'
AWAY_DRIVES_TABLE_XPATH = '//table[@id="vis_drives"]'


class GameSpider(scrapy.Spider):
    """
    A scrapy spider to scrape NFL game statistics from Pro Football Reference (PFR).
    """

    name = 'game'
    allowed_domains = ['pro-football-reference.com']
    download_delay = 1
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_EXPORTERS': {
            'json': 'scrapy.exporters.JsonItemExporter'
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_ENABLED': False,
        'FEED_URI': '%(directory)s/GAMES_%(year)s_%(week)s.json',
        'ITEM_PIPELINES': {
            'pygskin.scrape.pipelines.PFRTeamAbbreviationPipeline': 100
        }
    }

    def __init__(self, year: int, week: int, directory: str, **kwargs):
        """
        :param year: the year of the games to scrape
        :param week: the week number to scrape
        :param directory: the directory to save json output to
        :param kwargs: keyword arguments
        """
        self.year = year
        self.week = week
        self.directory = directory
        self.start_urls = [f"https://www.pro-football-reference.com/years/{year}/week_{week}.htm"]
        super().__init__(**kwargs)

    def parse(self, response: HtmlResponse, **kwargs):
        """
        Parses initial PFR week page.

        :param response: the week page html response
        :param kwargs: keyword arguments
        :return: additional requests for each game in the week
        """
        for game_url in response.xpath(GAME_URL_XPATH_TEMPLATE.substitute({'year': self.year, 'week': self.week})).getall():
            yield scrapy.Request(response.urljoin(game_url), callback=parse_game)


def parse_game(response: HtmlResponse) -> GameItem:
    """
    Parses a PFR game html response.

    :param response: the game page html response
    :return: a GameItem containing parsed fields
    """
    item = GameItem()
    item['url'] = response.url
    item['home_team'] = response.xpath(HOME_TEAM_XPATH).get().split('/')[2].upper().strip()
    item['away_team'] = response.xpath(AWAY_TEAM_XPATH).get().split('/')[2].upper().strip()
    item['home_score'] = int(response.xpath(HOME_SCORE_XPATH).get().strip())
    item['away_score'] = int(response.xpath(AWAY_SCORE_XPATH).get().strip())
    date = response.xpath(DATE_XPATH).get().strip()
    time = response.xpath(TIME_XPATH).get().split(' ')[1].strip()
    item['datetime'] = datetime.strptime(f"{date} {time}".replace('am', 'AM').replace('pm', 'PM'), DATETIME_FORMAT)
    item['home_offense_stats'] = _process_player_stats_rows(response.xpath(HOME_PASSING_RUSHING_RECEIVING_ROWS_XPATH))
    item['away_offense_stats'] = _process_player_stats_rows(response.xpath(AWAY_PASSING_RUSHING_RECEIVING_ROWS_XPATH))
    item['home_defense_stats'] = []
    item['away_defense_stats'] = []
    item['home_returns_stats'] = []
    item['away_returns_stats'] = []
    item['home_snap_counts'] = []
    item['away_snap_counts'] = []
    for comment in response.xpath('//comment()'):  # process comments which include some tables
        comment_html = comment.get().replace('<!--', '').replace('-->', '')
        selector = scrapy.Selector(text=comment_html)
        if len(selector.xpath(HOME_DEFENSE_ROWS_XPATH)) > 0:
            item['home_defense_stats'] = _process_player_stats_rows(selector.xpath(HOME_DEFENSE_ROWS_XPATH))
        if len(selector.xpath(AWAY_DEFENSE_ROWS_XPATH)) > 0:
            item['away_defense_stats'] = _process_player_stats_rows(selector.xpath(AWAY_DEFENSE_ROWS_XPATH))
        if len(selector.xpath(HOME_RETURNS_ROWS_XPATH)) > 0:
            item['home_returns_stats'] = _process_player_stats_rows(selector.xpath(HOME_RETURNS_ROWS_XPATH))
        if len(selector.xpath(AWAY_RETURNS_ROWS_XPATH)) > 0:
            item['away_returns_stats'] = _process_player_stats_rows(selector.xpath(AWAY_RETURNS_ROWS_XPATH))
        if len(selector.xpath(HOME_SNAP_COUNTS_ROWS_XPATH)) > 0:
            item['home_snap_counts'] = _process_player_stats_rows(selector.xpath(HOME_SNAP_COUNTS_ROWS_XPATH))
        if len(selector.xpath(AWAY_SNAP_COUNTS_ROWS_XPATH)) > 0:
            item['away_snap_counts'] = _process_player_stats_rows(selector.xpath(AWAY_SNAP_COUNTS_ROWS_XPATH))
        home_drives_table = selector.xpath(HOME_DRIVES_TABLE_XPATH)
        if len(home_drives_table) > 0:
            item['home_drives'] = _process_table(home_drives_table)
        away_drives_table = selector.xpath(AWAY_DRIVES_TABLE_XPATH)
        if len(away_drives_table) > 0:
            item['away_drives'] = _process_table(away_drives_table)
    yield item


def _process_player_stats_rows(rows: List) -> List[Dict[str, str]]:
    """
    Processes a PFR player stats row and returns a list of dicts representing each row.

    :param rows: the stats rows
    :return: a list of row dicts
    """
    if len(rows) == 0:
        return []
    stats = []
    for row in rows:
        stat_dict = dict()
        cells = row.xpath('./*[@data-stat]')
        for cell in cells:
            stat = cell.xpath('@data-stat').get()
            tag = cell.xpath('name()').get()
            value = cell.xpath('./a/text()').get().strip() if tag == 'th' else cell.xpath('text()').get()
            if stat == 'player':
                stat = 'name'
            stat_dict[stat] = value
        stats.append(stat_dict)
    return stats


def _process_table(table: Selector) -> List[Dict[str, str]]:
    """
    Processes a PFR table and returns a list of dicts.

    :param table: the PFR table
    :return: a list of row dicts
    """
    rows = []
    for tr in table.xpath('//tbody/tr'):
        row = dict()
        for cell in tr.xpath('./*[@data-stat]'):
            row[cell.xpath('@data-stat').get()] = cell.xpath('./text()').get()
        rows.append(row)
    return rows
