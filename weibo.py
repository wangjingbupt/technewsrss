#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')
from weiboSDK import APIClient

import urlparse

class Weibo:

  def __init__(self,appKey,appSecret,access_token):
    self.client = APIClient(app_key=appKey,app_secret=appSecret)
    tm = int(time.time()) + 30*86400 
    self.client.set_access_token(access_token,tm)

  def pubHackerFeed(self,item):
    result=urlparse.urlparse(item['link'])
    host = result.netloc	  
    content = item['link'] + ' <'+item['title'] + '> ('+ host+')  #hacker news#'
    res = self.client.statuses.update.post(status = content)
    print res
 
  def pubStartupFeed(self,item):
    content = item['link'] + ' <'+item['title'] + '>  #startup news#'
    res = self.client.statuses.update.post(status = content)
    print res
 
