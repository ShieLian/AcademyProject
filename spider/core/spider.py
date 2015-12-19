#coding=UTF-8
'''
Created on 2015年11月30日

@author: ShieLian
'''
import cookielib
import urllib2
from urllib2 import HTTPError,URLError

import os

from utils import parserlib
from utils.CustomErrors import *


class Spider(object):
    '''
    classdocs
    '''


    def __init__(self, params={}):
        if params!=None:
            if params.has_key("timeout"):
                self.timeout=params["timeout"]
            else:
                self.timeout=4
            if params.has_key("path"):
                self.path=params["path"]+'/'#!
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
            else:
                self.path="./"
        else:
            self.timeout=4
        self.notitleid=1
        self.protocal="http"
        cookieJar = cookielib.CookieJar()
        self.cookieJar=cookieJar
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
        self.opener=opener
        urllib2.install_opener(opener)
        
    def fetchPage(self,url,usecookie=False):
        """
                抓取特定的一个页面
                返回：(string)html
        pars:
            url(string)
            usecookie(boolean)
        """
        protocal=url[:url.find('://')]#协议名

        if usecookie:
            urllib2.install_opener(self.opener)
        else:
            urllib2.install_opener(None)
        
        try:
            response=urllib2.urlopen(url,timeout=self.timeout)
        except URLError:
            raise NoConnectionError
        html=response.read()
        try:
            title=parserlib.getTitle(html)
        except NoTitleError:
            title=("Untitled-%d"%self.notitleid)
            ++self.notitleid
        #resourceUrls=parserlib.parseImgs(html)|parserlib.parseStyles(html)|parserlib.parseScripts(html)|parserlib.parseStyleImgs(html)
        resourceUrls=parserlib.parseSrcs(html)|parserlib.parseStyleImgs(html)
        frameUrls=parserlib.parseFrames(html)
        total_file=len(resourceUrls)+len(frameUrls)+1
        downloaded_file=0
        '''@todo'''
        for resourceurl in resourceUrls:
            resourceurl=parserlib.getAbsUrl(resourceurl, url)
            try:
                response=urllib2.urlopen(resourceurl)
            except HTTPError:
                continue
            except URLError:
                print resourceurl
                continue
            if resourceurl[-3:]=="css":
                self.saveResource(self.path+parserlib.getFileName(resourceurl),parserlib.filtUrl(response.read()))
            else:
                self.saveResource(self.path+parserlib.getFileName(resourceurl),response.read())
            ++downloaded_file
        self.saveText(("<!-- saved form %s-->\n"%url)+parserlib.filtUrl(html,url),self.path+title+".html")
        print "!"
        ++downloaded_file
        for frameurl in frameUrls:
            if not os.path.exists(parserlib.getFileName(frameurl)):
                try:
                    self.fetchPage(frameurl,usecookie)
                except HTTPError:
                    continue
                ++downloaded_file
    def saveText(self,text,path):
        """
                底层，保存(string)text，
        pars:
            string html
            string path
        """
        f=open(path.decode("UTF-8"),"w")
        f.write(text)
        f.close()
    
    def saveResource(self,path,bytes):
        """
                底层，保存(string)bytes，如图片
        pars:
            string html
            string path
        """
        f=open(path,"wb")
        f.write(bytes)
        f.close()
        
def startFetch(self,url,advancedOption=""):  
    '''
    pars:
        string url
        string advancedOption
    '''
    #urllib队列