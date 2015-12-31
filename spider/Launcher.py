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

def main():
    processEventBus.registry(events.ProcessListener(processEventHandler))
   
    
#接口
def startFetch(targetUrl,savePath,settings,advancedSettings):
    urllist=parserlib.getUrlList(targetUrl,settings,advancedSettings)
    reptile.startFetch(urllist,savePath,settings['usecookie'],processLock,resourceUrlPool,processEventBus)
    
if __name__=='__main__':
    processEventBus=events.EventBus()
    window=frame.Frame(startFetch)
    main() 
    
def processEventHandler(content):
    processLock.acquire()
    downLoadedResourceNum+=content
    window.updateProcess("%d / %d"%(downLoadedResourceNum,len(resourceUrlPool)))
    processLock.release()

