# -*- coding: utf-8 -*-
import scrapy
from time import sleep
from scrapy.selector import Selector
from ..items import NewsItem
from urllib.parse import quote
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class Ch3Spider(scrapy.Spider):
    name = 'ch3_spider'
    search_field = "ิ"
    count_page = 0
    max_page = 5
    start_urls = []
    allowed_domains = ["news.ch3thailand.com"]
    def start_requests(self):
        # self points to the spider instance
        # that was initialized by the scrapy framework when starting a crawl
        #
        # spider instances are "augmented" with crawl arguments
        # available as instance attributes,
        # self.ip has the (string) value passed on the command line
        # with `-a ip=somevalue`
        self.search_field = getattr(self,"search_field","")
        yield scrapy.Request("https://www.ch3thailand.com/search?q=" + quote(self.search_field), callback=self.parse)


    def parse(self, response):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
        driver.get("https://www.ch3thailand.com/search?q=" + quote(self.search_field))
        self.count_page += 1
        while self.count_page < self.max_page:
            self.count_page += 1
            scrapy_selector = Selector(text=driver.page_source)
            content_page = scrapy_selector.css('.gs-title::attr(href)').extract()
            # for page in content_page:
            #     yield scrapy.Request(page, callback=self.parse_item)
            next_page = driver.find_elements_by_css_selector("div[aria-label='หน้า " + str(self.count_page) + "']")
            if len(next_page) == 0:
                return
            next_page[0].click()
            print(self.count_page)
            sleep(5)
        driver.close()

    def parse_item(self, response):
        items = NewsItem()
        title = response.css(".content-head::text").extract_first()
        if title is None:
            return
        print(title)
        author = "ch3"
        date = response.css(".content-des-text:nth-child(2)::text").extract_first()
        body = response.css(".content-news").css("::text").extract()
        bodytext = ""
        for paragraph in body:
            bodytext += paragraph + " /p "
        bodytext.strip()
        tags = response.css(".content-tag-click").css("::text").extract()
        print(tags)
        print("\n")
        url = response.request.url
        items['title'] = title
        items['author'] = author
        items['date'] = date
        items['body'] = bodytext
        items['tags'] = tags
        items['url'] = url
        yield items

