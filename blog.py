#!/usr/bin/python
# encoding=utf8 
import sys,time
reload(sys)
sys.setdefaultencoding('utf-8')

import urlparse
from urllib import urlencode

class Blog:

  def __init__(self,cObj,cookie,wObj):
    self.cookie = cookie
    self.cObj = cObj
    self.wObj = wObj
    self.header ={}
    self.header2 ={}
    self._initHeader()

  def _initHeader(self):
    self.header['User-Agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11' 
    self.header2['User-Agent']='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.101 Safari/537.11' 
    self.header['Referer']='http://control.blog.sina.com.cn/admin/article/changWeiBo.php'
    self.header2['Referer']='http://c.blog.sina.com.cn/cblog.php'
    self.header['Origin']='http://control.blog.sina.com.cn'
    self.header2['Origin']='http://c.blog.sina.com.cn'
    self.header['Host'] ='control.blog.sina.com.cn'
    self.header2['Host'] ='c.blog.sina.com.cn'

  def pubHackerLongWeibo(self,item):
    result=urlparse.urlparse(item['link'])
    host = result.netloc	  

    title = item['title']
    content = item['content']

    sentToPocket = 'http://getpocket.com/edit?'+urlencode({'url':item['link'],'title':item['title']})
    tempUrl = self.getShortUrl(sentToPocket)
    if tempUrl:
      sentToPocket = tempUrl
    print sentToPocket
    if len(title) > 55 :
      weiboTitle = title[0:55]+'...'
    else:
      weiboTitle = title
    weiboContent1 = '<'+weiboTitle+ '> ('+ host+') 阅读全文: '
    weiboContent2 = '  #hacker news# 原文地址: '+ item['link'] + ' (save to pocket '+sentToPocket+' )'
    return self._pubLongWeibo(title,content,item['link'],weiboContent1,weiboContent2)

  def getShortUrl(self,surl):
     
    rs = self.wObj.client.short_url.shorten.post(url_long = surl)
    if not rs:
      return False
    if 'urls' in rs:
      shortUrl = rs['urls'][0]['url_short']
      return shortUrl

    return  False
    

  def pubStartupLongWeibo(self,item):

    title = item['title']
    content = item['content']

    sentToPocket = 'http://getpocket.com/edit?'+urlencode({'url':item['link'],'title':item['title']})
    #sentToPocket = sentToPocket.replace('+','.')
    tempUrl = self.getShortUrl(sentToPocket)
    if tempUrl:
      sentToPocket = tempUrl
    print sentToPocket
    if len(title) > 65 :
      weiboTitle = title[0:65]+'...'
    else:
      weiboTitle = title
    weiboContent1 = '<'+weiboTitle+ '>  阅读全文: '
    weiboContent2 = '  #startup news# 原文地址: '+ item['link'] + ' (save to pocket '+sentToPocket+' )'

    return self._pubLongWeibo(title,content,item['link'],weiboContent1,weiboContent2)

  def _pubLongWeibo(self,title,content,link,weiboContent1,weiboContent2):

    self._setCookies()
    content = '原文地址: <a href="'+link+'">'+link+'</a><br>'+content
    blogId = self._postBlog(title,content)
    #blogId = 'd3182d790101ktgf'
    if blogId:
      print blogId
      time.sleep(20)
      blogImgUrl = self._getBlogImgUrl(blogId)
      if blogImgUrl:
        time.sleep(5)
        print blogImgUrl
        blogUrl = 'http://blog.sina.com.cn/s/blog_'+blogId+'.html'
        weiboContent = weiboContent1 + blogUrl + weiboContent2
        print weiboContent
        self._sentLongWeibo(blogId,blogImgUrl,weiboContent)
      return True
    
    return False

  def _sentLongWeibo(self,blogId,blogImgUrl,weiboContent):
    url = 'http://control.blog.sina.com.cn/admin/article/changWeiBoSend.php'
    header = self.header
    header['Cookie'] = self.cookie
    params = {}
    params['blog_id'] = blogId
    params['blog_type'] = 'blog'
    params['pic_path'] = blogImgUrl
    params['weibo_result'] = weiboContent
    while 1:
      res = self.cObj._http_call(the_url = url ,params = params, header = header, method = 'POST',timeout = 4)
      print res
      if res == False:
        time.sleep(5)
        continue
      break
    
    if 'code' in res and  res['code'] =='A00006':
      print 'ok_final'
    
  def _sentLongWeibo2(self,blogId,blogImgUrl,weiboContent):
    url = 'http://c.blog.sina.com.cn/weibopost.php'
    header = self.header2
    header['Cookie'] = self.cookie
    params = {}
    params['picUrl'] = blogImgUrl
    params['content'] = weiboContent
    params['bloguid'] = ''
    #params['sendblog'] = 1
    while 1:
      res = self.cObj._http_call(the_url = url ,params = params, header = header, method = 'POST')
      print res
      if res == False:
        time.sleep(5)
        continue
      break
    if 'code' in res and  res['code'] =='A00006':
      print 'ok_final'

      
  def _getBlogImgUrl(self,blogId):
    url = 'http://control.blog.sina.com.cn/admin/article/changWeiBoGetPic.php'
    header = self.header
    header['Cookie'] = self.cookie
    params = {}
    params['blog_id'] = blogId
    while 1:
      res = self.cObj._http_call(the_url = url ,params = params, header = header, method = 'POST')
      print res
      if res == False:
        time.sleep(3)
        continue
      break
    if 'code' in res and  res['code'] =='A00006':
      return res['data']['picUrl']

    return None
    
  def _getBlogImgUrl2(self,blogId):
    url = 'http://c.blog.sina.com.cn/getpicurl.php'
    header = self.header2
    header['Cookie'] = self.cookie
    params = {}
    params['blogid'] = blogId
    while 1:
      res = self.cObj._http_call(the_url = url ,params = params, header = header, method = 'POST')
      if res == False:
        time.sleep(3)
        continue
      break
    if 'code' in res and  res['code'] =='A00006':
      return res['data']['pic_url']

    return False

  def _postBlog(self,title,content):
    url = 'http://control.blog.sina.com.cn/admin/article/article_post.php'    
    header = self.header
    header['Cookie'] = self.cookie
    params = {}
    params['assoc_style'] = '1'
    params['utf8'] = '1'
    params['is_changweibo'] = '1'
    params['blog_body'] = content
    params['blog_title'] = title
    params['conlen'] = len(params['blog_body'])
    params['is_album']='0'
    #params['vtoken']='6070daffb69f20a212dc61dca8bf55a3'
    params['vtoken']='45a6f5836d745d5900a76c226ae95a72'
    params['is_media']='0'
    params['is_stock']='0'
    params['is_tpl']='0'
    params['assoc_style']='1'
    params['articleStatus_preview']='1'
    params['topic_id']='0'
    params['topic_channel']='0'
    params['blog_class']='00'
    res = self.cObj._http_call(the_url = url ,params = params, header = header, method = 'POST')
    print res
    if not res:
      return False
    if 'code' in res and  res['code'] =='B06001':
      return res['data']
    return None
    

  def _postBlog2(self,title,content):
    url = 'http://c.blog.sina.com.cn/cblogpost.php'    
    header = self.header2
    header['Cookie'] = self.cookie
    params = {}
    params['content'] = content
    params['title'] = title
    params['tmp']= 0
    res = self.cObj._http_call(the_url = url ,params = params, header = header, method = 'POST')
    if not res:
      return False
    if 'code' in res and  res['code'] =='A00006':
      return res['data']['blogid']
    if 'message' in res:
      print res['message']
    return False
    

  def _setCookies(self):
    header = self.header
    header['Cookie'] = self.cookie
    url = 'http://control.blog.sina.com.cn/admin/article/changWeiBo.php'
    cookies = self.cObj._http_call_set_cookie(the_url = url,header = header)
    if cookies:
      self.cookie += cookies
    
  def _setCookies2(self):
    header = self.header2
    header['Cookie'] = self.cookie
    url = 'http://c.blog.sina.com.cn/cblog.php'
    cookies = self.cObj._http_call_set_cookie(the_url = url,header = header)
    self.cookie += cookies

