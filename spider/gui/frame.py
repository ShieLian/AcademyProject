#coding=utf-8
'''
Created on 2015年11月30日
底层和GUI间只由reptile.core.reptile.Reptile对象和此对象交互
这个类包装整个GUI，并由此调用Launcher的入口Reptile.startFetch
@author: 
'''
from Tkinter import *
from FileDialog import *
import threading
import tkMessageBox
import tkFileDialog
class Window:
    def __init__(self,callback,shut):                                                                                 # 构建基础用户界面的所有基本控件
        self.root = Tk()
        self.root.title("网页爬取器")
        
        self.str_targeturl = StringVar()
        self.str_savepath = StringVar()

        self.label1=Label(self.root,text='目标网页地址：')
        self.label1.grid(row=0, column=0, sticky=W)
        
        self.entry_targeturl = Entry(self.root, textvariable=self.str_targeturl)
        self.entry_targeturl.grid(row=0, column=1, columnspan=3)
        
        self.label2 = Label(self.root, text='   保存在： ')
        self.label2.grid(row=1, column=0, sticky=W)
        
        self.entry_savepath = Entry(self.root, textvariable=self.str_savepath)
        self.entry_savepath.grid(row=1, column=1, columnspan=3)
        
        self.button_browse = Button(self.root, text='   浏览   ', command=self.selectSavePath)
        self.button_browse.grid(row=1, column=4)
        self.button_advancedoption = Button(self.root, text='高级选项', command=self.openAdvancedOptionDialog)
        self.button_advancedoption.grid(row=3, column=0)
        
        self.content=StringVar()#显示进度的StringVar
        self.label3=Label(self.root, textvariable=self.content)
        self.label3.grid(row=4, column=0, columnspan=5, sticky=W+E)
        
        self.button_option = Button(self.root, text='   设置   ', command=self.openOptionDialog)
        self.button_option.grid(row=2, column=0, columnspan=1)
        
        self.button_start = Button(self.root, text='开始爬取',fg='red', command=self.start)
        self.button_start.grid(row=2, column=3)
        
        self.button_shut = Button(self.root, text='结束爬取', fg='blue',command=self.end)
        self.button_shut.grid(row=2, column=4)
        
        self.button_exit = Button(self.root, text='退出程序', command=self.quit)
        self.button_exit.grid(row=3, column=4)
        
        self.stateditemlist=[self.entry_targeturl,self.entry_savepath,self.button_browse,self.button_advancedoption,self.button_option,self.button_start]
        
        self.optionDialog=OptionsDialog(self)
        self.optionDialog.hide()
        self.advancedOptionDialog=AdvancedOptionsDialog(self)
        self.advancedOptionDialog.hide()
        self.settings={'urllistfile':'','usecookie':1}
        self.advancedSettings=("","")
        self.callback=callback
        self.shut=shut
        
        self.root.resizable(False, False)
        
    def startloop(self):
        self.root.mainloop()
    
    def selectSavePath(self):                                                                         # 打开文件浏览器的函数
        path=tkFileDialog.askdirectory()
        self.str_savepath.set(path)

    def openAdvancedOptionDialog(self):                                                                         # 打开高级选项界面的函数
        self.advancedOptionDialog=self.advancedOptionDialog.show()
    def openOptionDialog(self):                                                                                 # 打开设置界面的函数                                                        
        self.optionDialog=self.optionDialog.show()
        
    def getInfo(self):                                                                                  # 将用户的设置的目标网站与储存位置储存起来
        return self.str_targeturl.get(),self.str_savepath.get()
    
    def updateProcess(self,string):
        self.content.set(string)
    
    def lock(self):
        for item in self.stateditemlist:
            item["state"]='disable'
    def unlock(self):
        for item in self.stateditemlist:
            item["state"]='normal'
    def start(self):                                                                                    # 调用程序开始爬取页面的函数
        if  not (self.str_targeturl.get() or (self.settings and self.settings["urllistfile"])):
            tkMessageBox.showerror(u"错误",u"没有设置目标网页地址，请设置目标URl或导入URL列表文件")
            return
        path=self.str_savepath.get()
        if not path:
            tkMessageBox.showerror(u"错误",u"没有设置保存位置")
            return 
        if not os.path.exists(path) or not os.path.isdir(path) :
            choose=tkMessageBox.askquestion(u"警告",u"文件路径不存在,是否新建路径?")
            if choose=='no':
                return
            else:
                os.makedirs(path)
        self.lock()
        url=self.str_targeturl.get()
        if not ('http' in url):
            url='http://'+url
        thread=threading.Thread(target=self.callback,args=(url,path,self.settings,self.advancedSettings))
        thread.start()
        #self.callback(url,path,self.settings,self.advancedSettings)

    def end(self):                                                                                      # 调用程序结束页面的爬取的函数
        self.shut()
        self.unlock()

    def quit(self):                                                                                     # 退出该程序
        self.root.quit()
