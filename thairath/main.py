import scrapy
from scrapy.utils.project import get_project_settings
# from scrapy.crawler import CrawlerProcess
from scrapy import spiderloader
import sys
from thairath.middlewares import wordCounter
from collections import Counter
import scrapy.crawler as crawler
from multiprocessing import Process, Queue, Manager
from twisted.internet import reactor
from ctypes import c_char_p
from pythainlp.util import isthai
def run_spider(spider,setting, search_value, alreadyUsedWordList, new_field):
    def f(q,alreadyUsedWordList, new_field):
        try:
            runner = crawler.CrawlerRunner(setting)
            deferred = runner.crawl(spider, search_field= search_value)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            print('In multi')
            print(wordCounter)

            i = 0
            if len(wordCounter)>0:
                while i <= len(wordCounter):
                    i += 1
                    wordSelected = wordCounter.most_common()[len(wordCounter) - i][0]
                    if wordSelected not in alreadyUsedWordList and isthai(wordSelected):
                        print('not all words are used')
                        new_field.value = wordSelected
                        print(new_field.value)
                        break
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,alreadyUsedWordList, new_field))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

setting = get_project_settings()
spider_loader = spiderloader.SpiderLoader.from_settings(setting)
# process = CrawlerProcess(setting)
alreadyUsedWord = Manager().list()
iterations = 20
roundCount = 0
search_field=sys.argv[1]
new_field = Manager().Value(c_char_p,search_field)
while roundCount<iterations:
    alreadyUsedWord.append(search_field)
    for spider_name in spider_loader.list():
        print("Running spider %s" % (spider_name))
        print(spider_name)
        run_spider(spider_name,setting,search_field,alreadyUsedWord,new_field)
        # process.crawl(spider_name,search_field=search_field)
    # process.start()

    roundCount += 1
    print('new search field is' + new_field.value)
    search_field = new_field.value

