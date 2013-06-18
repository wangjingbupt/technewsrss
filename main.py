#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')
from crawlerData import CrawlerData
import time

HACKER_NEWS_RSS_URL = 'https://news.ycombinator.com/rss'
STARTUP_NEWS_RSS_URL = 'http://news.dbanotes.net/rss'

if __name__ == '__main__':

  cObj = CrawlerData()
  mObj = Mongo()
  wObj = Weibo()
  items = cObj.getParseData(HACKER_NEWS_RSS_URL)

  for item in items:
    res = mObj.checkItemExists(item)
    if res:
      continue
    item['time'] = time.time() 
    res = mObj.saveItem(item)
    if res :
      continue
    wObj.pubFeed(item)

  

