'''
Created on 2015年11月30日

@author: ShieLian
'''

class Reptile(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    def fetchPage(self,url,cookieBuffer=None):
        """
                底层，抓取特定的一个页面
                返回：(string)html
        """
        
    def savePage(self,html,path):
        """
                底层，保存(string)html，
        pars:
            string html
            string path
        """
        f=open(path,"w")
        f.write(html)
        f.close
    def startFetch(self,url,advancedOption=""):  
        '''
        pars:
            string url
            string advancedOption
        '''