#coding=UTF-8
'''
Created on 2015.11.30

@author: ShieLian
'''
import copy

import core.events as events
import threading
from core import reptile
from core.utils import parserlib
import gui.frame as frame
from core.utils import CustomErrors

downLoadedResourceNum=0
resourceUrlPool=set()
processLock=threading.Lock()
processEventBus=None
window=None

#接口
def startFetch(targetUrl,savePath,settings,advancedSettings):
    global downLoadedResourceNum
    urllist=parserlib.getUrlList(targetUrl,settings,advancedSettings)
    window.lock()
    for url in urllist:
        downLoadedResourceNum=0
        try:
            reptile.startFetch(url,savePath,settings['usecookie'],processLock,resourceUrlPool,processEventBus)
        except CustomErrors.NoConnectionError:
            window.unlock()
            window.updateProcess('无连接，请查看网络连接以及目标url是否正确')
    window.unlock()
def processEventHandler(content):
    processLock.acquire()
    global downLoadedResourceNum,window
    if content!=-1:
        downLoadedResourceNum+=content
        window.updateProcess("%d 资源已下载/ %d 资源需下载"%(downLoadedResourceNum,len(resourceUrlPool)))
        processLock.release()
    else:
        window.updateProcess("%d 资源已下载/ %d 资源需下载,已完成"%(downLoadedResourceNum,len(resourceUrlPool)))
        processLock.release()
def shut():
    processEventBus.pushEvent(events.ShutEvent())

def main():
    processEventBus.registry(events.ProcessListener(processEventHandler))
    processEventBus.registry(events.ShutListener(shut))
    
if __name__=='__main__':
    processEventBus=events.EventBus()
    main()
    window=frame.Window(startFetch,shut)
    window.startloop()

