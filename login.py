#!/usr/bin/env python
#coding=utf8

import urllib
import urllib2
import cookielib
import base64
import re
import json
import hashlib
import os
import rsa
import binascii


cookiejar = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

parameters = {
    'entry': 'weibo',
    'callback': 'sinaSSOController.preloginCallBack',
    'su': 'd2FuZ2ppbmdidXB0JTQwMTM5LmNvbQ==',
    'rsakt': 'mod',
    'checkpin': '1',
    'client': 'ssologin.js(v1.4.11)',
    '_': '1362560902427'
}

postdata = {
    'entry': 'sso',
    'gateway': '1',
    'from': '',
    'savestate': '30',
    'useticket': '0',
    'pagerefer': 'http://login.sina.com.cn/sso/login.php',
    'vsnf': '1',
    'su': '',
    'service': 'sso',
    'servertime': '',
    'nonce': '',
    'pwencode': 'rsa2',
    'rsakv': '',
    'sp': '',
    'encoding': 'UTF-8',
    'prelt': '0',
    'returntype': 'IFRAME',
    'callback': 'parent.sinaSSOController.loginCallBack'
}
class Login:
  def get_servertime(self):
    url = 'http://login.sina.com.cn/sso/prelogin.php?' + urllib.urlencode(parameters)
    data = urllib2.urlopen(url).read()
    p = re.compile('\((.*)\)')
    try:
      json_data = p.search(data).group(1)
      data = json.loads(json_data)
      servertime = str(data['servertime'])
      nonce = data['nonce']
      pubkey = data['pubkey']
      rsakv = data['rsakv']
      return servertime, nonce, pubkey, rsakv
    except:
      print 'Get severtime error!'
      return None

  def get_pwd(self,pwd, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd) #拼接明文 js加密文件中得到
    passwd = rsa.encrypt(message, key) #加密
    passwd = binascii.b2a_hex(passwd)  #将加密信息转换为16进制
    return passwd

  def get_user(self,username):
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username

  def login(self,username, pwd):

    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)'
    try:
      servertime, nonce, pubkey, rsakv = self.get_servertime()
    except:
      return
    global postdata
    postdata['servertime'] = servertime
    postdata['nonce'] = nonce
    postdata['rsakv'] = rsakv
    postdata['su'] = self.get_user(username)
    postdata['sp'] = self.get_pwd(pwd, servertime, nonce, pubkey)

    postdata = urllib.urlencode(postdata)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}

    req = urllib2.Request(
      url=url,
      data=postdata,
      headers=headers
    )
    result = urllib2.urlopen(req)
    text = result.read()
    if text.find('"uid":"') > 0:
      cookie = result.info().getheader('Set-Cookie')
      return cookie
    return None
