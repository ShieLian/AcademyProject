#coding=utf-8
'''
Created on 2015年12月21日

@author: ShieLian
'''
import threading
class Event:
    def __init__(self,eventname):
        self.eventname=eventname

class EventBus:
    def __init__(self):
        self.listeners={}
        self.queues={}
        self.alive=True
        self.fireThread=threading.Thread(target=self.fire)
        self.fireThread.setDaemon(True)
        self.lock=threading.Lock()
        self.fireThread.start()
    def registry(self,eventListener):
        '''
                注册监听器
        '''
        if self.listeners.has_key(eventListener.eventname):
            self.listeners[eventListener.eventname].append(eventListener)
        else:
            self.listeners[eventListener.eventname]=[eventListener]
        self.queues[eventListener.eventname]=[]
    def pushEvent(self,event):
        self.lock.acquire()
        self.queues[event.eventname].append(event)
        self.lock.release()
    def fire(self):
        '''
                被单独的事件处理线程调用，分发事件
        '''
        while self.alive:
            for eventname in self.listeners.keys():
                for event in self.queues[eventname]:
                    for listener in self.listeners[eventname]:
                        listener.handle(event)
                    self.lock.acquire()
                    self.queues[eventname].remove(event)
                    self.lock.release()
    
    def shut(self):
        self.alive=False
class EventListener:
    def __init__(self,eventname):
        self.eventname=eventname
    def handle(self,event):
        pass
    
class ProcessListener(EventListener):
    def __init__(self,callback):
        EventListener.__init__(self,"processevent")
        self.callback=callback
    def handle(self,event):
        self.callback(event.content)
        
class ProcessEvent(Event):
    def __init__(self,content=""):
        Event.__init__(self,'processevent')
        self.eventname='processevent'
        self.content=content