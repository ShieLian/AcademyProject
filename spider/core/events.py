#coding=utf-8
'''
Created on 2015年12月21日

@author: ShieLian
'''
class Event:
    def __init__(self,eventname):
        self.name=eventname
class EventBus:
    def __init__(self):
        self.listeners={}
        self.queues={}
    def registry(self,eventListener):
        if self.listeners.has_key(eventListener.eventName):
            self.listeners[eventListener.eventName].append(eventListener)
        else:
            self.listeners[eventListener.eventName]=[eventListener]
        self.queues[eventListener.eventName]=[]
    def pushEvent(self,event):
        self.queues[event.eventName].append(event)
    def fire(self):
        '''
                被单独的事件处理线程调用，分发事件
        '''
        for eventname in self.listeners.keys():
            for event in self.queues[eventname]:
                for listener in self.listeners[eventname]:
                    listener.handle(event)
                self.queues[eventname].remove(event)
                    
class EventListener:
    def __init__(self,eventName):
        self.eventName=eventName
    def handle(self,event):
        pass
    
class ProcessListener(EventListener):
    def __init__(self,callback):
        EventListener.__init__(self,"process")
        self.callback=callback
    def handle(self,event):
        self.callback(event.process)
        
class ProcessEvent(Event):
    def __init__(self,eventName,content=""):
        Event.__init__(self,eventName)
        self.eventName=eventName
        self.process=content