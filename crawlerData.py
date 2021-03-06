#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')
import feedparser
import gzip, time, hmac, base64, hashlib, urllib, urllib2, logging, mimetypes, collections
from urllib2 import Request, urlopen, URLError, HTTPError

try:
    import json
except ImportError:
    import simplejson as json

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

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

  def _http_call_set_cookie(self,the_url, params = {} , method = _HTTP_GET , header = {}):

    params = self._encode_params(params)
    http_url = '%s?%s' % (the_url, params) if method==_HTTP_GET else the_url
    http_body = None if method==_HTTP_GET else params
    req = urllib2.Request(http_url, data=http_body)
    for k,v in header.iteritems():
      req.add_header(k, v)
    try:
      resp = urllib2.urlopen(req)
      try:
        setCookie = resp.info().getheader('set-Cookie')
      except:
        setCookie = ''
      return setCookie
    except urllib2.HTTPError, e:
      return False 

    
  def _http_call(self,the_url, params = {} , method = _HTTP_GET , header = {},timeout=20):
    '''
    send an http request and return a json object if no error occurred.
    '''
    params = self._encode_params(params)
    http_url = '%s?%s' % (the_url, params) if method==_HTTP_GET else the_url
    http_body = None if method==_HTTP_GET else params
    req = urllib2.Request(http_url, data=http_body)
    #req.add_header('Accept-Encoding', 'gzip')
    for k,v in header.iteritems():
      req.add_header(k, v)
    try:
      resp = urllib2.urlopen(req,timeout=timeout)
      body = self._read_body(resp)
      try:
        r = json.loads(body)
      except:
        r = body
      return r
    except:
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


