#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')
from crawlerData import CrawlerData
from mongo import Mongo
from weibo import Weibo
import time

HACKER_NEWS_RSS_URL = 'https://news.ycombinator.com/rss'
STARTUP_NEWS_RSS_URL = 'http://news.dbanotes.net/rss'

CONF = {'host':'127.0.0.1','port':27823}

APP_KEY = '3630429777'
APP_SECRET = '3ea78b0fc46a79184a160e4c2676a431'

TOKEN = '2.00zyFgrDzcugxD252776ad8fvuBiOB'

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
		sys.exit()

  items = cObj.getParseData(STARTUP_NEWS_RSS_URL)
  
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
    wObj.pubStartupFeed(item)
		sys.exit()
  
  

