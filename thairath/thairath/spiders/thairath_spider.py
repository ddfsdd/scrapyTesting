# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsItem
from urllib.parse import quote

class ThaiRathSpider(scrapy.Spider):
    name = 'thai_spider'
    search_field = "ิ"
    count_page = 0
    max_page = 5
    start_urls = []
    allowed_domains = ["thairath.co.th"]
    def start_requests(self):
        # self points to the spider instance
        # that was initialized by the scrapy framework when starting a crawl
        #
        # spider instances are "augmented" with crawl arguments
        # available as instance attributes,
        # self.ip has the (string) value passed on the command line
        # with `-a ip=somevalue`
        self.search_field = getattr(self,"search_field","")

        yield scrapy.Request('https://www.thairath.co.th/search?q='+quote(self.search_field)+'&p=1', callback=self.parse)
    def parse(self, response):
        content_page = response.css(".col-8 a").css("::attr(href)").extract()
        for page in content_page:
            yield scrapy.Request(page, callback= self.parse_item)
        self.count_page +=1
        print("\n")
        next_page = "https://www.thairath.co.th/search?q=" +quote(self.search_field)+'&p='+str(self.count_page+1)
        if self.count_page < self.max_page:
            print(next_page)
            print(self.count_page)
            yield scrapy.Request(next_page, callback= self.parse)


    def parse_item(self, response):
        items = NewsItem()
        title = response.css(".e1ui9xgn0::text").extract_first()
        author = response.css(".e1ui9xgn1 a").css("::text").extract_first()
        date = response.css(".e1ui9xgn2::text").extract_first()
        body = response.css("p , strong").css("::text").extract()
        bodytext = ""
        for paragraph in body:
            bodytext += paragraph + " /p "
        bodytext.strip()
        tags = response.css(".evs3ejl15 a").css("::text").extract()
        url = response.request.url
        items['title'] = title
        items['author'] = author
        items['date'] = date
        items['body'] = bodytext
        items['tags'] = tags
        items['url'] = url
        yield items

