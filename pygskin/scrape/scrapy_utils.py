from multiprocessing import Process, Queue
from typing import Type

from scrapy import crawler, Spider
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor


def run_spider(spider: Type[Spider], **kwargs) -> None:
    """
    Runs a scrapy spider with optional keyword arguments.
    Running spiders via this method will avoid ReactorNotRestartable errors.

    :param spider: the spider to run.
    :param kwargs: keyword arguments to provide.
    :return:
    """
    def f(queue: Queue):
        try:
            runner = crawler.CrawlerRunner(get_project_settings())
            deferred = runner.crawl(spider, **kwargs)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            queue.put(e)
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()
    if result is not None:
        raise result
