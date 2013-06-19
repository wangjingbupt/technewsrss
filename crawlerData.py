#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')
import feedparser
import gzip, time, hmac, base64, hashlib, urllib, urllib2, logging, mimetypes, collections

_HTTP_GET = 'GET'
_HTTP_POST = 'POST'

class CrawlerData:
  
  def getParseData(self,url): 
    d = feedparser.parse(url)
    items = []
    if 'entries' in d:
      for data in d['entries']:
        item = {'title': data['title'],'link':data['link']}
        items.append(item)

    return items

    
  def _http_call(self,the_url, params = {} , method = _HTTP_GET):
    '''
    send an http request and return a json object if no error occurred.
    '''
    params = self._encode_params(params)
    http_url = '%s?%s' % (the_url, params) if method==_HTTP_GET else the_url
    http_body = None if method==_HTTP_GET else params
    req = urllib2.Request(http_url, data=http_body)
    req.add_header('Accept-Encoding', 'gzip')
    try:
      resp = urllib2.urlopen(req)
      body = self._read_body(resp)
      return body
    except urllib2.HTTPError, e:
      return False 

  def _read_body(self,obj):
    using_gzip = obj.headers.get('Content-Encoding', '')=='gzip'
    body = obj.read()
    if using_gzip:
        logging.info('gzip content received.')
        gzipper = gzip.GzipFile(fileobj=StringIO(body))
        fcontent = gzipper.read()
        gzipper.close()
        return fcontent
    return body

  def _encode_params(self,params):
    args = []
    for k, v in params.iteritems():
        if isinstance(v, basestring):
            qv = v.encode('utf-8') if isinstance(v, unicode) else v
            args.append('%s=%s' % (k, urllib.quote(qv)))
        elif isinstance(v, collections.Iterable):
            for i in v:
                qv = i.encode('utf-8') if isinstance(i, unicode) else str(i)
                args.append('%s=%s' % (k, urllib.quote(qv)))
        else:
            qv = str(v)
            args.append('%s=%s' % (k, urllib.quote(qv)))
    return '&'.join(args)

