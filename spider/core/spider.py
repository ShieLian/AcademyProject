#coding=UTF-8
'''
Created on 2015年11月30日

@author: ShieLian
'''
import cookielib
import urllib2

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
        else:
            self.timeout=4
        self.notitleid=1
        cookieJar = cookielib.CookieJar()
        self.cookieJar=cookieJar
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
        self.opener=opener
        urllib2.install_opener(opener)
        
    def fetchPage(self,url,usecookie=False):
        """
                底层，抓取特定的一个页面
                返回：(string)html
        pars:
            url(string)
            usecookie(boolean)
        """
        if usecookie:
            urllib2.install_opener(self.opener)
        else:
            urllib2.install_opener(None)
        response=urllib2.urlopen(url,timeout=self.timeout)
        html=response.read()
        try:
            title=parserlib.getTitle(html)
        except NoTitleError:
            title=("notitle-%d"%self.notitleid)
            ++self.notitleid
        self.savePage(html, ("./%s.html"% title).decode("UTF-8"))
        resourceUrls=parserlib.parseImgs(html)|parserlib.parseStyles(html)|parserlib.parseScripts(html)
        frameUrls=parserlib.parseFrames(html)
        for reurl in resourceUrls:
            print parserlib.getAbsUrl(reurl, url)
    def savePage(self,text,path):
        """
                底层，保存(string)text，
        pars:
            string html
            string path
        """
        f=open(path,"w")
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