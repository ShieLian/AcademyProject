#coding=UTF-8
'''
Created on 2015年11月30日

@author: ShieLian
'''
import cookielib
import urllib2
from urllib2 import HTTPError,URLError
import threading
import os
import copy

from spider.core import events
from utils import parserlib
from utils.CustomErrors import *

class Spider:
    '''
    classdocs
    '''
    def __init__(self, params={}):
        if params!=None:
            if params.has_key("timeout"):
                self.timeout=params["timeout"]
            else:
                self.timeout=100
            if params.has_key("path"):
                self.path=params["path"]
                if self.path[-1]!='/':
                    self.path+='/'
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
            else:
                self.path="./"
        else:
            self.timeout=100
        self.notitleid=1
        self.protocal="http"
        cookieJar = cookielib.CookieJar()
        self.cookieJar=cookieJar
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
        
        self.opener=opener
        urllib2.install_opener(opener)
        
        self.alive=True
        self.title=''
        
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
        
        #try:
        response=urllib2.urlopen(url,timeout=self.timeout)
        #except URLError:
        #    print url
        #    raise NoConnectionError
        html=response.read()
        try:
            title=parserlib.getTitle(html)
        except NoTitleError:
            title=("Untitled-%d"%self.notitleid)
            ++self.notitleid
        self.title=title
        #resourceUrls=parserlib.parseImgs(html)|parserlib.parseStyles(html)|parserlib.parseScripts(html)|parserlib.parseStyleImgs(html)
        resourceUrls=parserlib.parseSrcs(html)|parserlib.parseStyleImgs(html)
        if processLock:
            processLock.acquire()
            resourceUrlPool|=resourceUrls
            processLock.release()
        frameUrls=parserlib.parseFrames(html)
        '''@todo'''
        if not os.path.exists((self.path+self.title+'/').decode('utf-8')):
            os.makedirs((self.path+self.title+'/').decode('utf-8'))
        for resourceurl in resourceUrls:
            if not self.alive:
                return
            resourceurl=parserlib.getAbsUrl(resourceurl, url)
            try:
                response=urllib2.urlopen(resourceurl)
            except HTTPError:
                continue
            except URLError:
                print resourceurl
                continue
            if resourceurl[-3:]=="css":
                self.saveResource(self.path+self.title+'/'+parserlib.getFileName(resourceurl),parserlib.filtUrl(response.read(),resourceurl))
            else:
                self.saveResource(self.path+self.title+'/'+parserlib.getFileName(resourceurl),response.read())
        self.saveText(("<!-- saved form %s-->\n"%url)+parserlib.filtUrl(html,url,title),self.path+title+".html")
        for frameurl in frameUrls:
            if not self.alive:
                return
            if not os.path.exists(self.path+self.title+'/'+parserlib.getFileName(frameurl)):
                try:
                    self.fetchFrame(frameurl,self.path,usecookie)
                except HTTPError:
                    continue
    
    def fetchFrame(self,url,path,usecookie):
        """
                抓取特定的一个框架
                返回：(string)html
        pars:
            url(string)
            path(string)保存路径
            usecookie(boolean)
        """
        protocal=url[:url.find('://')]#协议名
        try:
            response=urllib2.urlopen(url,timeout=self.timeout)
        except URLError:
            raise NoConnectionError
        html=response.read()
        framename=parserlib.getFrameName(url)
        #resourceUrls=parserlib.parseImgs(html)|parserlib.parseStyles(html)|parserlib.parseScripts(html)|parserlib.parseStyleImgs(html)
        resourceUrls=parserlib.parseSrcs(html)|parserlib.parseStyleImgs(html)
        if processLock:
            processLock.acquire()
            resourceUrlPool|=resourceUrls
            processLock.release()
        frameUrls=parserlib.parseFrames(html)
        if not os.path.exists((self.path+framename+'/').decode('utf-8')):
            os.makedirs((self.path+framename+'/').decode('utf-8'))
        for resourceurl in resourceUrls:
            if not self.alive:
                return
            resourceurl=parserlib.getAbsUrl(resourceurl, url)
            try:
                response=urllib2.urlopen(resourceurl)
            except HTTPError:
                continue
            except URLError:
                print resourceurl
                continue
            if resourceurl[-3:]=="css":
                self.saveResource(path+framename+'/'+parserlib.getFileName(resourceurl),parserlib.filtUrl(response.read(),resourceurl))
            else:
                self.saveResource(path+framename+'/'+parserlib.getFileName(resourceurl),response.read())
        self.saveText(("<!-- saved from %s-->\n"%url)+parserlib.filtUrl(html,url),path+parserlib.getFrameName(url))
        for frameurl in frameUrls:
            if not self.alive:
                return
            if not os.path.exists(self.path+self.title+'/'+parserlib.getFileName(frameurl)):
                try:
                    self.fetchFrame(frameurl,path+framename,usecookie)#xxx
                except HTTPError:
                    continue
                
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
        if os.path.exists(path):
            return
        print path
        f=open(path.decode('utf-8'),"wb")
        f.write(bytes)
        f.close()
        if processLock:
            processLock.acquire()
            processEventBus.pushEvent(events.ProcessEvent(content=1))
            processLock.release()
processLock,resourceUrlPool,processEventBus=None,None,None
def startFetch(urlList,savePath,usecookie,Lock,UrlPool,EventBus):  
    '''
    pars:
        string url
        dic advancedOption
    '''
    #urllib队列
    processLock,resourceUrlPool,processEventBus=Lock,UrlPool,EventBus
    worker=Spider({'path':savePath})
    thread=None
    if usecookie:
        for url in urlList:
            thread=threading.Thread(target=worker.fetchPage(url, usecookie),args=(url,True))
            thread.start()
            thread.join()
    else:
        for url in urlList:
            newworker=copy.deepcopy(worker)
            thread=threading.Thread(target=newworker.fetchPage(url, usecookie),args=(newworker,url,False))
            thread.start()
            thread.join()
