import json
from typing import Tuple

import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from pygskin import file_utils
from pygskin.scrape.spiders.game_spider import GameSpider
from pygskin.scrape.spiders.salary_spider import SalarySpider


def scrape_week(year: int, week: int, directory: str) -> Tuple[str, str]:
    """
    Scrapes NFL stats and fantasy information for a given week and saves to file.
    This function scrapes both PFR and RG, saving output to separate json files.

    :param year: the year of the week to scrape
    :param week: the week number to scrape
    :param directory: the directory to save the file to
    :return: a tuple containing game file path and salary file path
    :raises: ValueError if the directory does not exist
    """
    if not file_utils.dir_exists(directory):
        raise ValueError(f"The directory does not exist: {directory}")
    games_file_path = f"{directory}/GAMES_{year}_{week}.json"
    salaries_file_path = f"{directory}/SALARIES_{year}_{week}.json"
    file_utils.try_remove_file(games_file_path)
    file_utils.try_remove_file(salaries_file_path)
    process = CrawlerProcess(get_project_settings())
    process.crawl(SalarySpider, year=year, week=week, directory=directory)
    process.crawl(GameSpider, year=year, week=week, directory=directory)
    process.start()
    return games_file_path, salaries_file_path


def parse_scraped_week_to_data_frame(games_file: str, salary_file: str) -> pd.DataFrame:
    """
    Parses a json file containing scraped NFL information to a pandas DataFrame.

    :param games_file: the path to the scraped games json file
    :param salary_file: the path to the scraped salary json file
    :return: a pandas DataFrame
    :raises: ValueError if the file does not exist
    """
    if not file_utils.file_exists(salary_file):
        raise ValueError(f"The file at {salary_file} does not exist")
    players_dict = {}
    with open(salary_file, mode='r') as f:
        salary_json = json.load(f)
        for site in salary_json:
            name = site['site']
            for salary in site['salaries']:
                salary['year'] = salary.pop('Year')  # TODO: remove this once key pipeline is fixed
                salary[f"{name.lower()}_points"] = salary.pop('points')
                salary[f"{name.lower()}_salary"] = salary.pop('salary')
                key = f"{salary['name']}|{salary['team']}|{salary['position']}"
                if key in players_dict:
                    players_dict[key].update(salary)
                else:
                    players_dict[key] = salary
    data = pd.DataFrame(data=list(players_dict.values()))
    data['week'] = pd.to_numeric(data['week'])
    data['year'] = pd.to_numeric(data['year'])
    data['fd_points'] = pd.to_numeric(data['fd_points'])
    data['dk_points'] = pd.to_numeric(data['dk_points'])
    data['fd_salary'] = pd.to_numeric(data['fd_salary'])
    data['dk_salary'] = pd.to_numeric(data['dk_salary'])
    return data


def scrape_and_parse_week_to_data_frame(year, week, directory):
    """
    Scrapes NFL stats and fantasy information for a given week, then parses it and returns a pandas DataFrame.
    This function acts as a convenience method of calling both scrape_week and parse_scraped_week_to_data_frame.

    :param year: the year of the week to scrape
    :param week: the week number to scrape
    :param directory: the directory to save the scraped json file to
    :return: a pandas DataFrame
    """
    game_file, salary_file = scrape_week(year, week, directory)
    return parse_scraped_week_to_data_frame(game_file, salary_file)


print(scrape_and_parse_week_to_data_frame(2020, 1, '/users/joshsullivan').head(n=5))
