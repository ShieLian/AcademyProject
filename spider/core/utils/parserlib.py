#coding=UTF-8
'''
Created on 2015年11月30日

@author: ShieLian
'''

import re
import copy

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
    imgs=re.findall("(<(?:img|image) (?:[^=]+=[^\b>]*)>)",html,re.I)
#     print imgs
    for i in range(len(imgs)):
        imgs[i]=re.findall('src="([^"]+)"', imgs[i])[0]
    imgset=set(imgs)
    return imgset

def parseStyleImgs(text):
    imgs=re.findall("url:\(([^)]+)\)",text,re.I)
    imgs+=re.findall("url\(([^)]+)\)",text,re.I)
    return set(imgs)

def parseScripts(html):
    """
        返回html中所有的script标签中的src
    par html(string)
    return urls(string[])
    """
    jss=re.findall("(<script (?:[^=]+=[^\b>]*)>)",html,re.I)
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
    styles=re.findall("(<style (?:[^=]+=[^\b>]*)>)",html,re.I)
    urls=[]
#     print styles
    for i in range(len(styles)):
        if len(re.findall('src="([^"]+)"', styles[i]))!=0: 
            urls.append(re.findall('src="([^"]+)"', styles[i])[0])
    return set(urls)

def parseFrames(html):
    frames=re.findall("(<frame (?:[^=]+=[^\b>]*)>)",html,re.I)
#     print frames
    urls=[]
    for tag in frames:
        urls.append(re.findall('src[\b]*=[\b]*"([^"]+)',tag)[0])
    return set(urls)

def parseHrefs(html):
    
    tags=re.findall('(<[^>]+>)',html,re.I)
    for tag in tags:
        if not "href" in tag:
            tags.remove(tag)
    hrefs=[]
    for tag in tags:
        templist=re.findall('href="([^"]+)"',tag)
        if '#' in templist:
            print tag
            print templist
        if len(templist)!=0:
            hrefs+=copy.deepcopy(templist)
    return set(hrefs)
def filtUrl(text,path):
    '''
        过滤URL，资源只保留文件名，链接补全为绝对URL
    '''
    urls=parseImgs(text)|parseStyles(text)|parseScripts(text)|parseStyleImgs(text)|parseFrames(text)
#     print urls
    for url in urls:
        while url in text:
            text=text[:text.find(url)]+getFileName(url)+text[text.find(url)+len(url):]
    hrefs=parseHrefs(text)
    for url in hrefs:
        while (not isAbs(url)) and('href="'+url in text):
            index=text.find('href="'+url)
#             print getAbsUrl(url,path),text[index+len(url)+1:]
            text=text[:index+6]+getAbsUrl(url,path)+text[index+len(url)+6:]
    return text

def isAbs(url):
    return ("://" in url) and (url[0]!=':')

def getTitle(html):
    tittles=re.findall("<(?:title)>([^<]+)</(?:title)>",html,re.I)
    if len(tittles)==0:
#         print html
        raise NoTitleError()
    else:
        return tittles[0]

def getFileName(url):
    if not '/' in url: return url
    else : return url[url.rfind('/')+1:]
def getAbsUrl(url,path):
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
