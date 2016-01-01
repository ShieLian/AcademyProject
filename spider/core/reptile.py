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
import re
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
                self.timeout=30
            if params.has_key("path"):
                self.path=params["path"]
                if self.path[-1]!='/':
                    self.path+='/'
                if not os.path.exists(self.path):
                    os.makedirs(self.path)
            else:
                self.path="./"
        else:
            self.timeout=30
        self.notitleid=1
        self.protocal="http"
        cookieJar = cookielib.CookieJar()
        self.cookieJar=cookieJar
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
        
        self.opener=opener
        urllib2.install_opener(opener)
        
        self.alive=True
        self.title=''
    
    processLock,resourceUrlPool,processEventBus=None,None,None
    
    def fetchPage(self,url,usecookie=False):
        """
                抓取特定的一个页面
                返回：(string)html
        pars:
            url(string)
            usecookie(boolean)
        """
        global processLock,resourceUrlPool,processEventBus
        
        protocal=url[:url.find('://')]#协议名

        if usecookie:
            urllib2.install_opener(self.opener)
        else:
            urllib2.install_opener(None)
        
        try:
            response=urllib2.urlopen(url,timeout=self.timeout)
        except URLError:
            print url
            raise NoConnectionError
        html=response.read()
        try:
            title=parserlib.getTitle(html)
        except NoTitleError:
            title=("Untitled-%d"%self.notitleid)
            self.notitleid+=1
        self.title=title
        resourceUrls=parserlib.parseSrcs(html)|parserlib.parseStyleImgs(html)
        if processLock:
            processLock.acquire()
            resourceUrlPool|=resourceUrls
            processLock.release()
        frameUrls=parserlib.parseFrames(html)
        self.path=self.path.encode('u8')
        sameNameNum=0
        while os.path.exists((self.path+title+".html").decode('u8')):
            f=open((self.path+title+".html").decode('u8'),'r')#从保存的网页的开头拿出该网页的原url
            text=f.readline()
            f.close()
            text=text[text.find('from ')+5:-4]
            if text in url or url in text:
                return
            sameNameNum+=1
            title='%s(%d)'%(self.title,sameNameNum)
        if not os.path.exists((self.path+title+'/').decode('u8')):
            os.makedirs((self.path+title+'/').decode('utf-8'))
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
        self.saveText(("<!-- saved from %s-->\n"%url)+parserlib.filtUrl(html,url,title),self.path+title+".html")
        for frameurl in frameUrls:
            if not self.alive:
                return
            if not os.path.exists(self.path+self.title+'/'+parserlib.getFileName(frameurl)):
                try:
                    self.fetchFrame(frameurl,self.path,usecookie)
                except HTTPError:
                    continue
        if processLock:
            processLock.acquire()
            processEventBus.pushEvent(events.ProcessEvent(content=-1))
            processLock.release()
            
    def fetchFrame(self,url,path,usecookie):
        """
                抓取特定的一个框架
                返回：(string)html
        pars:
            url(string)
            path(string)保存路径
            usecookie(boolean)
        """
        global processLock,resourceUrlPool,processEventBus
        
        protocal=url[:url.find('://')]#协议名
        try:
            response=urllib2.urlopen(url,timeout=self.timeout)
        except URLError:
            raise NoConnectionError
        html=response.read()
        framename=parserlib.getFrameName(url)
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
        if processLock:
            processLock.acquire()
            processEventBus.pushEvent(events.ProcessEvent(content=-1))
            processLock.release()
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
        f=open(path.decode('utf-8'),"wb")
        f.write(bytes)
        f.close()
        if processLock:
            processLock.acquire()
            processEventBus.pushEvent(events.ProcessEvent(content=1))
            processLock.release()

def startFetch(url,savePath,usecookie,Lock,UrlPool,EventBus):  
    '''
    pars:
        string url
        dic advancedOption
    '''
    global processLock,resourceUrlPool,processEventBus
    processLock,resourceUrlPool,processEventBus=Lock,UrlPool,EventBus
    worker=Spider({'path':savePath})
    thread=threading.Thread(target=worker.fetchPage(url, usecookie),args=(url,usecookie))
    thread.start()
    thread.join()
