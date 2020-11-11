import scrapy
from scrapy.http.response.html import HtmlResponse

from pygskin.scrape.items import SalaryItem


class SalarySpider(scrapy.Spider):
    """
    A scrapy spider for scraping NFL DFS salaries from RotoGuru for a given week.
    """

    name = 'salary'
    allowed_domains = ['rotoguru1.com']
    download_delay = 1
    custom_settings = {
        'FEED_URI': '%(directory)s/SALARIES_%(year)s_%(week)s.json',
        'ITEM_PIPELINES': {
            'pygskin.scrape.pipelines.RotoGuruSalaryKeysPipeline': 100,
            'pygskin.scrape.pipelines.RotoGuruTeamAbbreviationPipeline': 200,
            'pygskin.scrape.pipelines.RotoGuruPlayerNameCorrectionPipeline': 300,
            'pygskin.scrape.pipelines.RotoGuruSiteAbbreviationPipeline': 400
        }
    }

    def __init__(self, year: int, week: int, directory: str, **kwargs):
        """
        :param year: the year of the week to scrape
        :param week: the week number to scrape
        :param directory: the directory to save json output to
        :param kwargs: keyword arguments
        """
        self.year = year
        self.week = week
        self.directory = directory
        self.start_urls = [
            f"http://rotoguru1.com/cgi-bin/fyday.pl?year={year}&week={week}&game=dk&scsv=1",
            f"http://rotoguru1.com/cgi-bin/fyday.pl?year={year}&week={week}&game=fd&scsv=1"
        ]
        super().__init__(**kwargs)

    def parse(self, response: HtmlResponse, **kwargs):
        """
        Yields scrapy requests for each fantasy site to scrape (DK, FD, etc.).

        :param response: the html response
        :param kwargs: keyword arguments
        :return: a scrapy request for each fantasy site
        """
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_salary_page)

    def parse_salary_page(self, response: HtmlResponse):
        """
        Parses a RotoGuru salary page for a given week and DFS site, returning a SalaryItem.

        :param response: the DFS salary page
        :return: a SalaryItem containing scraped fields
        """
        item = SalaryItem()
        item['url'] = response.url
        item['year'] = self.year
        item['week'] = self.week
        item['site'] = response.xpath('//font[@size="+2"]/text()[2]').get().split(' ')[0].strip()
        salaries = []
        lines = response.xpath('//pre/text()').get().strip().split('\n')
        header = lines[0].split(';')
        for i in range(1, len(lines)):
            salary = {}
            split_line = lines[i].split(';')
            for j in range(len(header)):
                salary[header[j]] = split_line[j]
            salaries.append(salary)
        item['salaries'] = salaries
        yield item
