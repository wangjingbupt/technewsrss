#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')
from crawlerData import CrawlerData
from mongo import Mongo
from weibo import Weibo
import time
from conf import *

HACKER_NEWS_RSS_URL = 'https://news.ycombinator.com/rss'
STARTUP_NEWS_RSS_URL = 'http://news.dbanotes.net/rss'


if __name__ == '__main__':

  cObj = CrawlerData()
  mObj = Mongo(CONF)
  wObj = Weibo(APP_KEY , APP_SECRET , TOKEN)
  items = cObj.getParseData(HACKER_NEWS_RSS_URL)
  
  for item in items:
    print item
    res = mObj.checkItemExists(item)
    print res
    if not res:
      continue
    item['time'] = time.time() 
    res = mObj.saveItem(item)
    print res
    if not res :
      continue
    wObj.pubHackerFeed(item)
    break

  time.sleep(300)
  items = cObj.getParseData(STARTUP_NEWS_RSS_URL)
  count = 0
  
  for item in items:
    if count > 30:
      break
    count +=1
    print item
    res = mObj.checkItemExists(item)
    print res
    if not res:
      continue
    item['time'] = time.time() 
    res = mObj.saveItem(item)
    print res
    if not res :
      continue
    wObj.pubStartupFeed(item)
    break
  
  

