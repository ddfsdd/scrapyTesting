# import scrapy
#
# from ..items import NewsItem
# from urllib.parse import quote
#
# # import items.py class for data storage
#
# # as the class Khaosod2 gets inheritance from scrapy.Spider, some basic things are inherited.
# # variable: name, start_urls, and parse cannot be changed, as scrapy expects it.
#
#
# class Khaosod2Spider(scrapy.Spider):
#     name = 'khaosod_spider'
#     # name of the bot to be used in the run(crawl) command
#     # start_urls should be the home or the front page in case of multiple pages scrapping
#
#     s_key = "ทักษิณ"
#     # search key
#
#     # currently, khaosod has no pages
#     # page_number = 2
#     allowed_domains = ["khaosod.co.th"]
#
#     def start_requests(self):
#         # self points to the spider instance
#         # that was initialized by the scrapy framework when starting a crawl
#         #
#         # spider instances are "augmented" with crawl arguments
#         # available as instance attributes,
#         # self.ip has the (string) value passed on the command line
#         # with `-a ip=somevalue`
#         self.search_field = getattr(self, "search_field", "")
#         yield scrapy.Request("https://www.khaosod.co.th/search?s=" + quote(self.search_field), callback=self.parse)
#
#     def parse(self, response):
#         # the variable response contains the source code of the web
#
#         search_results = response.css("div.ud-search__context")
#
#         first_news = search_results.css("div.col-12").css("a.udblock__permalink::attr(href)").get()
#         # select div with class = "col-12" find a class, get href
#
#         yield response.follow(first_news, callback=self.parse_indivnews)
#         # follow the link
#
#         col8news = search_results.css("div.col-md-8 div.udblock.udblock--left_right")
#
#         for indivnews in col8news:
#             indivlink = indivnews.css("a.udblock__permalink::attr(href)").get()
#             yield response.follow(indivlink, callback=self.parse_indivnews)
#
#     def parse_indivnews(self, response):
#         # the variable response contains the source code of the web
#
#         items = NewsItem()
#
#         main_content = response.css("main.content")
#         # extract from the response, find css part of the response, find main content
#
#         headlines = main_content.css("div.container.ud-padding")
#         # find div with class = "container ud-padding"
#
#         # title1 = response.css("main.content").css("span.ud-bh__suffix::text").extract()
#         title = headlines.css("h1.udsg__main-title::text").extract_first()
#
#         date = headlines.css("div.udsg__meta-wrap")[1].css("div.udsg__meta-left span.udsg__meta::text").extract()
#         # find the second udsg__meta-wrap for the date
#
#         appendeddate = ""
#         for i in date:
#             appendeddate = appendeddate + str(i)
#
#         bodyall = main_content.css("div.ud_ads_sticky__container").css("div.udsg__content")
#         newsbody = bodyall.css("p, em, strong, blockquote").css("::text").extract()
#         bodytext = ""
#         for paragraph in newsbody:
#             # bodytext += paragraph + " /p "
#             bodytext += paragraph + " "
#         bodytext.strip()
#         tags = main_content.css("li.udsg__tag-item a.udsg__tag-link::text").extract()
#
#         url = response.request.url
#
#         # khaosod doesn't specify author
#         author = '-'
#
#         items['title'] = title
#         items['date'] = appendeddate
#         items['body'] = bodytext
#         items['tags'] = tags
#         items['author'] = "khaosod"
#         items['url'] = url
#         yield items
#
#
#         # search_context = response.css("div.ud-search__context")
#         # code_in_box = search_context.css("div.ud-search__context")
#         # get the html code in the quote box
#         # yield {
#         #     'titletext': title,
#         #     'date': appendeddate,
#         #     'body': bodytext,
#         #     'tag': tags,
#         #     'url': url
#         # }
#         # to output into csv file, there must be only one yield command
