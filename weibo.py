#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')
from weiboSDK import APIClient

class Weibo:

  def __init__(self,appKey,appSecret,access_token):
    self.client = APIClient(app_key=appKey,app_secret=appSecret)
    tm = int(time.time()) + 30*86400 
    self.client.set_access_token(access_token,tm)

  def pubFeed(self,item):
    content = item['title']

    res = self.client.statuses.update.post(status = content)
    print res
 
