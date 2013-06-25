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
    return True
  return False

def startupNews(cObj,mObj,wObj): 

  items = cObj.getParseData(STARTUP_NEWS_RSS_URL)
  count = 0
  
  for item in items:
    #if count > 100:
    #  break
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
    return True
  return False
  
  
if __name__ == '__main__':

  cObj = CrawlerData()
  mObj = Mongo(CONF)
  wObj = Weibo(APP_KEY , APP_SECRET , TOKEN)
  fObj = open('/home/erik/technewsrss/flag','r')
  flag = int(fObj.read().strip())
  if flag == 1:
    if not startupNews(cObj,mObj,wObj):
      hackNews(cObj,mObj,wObj)
    flag = 0
  else:
    if not hackNews(cObj,mObj,wObj):
      startupNews(cObj,mObj,wObj)
    flag = 1
  fObj.close()
  fObj = open('/home/erik/technewsrss/flag','w')
  fObj.write(str(flag))
  fObj.close()



