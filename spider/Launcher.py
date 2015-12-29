#coding=UTF-8
'''
Created on 2015.11.30

@author: ShieLian
'''
import copy

import core.events as events
import threading
from gui.frame import *
from core.utils import parserlib
'''
@todo 监听注册&新建线程
'''
def main():
    processEventBus.registry(events.ProcessListener(processEventHandler))
downLoadedResourceNum=0
resourceUrlPool=set()
processLock=threading.Lock()
def processEventHandler(content):
    processLock.acquire()
    downLoadedResourceNum+=content
    frame.updateProcess("%d / %d"%(downLoadedResourceNum,len(resourceUrlPool)))
    processLock.release()
if __name__=='__main__':
    processEventBus=events.EventBus()
    frame=Frame()
    main()

#接口
def startFetch(targetUrl,savePath,settings,advancedSettings):
    #settings:threads,urllistfile,usecookie
    urllist=parserlib.getUrlList(targetUrl,settings,advancedSettings)
    threadnum=settings["threads"]
    threadnum=min( (len(urllist),threadnum) )
        
