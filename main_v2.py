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
from login import Login
import time
from conf import *
import HTMLEntity
import re

HACKER_NEWS_RSS_URL = 'https://news.ycombinator.com/rss'
STARTUP_NEWS_RSS_URL = 'http://news.dbanotes.net/rss'


def getContent(cObj,link):

    content = ''
    style="style=\"font-family: 'Microsoft YaHei';font-size:16px;display: block;margin:20px 0;line-height:26px;\""
    style2="style=\"font-family: 'Microsoft YaHei';font-size:24px;display: block;margin:20px 0;line-height:30px;\""
    style3="style=\"font-family: 'Microsoft YaHei';font-size:20px;display: block;margin:20px 0;line-height:26px;\""
    style4="style=\"font-family: 'Microsoft YaHei';font-size:18px;display: block;margin:20px 0;line-height:26px;\""
    style5="style='margin-left: 10px;'"
  
    url = 'https://www.readability.com/api/content/v1/parser'
    param ={'token':READABILITY_TOKEN,'url':link}
    rs =  cObj._http_call(url,param)
    if not rs:
      return False
    if 'content' in rs:
      c = rs['content']
      c = re.sub('<ul.*?>','<ul '+style5+' >',c) 
      c = re.sub('<(div|p|span).*?>','<\\1 '+style+' >',c) 
      c = re.sub('<[hH]1>','<h1 '+style2+' >',c) 
      c = re.sub('<[hH]2>','<h2 '+style3+' >',c) 
      c = re.sub('<[hH]3>','<h3 '+style4+' >',c) 

      content ='<div style="padding:15px;">'+HTMLEntity.decode(c)+'</div>'
    if len(content) < 1000:
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
    if not bObj.pubHackerLongWeibo(item):
      continue
    return True
  return False

def startupNews(cObj,mObj,bObj): 

  items = cObj.getParseData(STARTUP_NEWS_RSS_URL)
  count = 0
  
  for item in items:
    if count > 80:
      break
    count +=1
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
    if not bObj.pubStartupLongWeibo(item):
      continue
    #wObj.pubStartupFeed(item)
    return True
  return False
  
  
if __name__ == '__main__':

  cObj = CrawlerData()
  mObj = Mongo(CONF)
  wObj = Weibo(APP_KEY , APP_SECRET , TOKEN)
  lObj = Login()
  cookie = lObj.login(USERNAME,PASSWORD)
  if not cookie:
    print 'error'
    sys.exit()
  cookie = re.sub('domain.*?[;,]','',cookie)
  cookie = re.sub('[Hh]ttponly,','',cookie)
  cookie = re.sub('path=/;','',cookie)
  cookie +=';'
  print cookie

  
  bObj = Blog(cObj,cookie,wObj)
  fObj = open('/home/erik/technewsrss/flag2','r')
  flag = int(fObj.read().strip())
  if flag < 3:
    if not startupNews(cObj,mObj,bObj):
      hackNews(cObj,mObj,bObj)
    flag += 1
  else:
    if not hackNews(cObj,mObj,bObj):
      startupNews(cObj,mObj,bObj)
    flag = 0
  fObj.close()
  fObj = open('/home/erik/technewsrss/flag2','w')
  fObj.write(str(flag))
  fObj.close()



