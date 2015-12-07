'''
Created on 2015年12月4日

@author: ShieLian
'''
class Cookie:
    def __init__(self,name,domain,path,lifetime,content):
        self.name,self.domain,self.path,self.lifetime,self.content=name,domain,path,lifetime,content
        
        
class CookieBuffer:
    def __init__(self,host):
        self.host=host
        self.cookies=[]
    
    def addCookie(self,cookie):
        if(not isinstance(cookie,Cookie)):
            raise TypeError("The param is not a Cookie")
        self.cookies.append(cookie)
        
    def removeCookie(self,cookiename):
        #TODO
        for cookie in self.cookies:
            if cookie.name==cookiename:
                self.cookies.name.remove(cookie)

    