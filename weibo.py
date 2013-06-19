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
    content = item['link'] + ' <'+item['title'] + '> ('+ host+')  #hacker news#'+ ' (save to pocket '+sentToPocket+' )'
    res = self.client.statuses.update.post(status = content)
    print res
 
  def pubStartupFeed(self,item):
    sentToPocket = 'http://getpocket.com/edit?'+urlencode({'url':item['link'],'title':item['title']})
    content = item['link'] + ' <'+item['title'] + '>  #startup news# (save to pocket ' + sentToPocket+' )'
    res = self.client.statuses.update.post(status = content)
    print res
 
