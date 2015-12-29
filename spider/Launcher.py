#coding=UTF-8
'''
Created on 2015.11.30

@author: ShieLian
'''
import core.events as events
import threading
from gui.frame import *
processEventBus=events.EventBus()
frame=Frame()

'''
@todo 监听注册&新建线程
'''
def main():
    processEventBus.registry(events.ProcessListener(processEventHandler))
def startFetch(targetUrl,savePath,settings,advancedSettings):
    pass
downLoadedResourceNum=0
resourceUrlPool=set()
processLock=threading.Lock()
def processEventHandler(content):
    processLock.acquire()
    downLoadedResourceNum+=content
    frame.updateProcess("%d / %d"%(downLoadedResourceNum,len(resourceUrlPool)))
    processLock.release()
main()
