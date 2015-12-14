#coding=UTF-8
'''
Created on 2015年11月30日

@author: ShieLian
'''

import re

from CustomErrors import *


def parseAdvanceOption(string):
    '''
        解析string为AdvancedOption
    '''
def parseImgs(html):
    """
        返回html中所有的img标签中的src
    par html(string)
    return urls set(string)
    """
    imgs=re.findall("(<img (?:[^=]+=[^\b>]*)>)",html)
#     print imgs
    for i in range(len(imgs)):
        imgs[i]=re.findall('src="([^"]+)"', imgs[i])[0]
    imgset=set(imgs)
    return imgset

def parseStyleImgs(css):
    imgs=re.findall("url:\(([^)]+)\)",css)
    return set(imgs)

def parseScripts(html):
    """
        返回html中所有的script标签中的src
    par html(string)
    return urls(string[])
    """
    jss=re.findall("(<script (?:[^=]+=[^\b>]*)>)",html)
    urls=[]
#     print jss
    for i in range(len(jss)):
        if len(re.findall('src="([^"]+)"', jss[i]))!=0: 
            urls.append(re.findall('src="([^"]+)"', jss[i])[0])
    return set(urls)

def parseStyles(html):
    """
        返回html中所有的script标签中的src
    par html(string)
    return urls(string[])
    """
    styles=re.findall("(<style (?:[^=]+=[^\b>]*)>)",html)
    urls=[]
#     print styles
    for i in range(len(styles)):
        if len(re.findall('src="([^"]+)"', styles[i]))!=0: 
            urls.append(re.findall('src="([^"]+)"', styles[i])[0])
    return set(urls)

def parseFrames(html):
    '''
    @todo
    '''

def getTitle(html):
    tittles=re.findall("<(?:title)>([^<]+)</(?:title)>",html,re.I)
    if len(tittles)==0:
        print html
        raise NoTitleError()
    else:
        return tittles[0]
    
def getAbsUrl(url,path):
#     if "//" in url:
#         if "://" in url:
#             if url[0]!=':' : return url
#             else: return "http"+url
#         else: return "http:"+url
#     else:
#         
#         if url[:2]=='..':
#             folder=path[0:path.rfind('/')]
#             return folder[0:folder.rfind('/')]+url[2:]
#         elif url[0]=='.':
#             return path[0:path.rfind('/')]+url[1:]
#         else:
#             if path[-1]=='/': return path+url
#             elif path.count('/')==2: return path+'/'+url
#             else 
    if path[-1]!='/' :
        if path.rfind('.')>path.rfind('/'):
            path=path[:path.rfind('/')+1]
        else:
            path+='/'
    if "//" in url:
        if "://" in url:
            if url[0]!=':' : return url
            else: return "http"+url
        else: return "http:"+url
    else:
        if url[:2]=='..':
            return path[0:path.rfind('/')]+url[2:]
        elif url[0]=='.':
            return path[0:path.rfind('/')]+url[1:]
        else:
            if url[0]!='/ ' : return path+url
            else: return path+url[1:]
