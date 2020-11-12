BOT_NAME = 'pygskin'

SPIDER_MODULES = ['pygskin.scrape.spiders']
NEWSPIDER_MODULE = 'pygskin.scrape.spiders'

FEED_FORMAT = 'json'
FEED_EXPORTERS = {
    'json': 'scrapy.exporters.JsonItemExporter'
}
FEED_EXPORT_ENCODING = 'utf-8'
LOG_ENABLED = False
