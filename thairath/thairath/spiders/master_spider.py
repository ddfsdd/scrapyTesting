# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.utils.project import get_project_settings
# from scrapy.crawler import CrawlerProcess
# from scrapy import spiderloader
#
# from time import sleep
# from scrapy.selector import Selector
# from ..items import ThairathItem
# from urllib.parse import quote
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
#
# class MasterSpider(scrapy.Spider):
#     name = 'master_spider'
#     search_field = "ิ"
#     start_urls = []
#     def start_requests(self):
#         # self points to the spider instance
#         # that was initialized by the scrapy framework when starting a crawl
#         #
#         # spider instances are "augmented" with crawl arguments
#         # available as instance attributes,
#         # self.ip has the (string) value passed on the command line
#         # with `-a ip=somevalue`
#         self.search_field = getattr(self,"search_field","")
#         yield scrapy.Request("http://quotes.toscrape.com", callback=self.parse)
#
#
#     def parse(self, response):
#         setting = get_project_settings()
#         spider_loader = spiderloader.SpiderLoader.from_settings(setting)
#         process = CrawlerProcess(setting)
#         process.crawl("thai_spider", search_field=self.search_field)
#
#         # for spider_name in spider_loader.list():
#         #     print("Running spider %s" % (spider_name))
#         #     process.crawl(spider_name,search_field=self.search_field)
#         process.start()
#
