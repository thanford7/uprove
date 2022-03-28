from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from spiders.employer_spiders import *


# process = CrawlerProcess(get_project_settings())
runner = CrawlerRunner(get_project_settings())
spidersToCrawl = [
    Barn2DoorSpider,
    # ZoomoSpider
]

for spider in spidersToCrawl:
    # process.crawl(spider)
    runner.crawl(spider)

d = runner.join()
d.addBoth(lambda _: reactor.stop())

# process.start()
reactor.run()