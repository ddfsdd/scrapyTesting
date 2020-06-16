import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy import spiderloader
import sys

setting = get_project_settings()
spider_loader = spiderloader.SpiderLoader.from_settings(setting)
process = CrawlerProcess(setting)

for spider_name in spider_loader.list():
    print("Running spider %s" % (spider_name))
    print(spider_name)
    process.crawl(spider_name,search_field=sys.argv[1])
process.start()