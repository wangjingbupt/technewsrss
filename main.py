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

CONF = {'host':'127.0.0.1','port':27017}

APP_KEY = '703474722'
APP_SECRET = '6514a66788eca2d4ecc214a383121c7d'

TOKEN = ''

if __name__ == '__main__':

  cObj = CrawlerData()
  mObj = Mongo(CONF)
  wObj = Weibo(APP_KEY , APP_SECRET , TOKEN)
  items = cObj.getParseData(HACKER_NEWS_RSS_URL)

  for item in items:
    res = mObj.checkItemExists(item)
    if not res:
      continue
    item['time'] = time.time() 
    res = mObj.saveItem(item)
    if res :
      continue
    wObj.pubFeed(item)

  