#----------------------------------------------------------------------------------------------------------------
import os
class AdvancedOptionsDialog:
    def __init__(self,father): 
        self.father=father                                                                                # 构建高级选项用户界面的控件
        self.advancedSettings=("","")
        
        self.top = Toplevel()
        self.top.title("高级选项")
        
        self.var_3 = StringVar()
        self.var_3.set('')        
        self.var_4 = StringVar()
        self.var_4.set('')
        
        
        Label(self.top,text='URL参数列表').grid(row=0,column=0,columnspan=3,sticky=W+E)
        
        Label(self.top,text="参数名").grid(row=1,column=0,sticky=W)
        self.e3 = Entry(self.top,textvariable=self.var_3)
        self.e3.grid(row=2,column=0,columnspan=2)
        
        Label(self.top,text="参数取值").grid(row=1,column=1)
        self.e4 = Entry(self.top,textvariable=self.var_4)
        self.e4.grid(row=2,column=1,columnspan=2)
        self.button_del = Button(self.top,text='  删除  ',command=self.clear)
        self.button_del.grid(row=2,column=4)
        
        self.button_sure = Button(self.top,text='   确定   ',command=self.makesure)
        self.button_sure.grid(row=3,column=1)
        self.button_cancel = Button(self.top,text='   取消   ',command=self.quittop)
        self.button_cancel.grid(row=3,column=2)
        
    def append(self):
        pass
        
    def clear(self):
        self.var_3.set('')
        self.var_4.set('')
    def show(self):
        try:
            self.top.deiconify()
        except TclError:#处理关闭窗口后，无法令窗口重现的情况
            self=AdvancedOptionsDialog(self.father)
            self.advancedSettings=self.father.advancedSettings
        self.var_3.set(self.advancedSettings[0])
        self.var_4.set(self.advancedSettings[1])
        return self
    def hide(self):
        self.top.withdraw()              
                    
    def makesure(self):
        #检查参数取值是否有语法错误或返回类型不可迭代
        try:
            t=eval(self.var_4.get())
        except SyntaxError:
            tkMessageBox.showerror(u'错误', u'输入的表达式有语法错误')
            return
        if type(t)!=list and type(t)!=set and type(t)!=tuple :
            tkMessageBox.showerror(u'错误', u'参数取值不是可迭代对象')
            return
        self.top.withdraw()
        self.advancedSettings=self.getadvancedSettings()
        self.father.advancedSettings=self.getadvancedSettings()
        
    def quittop(self):                                                                                 # 退出高级选项界面
        self.top.withdraw()
    def getadvancedSettings(self):
        return (self.var_3.get(),self.var_4.get())
#----------------------------------------------------------------------------------------------------------------
class OptionsDialog:
    def __init__(self,father):                                                                                # 构建设置用户界面的控件
        self.father=father
        self.settings={'urllistfile':'','usecookie':1}
        
        self.top = Toplevel()
        self.top.title("设置")
        self.top.resizable(False, False)
        
        self.var_urlListFile = StringVar()
        self.var_urlListFile.set(' ')          
        
        self.e6 = Entry(self.top,textvariable=self.var_urlListFile)
        
        self.e6.grid(row=0,column=1,columnspan=3)
        
        Label(self.top,text='设置URL列表文件').grid(row=0,column=0,sticky=W)
        self.button_browse=Button(self.top,text=' 浏览 ',command=self.browse)
        self.button_browse.grid(row=0,column=4)
        
        self.checkbutton=Checkbutton(self.top,text='使用cookie')
        self.checkbutton.grid(row=2,column=0,columnspan=3,sticky=W)
        
        self.b11 = Button(self.top,text='   确定   ',command=self.suretoset)
        self.b12 = Button(self.top,text='   取消   ',command=self.quitset)
        self.b11.grid(row=4,column=2)
        self.b12.grid(row=4,column=3)
    def browse(self):
        path=tkFileDialog.askopenfilename()
        self.var_urlListFile.set(path)
    def show(self):
        try:
            self.top.deiconify()
        except TclError:
            self=OptionsDialog(self.father)
            self.settings=self.father.settings
        self.var_urlListFile.set(self.settings['urllistfile'])
        self.checkbutton.variable=(self.settings['usecookie'])
        return self
    def hide(self):
        self.top.withdraw()
    
    def getsettings(self):                                                                            # 得到用户的设置                                                                     
        dic = {'urllistfile':self.var_urlListFile.get(),'usecookie':self.checkbutton.variable}
        return dic
        
    def suretoset(self):                     # 将用户的设置储存起来
        path=self.var_urlListFile.get()
        if not (os.path.isfile(path) or os.path.exists(path) or path==""):
            tkMessageBox.showerror(u"错误",u"文件不存在！")
            return 0
        if path:
            self.father.entry_targeturl['state']='readonly'
        else:
            self.father.entry_targeturl['state']='normal'
        self.top.withdraw()
        self.settings=self.getsettings()
        self.father.settings=self.getsettings()
    def quitset(self):                                                                                # 退出设置界面                                                                         
        self.top.withdraw()
        