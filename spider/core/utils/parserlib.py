#coding=UTF-8
'''
Created on 2015年11月30日

@author: ShieLian
'''
import re
def parseAdvanceOption(string):
    '''
        解析string为AdvancedOption
    '''
def parseImgs(html):
    """
        返回html中所有的img标签中的src
    par html(string)
    return urls(string[])
    """
    imgs=re.findall("(<img (?:[^=]+=[^ >]*)+>)",html)
    print imgs
    for i in range(len(imgs)):
        imgs[i]=re.findall('src="([^"]+)"', imgs[i])[0]
    return imgs