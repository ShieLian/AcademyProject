#coding=UTF-8
'''
Created on 2015.11.30

@author: ShieLian
'''
import copy

import core.events as events
import threading
from spider.core import reptile
from core.utils import parserlib
import gui.frame as frame

downLoadedResourceNum=0
resourceUrlPool=set()
processLock=threading.Lock()
processEventBus=None
window=None

def main():
    processEventBus.registry(events.ProcessListener(processEventHandler))
   
    
#接口
def startFetch(targetUrl,savePath,settings,advancedSettings):
    urllist=parserlib.getUrlList(targetUrl,settings,advancedSettings)
    reptile.startFetch(urllist,savePath,settings['usecookie'],processLock,resourceUrlPool,processEventBus)

def processEventHandler(content):
    processLock.acquire()
    global downLoadedResourceNum,window
    if content!=-1:
        downLoadedResourceNum+=content
        window.updateProcess("%d 资源已下载/ %d 资源需下载"%(downLoadedResourceNum,len(resourceUrlPool)))
        processLock.release()
    else:
        window.updateProcess("%d 资源已下载/ %d 资源需下载,已完成"%(downLoadedResourceNum,len(resourceUrlPool)))
        window.unlock()
if __name__=='__main__':
    processEventBus=events.EventBus()
    main()
    window=frame.Window(startFetch)
    window.startloop()

