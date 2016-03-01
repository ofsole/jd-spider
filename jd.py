#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '自动签到'
__author__ = 'elvis cai'
__mtime__ = '2016-3-1'
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import cookielib
import os
import re
import time

class JD():
    def __init__(self):
        self.filename = 'cookie.txt'
        self.cookie   = cookielib.MozillaCookieJar()
        self.opener   = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        self.user     = ''
        self.passwd   = ''
        self.sign_url = 'https://vip.jd.com/index.php?mod=Vip.Ajax&action=signIn'
        self.url      = 'https://passport.jd.com/uc/login'
        self.post     = {
             'chkRememberMe': 'on',
             'loginname': self.user,
             'loginpwd': self.passwd,
             'nloginpwd': self.passwd,
             'machineCpu': '',
             'machineDisk': '',
             'machineNet': '',
             'nloginpwd': self.passwd
        }
        self.postData = urllib.urlencode(self.post)
        self.headers = { 'User-Agent'     : "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
                             'Pragma'     : "no-cache",
                             'Host'       : "vip.jd.com",
                             'Upgrade-Insecure-Requests' : '1',
                             'Referer'    : "http://vip.jd.com/"
                           }
    def login(self):
        if os.path.exists(self.filename):
            with open(self.filename) as f:
                self.cookie.load(self.filename, ignore_discard=True, ignore_expires=True)
            request  = urllib2.Request(
                url  = self.sign_url,
                data = self.postData)
            result = self.opener.open(request)
            print result.read()
        else:
            request =  urllib2.Request(self.url)
            response = urllib2.urlopen(request)
            content = response.read()
            pattern_ve = re.compile('<img id="JD_Verification1.*?src2="(.*?)"',re.S)
            items_ve = re.findall(pattern_ve,content)
            pattern = re.compile('<form id="formlogin".*?<input.*?<input.*?<input.*?<input.*?.*?<input.*?<input.*?<input.*?name="(.*?)" value="(.*?)"',re.S)
            items = re.findall(pattern, content)
            print items
            for item in items:
                name = item[0]
                value = item[1]
            self.post[name] = value
            verify_url = items_ve[0].replace('amp;','') + '&yys=' + str(int(time.time() * 1000))
            print verify_url
#            image = urllib2.urlopen(urllib2.Request(verify_url)) 
            image = self.opener.open(verify_url)
            f = open('image.jpg','wb')
            f.write(image.read())
            f.close()
            print 'input code:'
            authcode = raw_input()
            self.post['authcode'] = authcode
            self.postData = urllib.urlencode(self.post)
            request  = urllib2.Request(
                url  = 'https://passport.jd.com/uc/loginService',
                data = self.postData)
            result   = self.opener.open(request).read().decode('gbk')
            print result
            if 'success' in result:
                self.cookie.save(ignore_discard=True, ignore_expires=True)
spider = JD()
spider.login()
