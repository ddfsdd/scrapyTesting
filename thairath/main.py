import scrapy
from scrapy.utils.project import get_project_settings
# from scrapy.crawler import CrawlerProcess
from scrapy import spiderloader
import sys
# from thairath.middlewares import wordCounter
from thairath.middlewares import wordSet
from collections import Counter
import scrapy.crawler as crawler
from multiprocessing import Process, Queue, Manager
from twisted.internet import reactor

from pythainlp.util import isthai
def run_spider(spider,setting, search_value, alreadyUsedWordList, notYetUsedWordList):
    def f(q,alreadyUsedWordList, notYetUsedWordList):
        try:
            runner = crawler.CrawlerRunner(setting)
            deferred = runner.crawl(spider, search_field= search_value)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            print('In multi')
            print(wordSet)
            for word in wordSet:
                if word not in alreadyUsedWord and word not in notYetUsedWord:
                    notYetUsedWord.append(word)
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,alreadyUsedWordList, notYetUsedWordList))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

setting = get_project_settings()
spider_loader = spiderloader.SpiderLoader.from_settings(setting)
# process = CrawlerProcess(setting)
alreadyUsedWord = Manager().list()
notYetUsedWord = Manager().list()
iterations = 2
roundCount = 0
search_field=sys.argv[1]

while roundCount<iterations:
    alreadyUsedWord.append(search_field)
    # for spider_name in spider_loader.list():
    #     print("Running spider %s" % (spider_name))
    #     print(spider_name)
    #     run_spider(spider_name,setting,search_field,alreadyUsedWord, notYetUsedWord)
    run_spider('thai_spider', setting, search_field, alreadyUsedWord, notYetUsedWord)
        # process.crawl(spider_name,search_field=search_field)
    # process.start()

    roundCount += 1

    if len(notYetUsedWord) == 0:
        break
    search_field = notYetUsedWord.pop()
    print('new search field is' + search_field)
    print(alreadyUsedWord)
    print(notYetUsedWord)

