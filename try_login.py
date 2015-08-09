#!/usr/bin/env python3
# -*- coding: utf-8 -*-
' 登录 '
__author__ = 'zzyfisher'

import urllib 
import urllib.request 
import urllib.parse 
import http.cookiejar 
import re 
 

#登录页面，用来获取hash值
#http://forum.xitek.com/member.php?mod=logging&action=login&referer=http://forum.xitek.com/
loginFormUrl = 'http://forum.xitek.com/member.php?mod=logging&action=login&referer=http://forum.xitek.com/'
#执行登录的地址
loginUrl='http://forum.xitek.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash='


class loginRLKQ: 
    post_data=b""; 
    def __init__(self): 
        #初始化类，cook的值 
        cj=http.cookiejar.CookieJar() 
        opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj)) 
        opener.addheaders=[('User-Agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')] 
        #初始化全局opener 
        urllib.request.install_opener(opener) 

    #login方法需要加入post数据 
    def login(self,loginurl,encode): 
        #模拟登陆 
        req=urllib.request.Request(loginurl,self.post_data) 
        rep=urllib.request.urlopen(req) 
        d=rep.read() 
        #print(d) 
        d=d.decode(encode) 
        return d 
    #登陆之后获取其他网页方法 
    def getUrlContent(self,url,encode): 
        req2=urllib.request.Request(url) 
        rep2=urllib.request.urlopen(req2) 
        d2=rep2.read() 
        d22=d2.decode(encode) 
        return d22
        
if __name__=="__main__": 
    #实例化类 
    x=loginRLKQ() 
    #给post数据赋值 
    x.post_data=urllib.parse.urlencode({'username':"firebux",'password':'1122FFBB'}).encode(encoding="gbk") 
    #登陆 
    y=x.login("http://forum.xitek.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=","gbk") 
    #获取网页信息 
    print(x.getUrlContent("http://forum.xitek.com/thread-1483570-1-1-1.html","gbk")) 
