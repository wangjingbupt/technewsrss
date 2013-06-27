#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')
from crawlerData import CrawlerData
from mongo import Mongo
from weibo import Weibo
from blog import Blog
import time
from urllib import urlencode
from login import Login
from conf import *
import re

import HTMLEntity

HACKER_NEWS_RSS_URL = 'https://news.ycombinator.com/rss'
STARTUP_NEWS_RSS_URL = 'http://news.dbanotes.net/rss'

if __name__ == '__main__':
  lObj = Login()
  cookie = lObj.login(USERNAME,PASSWORD)
  cookie = re.sub('domain.*?[;,]','',cookie)
  cookie = re.sub('[Hh]ttponly,','',cookie)
  cookie = re.sub('path=/;','',cookie)
  cookie +=';'
  

  #print unicode('0x53F6').encode('UTF-8')
  #print unicode('作')
  #sys.exit()
  cObj = CrawlerData()
  mObj = Mongo(CONF)
  wObj = Weibo(APP_KEY , APP_SECRET , TOKEN)
  bObj = Blog(cObj,cookie,wObj)
  print cookie

  #a = wObj.client.short_url.shorten.post(url_long = 'http://www.youku.com/')
  #print a['urls'][0]['url_short']
  #sys.exit()
  #items = cObj.getParseData(HACKER_NEWS_RSS_URL)
  items = cObj.getParseData(STARTUP_NEWS_RSS_URL)
  ss = 1
  
  for item in items:
    ss +=1
    if ss !=6:
      continue
    print item['title']
    print ss
    print item['link']
    url = 'https://www.readability.com/api/content/v1/parser'
    param ={'token':'7b112428b83ae0b3d70d52d13d2787826883dc9d','url':item['link']}
    rs =  cObj._http_call(url,param)
    style="style=\"font-family: 'Microsoft YaHei';font-size:18px;display: block;margin:20px 0;line-height:28px;\""
    style2="style=\"font-family: 'Microsoft YaHei';font-size:26px;display: block;margin:20px 0;line-height:32px;\""
    style3="style=\"font-family: 'Microsoft YaHei';font-size:23px;display: block;margin:20px 0;line-height:28px;\""
    style4="style=\"font-family: 'Microsoft YaHei';font-size:20px;display: block;margin:20px 0;line-height:28px;\""
    c = rs['content']
    c = re.sub('<([a-z ]+)>','<\\1 '+style+' >',c) 
    c = re.sub('<[hH]1>','<h1 '+style2+' >',c) 
    c = re.sub('<[hH]2>','<h2 '+style3+' >',c) 
    c = re.sub('<[hH]3>','<h3 '+style4+' >',c) 
    
    content =  HTMLEntity.decode(c)
    print content
    sys.exit()
    title = item['title']
    item['content'] = content
    #content = '123'
    #title = '123'
    #bObj.pubHackerLongWeibo(item)
    bObj.pubStartupLongWeibo(item)
    sys.exit()
    break
    #res = mObj.checkItemExists(item)
    #print res
    #if not res:
    #  continue
    #item['time'] = time.time() 
    #res = mObj.saveItem(item)
    #print res
    #if not res :
    #  continue
    #wObj.pubHackerFeed(item)
    #sentToPocket = 'http://getpocket.com/edit?'+urlencode({'url':item['link'],'title':item['title']})
    #print sentToPocket
    #sys.exit()
  items = cObj.getParseData(STARTUP_NEWS_RSS_URL)
  #print len(items)
  #sys.exit()
  
  for item in items:
    print len(item['title'])
    print item['title'][0:10]
    break
    #print item
    #res = mObj.checkItemExists(item)
    #print res
    #if not res:
    #  continue
    #item['time'] = time.time() 
    #res = mObj.saveItem(item)
    #print res
    #if not res :
    #  continue
    #wObj.pubStartupFeed(item)
    #sys.exit()
  
  

