#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')
import feedparser

class CrawlerData:
  
  def getParseData(self,url): 
    d = feedparser.parse(url)
    items = []
    if 'entries' in d:
      for data in d['entries']
        item = {'title': data['title'],'link':data['title']}
        items.append(item)

    return items

    
