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


def hackNews(cObj,mObj,wObj): 
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


def startupNews(cObj,mObj,wObj): 

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
    sys.exit()
  
  
if __name__ == '__main__':

  cObj = CrawlerData()
  mObj = Mongo(CONF)
  wObj = Weibo(APP_KEY , APP_SECRET , TOKEN)
  fObj = open('flag','r')
  flag = int(fObj.read().strip())
  if flag == 1:
    startupNews(cObj,mObj,wObj)
    hackNews(cObj,mObj,wObj)
    flag = 0
  else:
    hackNews(cObj,mObj,wObj)
    startupNews(cObj,mObj,wObj)
    flag = 1
  fObj.close()
  fObj = open('flag','w')
  fObj.write(str(flag))
  fObj.close()



