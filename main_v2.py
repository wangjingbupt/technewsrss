#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')
from crawlerData import CrawlerData
from mongo import Mongo
from weibo import Weibo
from blog import Blog
from urllib import urlencode
import time
from conf import *
import HTMLEntity

HACKER_NEWS_RSS_URL = 'https://news.ycombinator.com/rss'
STARTUP_NEWS_RSS_URL = 'http://news.dbanotes.net/rss'


def getContent(cObj,link):

    content = ''
  
    url = 'https://www.readability.com/api/content/v1/parser'
    param ={'token':'7b112428b83ae0b3d70d52d13d2787826883dc9d','url':link}
    rs =  cObj._http_call(url,param)
    if not rs:
      return False
    if 'content' in rs:
      content =  HTMLEntity.decode(rs['content'])
    if len(content) < 200:
      return False

    return content

def hackNews(cObj,mObj,bObj): 
  items = cObj.getParseData(HACKER_NEWS_RSS_URL)
  for item in items:
    res = mObj.checkItemExists(item)
    if not res:
      continue
    content = getContent(cObj,item['link'])
    if not content:
      continue
    item['time'] = time.time() 
    res = mObj.saveItem(item)
    if not res :
      continue
    #wObj.pubHackerFeed(item)
    item['content'] = content
    bObj.pubHackerLongWeibo(item)
    return True
  return False

def startupNews(cObj,mObj,bObj): 

  items = cObj.getParseData(STARTUP_NEWS_RSS_URL)
  
  for item in items:
    res = mObj.checkItemExists(item)
    if not res:
      continue
    content = getContent(cObj,item['link'])
    if not content:
      continue
    item['time'] = time.time() 
    res = mObj.saveItem(item)
    if not res :
      continue
    item['content'] = content
    bObj.pubStartupLongWeibo(item)
    #wObj.pubStartupFeed(item)
    return True
  return False
  
  
if __name__ == '__main__':

  cObj = CrawlerData()
  mObj = Mongo(CONF)
  wObj = Weibo(APP_KEY , APP_SECRET , TOKEN)
  bObj = Blog(cObj,LOGIN_COOKIE,wObj)
  fObj = open('/home/erik/technewsrss/flag2','r')
  flag = int(fObj.read().strip())
  if flag == 1:
    if not startupNews(cObj,mObj,bObj):
      hackNews(cObj,mObj,bObj)
    flag = 0
  else:
    if not hackNews(cObj,mObj,bObj):
      startupNews(cObj,mObj,bObj)
    flag = 1
  fObj.close()
  fObj = open('/home/erik/technewsrss/flag2','w')
  fObj.write(str(flag))
  fObj.close()



