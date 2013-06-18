#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')
import pymongo

class Mongo:
  def __init__(self,conf):
    host = conf['host']
    port = conf['port']
    self.conn = pymongo.Connection(host, port)
    self.db = self.conn.tech_new

  def checkItemExists(item):
    if not self.db:
      return False
    
    doc = self.db.info.find_one({'link':item['link']}) 
    if doc:
      return False

    return True

  def saveItem(item):
    if not self.db:
      return False
 
    res = self.db.info.insert(item)
    if res:
      return True

    return False


