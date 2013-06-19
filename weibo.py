#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')
from weiboSDK import APIClient

import urlparse
from urllib import urlencode

class Weibo:

  def __init__(self,appKey,appSecret,access_token):
    self.client = APIClient(app_key=appKey,app_secret=appSecret)
    tm = int(time.time()) + 30*86400 
    self.client.set_access_token(access_token,tm)

  def pubHackerFeed(self,item):
    result=urlparse.urlparse(item['link'])
    host = result.netloc	  

    sentToPocket = 'http://getpocket.com/edit?'+urlencode({'url':item['link'],'title':item['title']})
    if len(item['title']) > 70 :
      title = item['title'][0:70]+'...'
    else:
      title = item['title']
    content = item['link'] + ' <'+title + '> ('+ host+')  #hacker news#'+ ' (save to pocket '+sentToPocket+' )'
    res = self.client.statuses.update.post(status = content)
    print res
 
  def pubStartupFeed(self,item):
    sentToPocket = 'http://getpocket.com/edit?'+urlencode({'url':item['link'],'title':item['title']})
    if len(item['title']) > 90 :
      title = item['title'][0:90]+'...'
    else:
      title = item['title']
    content = item['link'] + ' <'+title + '>  #startup news# (save to pocket ' + sentToPocket+' )'
    res = self.client.statuses.update.post(status = content)
    print res
 
