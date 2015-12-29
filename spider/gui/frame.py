#coding=utf-8
'''
Created on 2015年11月30日
底层和GUI间只由reptile.core.reptile.Reptile对象和此对象交互
这个类包装整个GUI，并由此调用底层的入口Reptile.fetchWebpage(url[,advancedOption])
@author: 
'''
#开始爬取的布局...
#正确打开设置、高级设置...
#正确布局设置界面...
#正确退出对话窗口...
#返回设置的内容，dictionary...
#设计更新进度条的接口(line 43-46)
from Tkinter import *
from FileDialog import *
import tkMessageBox
import tkFileDialog
class Frame(object):
    '''
    classdocs
    '''
    def __init__(self):                                                                                 # 构建基础用户界面的所有基本控件
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
        
        self.b1 = Button(self.root, text='   浏览   ', command=self.selectSavePath)
        self.b1.grid(row=1, column=4)
        self.b2 = Button(self.root, text='高级选项', command=self.openAdvancedOptionDialog)
        self.b2.grid(row=3, column=0)
        
        self.content=StringVar()#显示进度的StringVar
        self.label3=Label(self.root, textvariable=self.content)
        self.label3.grid(row=4, column=0, columnspan=5, sticky=W+E)
        
        self.b3 = Button(self.root, text='   设置   ', command=self.openOptionDialog)
        self.b3.grid(row=2, column=0, columnspan=1)
        
        self.b4 = Button(self.root, text='开始爬取',fg='red', command=self.start)
        self.b4.grid(row=2, column=3)
        
        self.b5 = Button(self.root, text='结束爬取', fg='blue',command=self.end)
        self.b5.grid(row=2, column=4)
        
        self.b6 = Button(self.root, text='退出程序', command=self.quit)
        self.b6.grid(row=3, column=4)
        
        self.optionDialog=OptionsDialog(self)
        self.optionDialog.hide()
        self.advancedOptionDialog=AdvancedOptionsDialog(self)
        self.advancedOptionDialog.hide()
        self.settings={}
        self.advancedsettings={}
        
        self.root.resizable(False, False)
        self.root.mainloop()
    def selectSavePath(self):                                                                         # 打开文件浏览器的函数
        path=tkFileDialog.askdirectory()
        self.str_savepath.set(path)
        print path

    def openAdvancedOptionDialog(self):                                                                         # 打开高级选项界面的函数
        #dialog = AdvancedOptionsDialog(self)
        self.advancedOptionDialog=self.advancedOptionDialog.show()
    def openOptionDialog(self):                                                                                 # 打开设置界面的函数                                                        
        #dialog = OptionsDialog(self)
        self.optionDialog=self.optionDialog.show()
        
    def getInfo(self):                                                                                  # 将用户的设置的目标网站与储存位置储存起来
        return self.str_targeturl.get(),self.str_savepath.get()
    
    def updateProcess(self,string):
        self.content.set(string)
        
    def start(self):                                                                                    # 调用程序开始爬取页面的函数
        #Label(self.root,textvariable=self.label3).grid(row=3,column=0,columnspan=5,sticky=W)
        if  not (self.str_targeturl.get() or (self.settings and self.settings["urllistfile"])):
            tkMessageBox.showerror(u"错误",u"没有设置目标网页地址，请设置目标URl或导入URL列表文件")
            return
        path=self.str_savepath.get()
        if not os.path.exists(path) or not os.path.isdir(path) :
            choose=tkMessageBox.askquestion(u"警告",u"文件路径不存在,是否新建路径?")
            if choose=='no':
                return
            else:
                os.makedirs(path)
        print "开始爬取"

    def end(self):                                                                                      # 调用程序结束页面的爬取的函数
        #self.label3.grid_forget()
        print "程序未完成，该功能暂时无法使用！"

    def quit(self):                                                                                     # 退出该程序
        self.root.quit()
#----------------------------------------------------------------------------------------------------------------
import os
class AdvancedOptionsDialog:
    def __init__(self,father): 
        self.father=father                                                                                # 构建高级选项用户界面的控件
        self.advancedsettings={}
        
        self.top = Toplevel()
        self.top.title("高级选项")
        
        self.label4 = StringVar()
        self.label4.set('URL参数列表')
        
        self.entry3 = StringVar()
        self.entry3.set('')
        self.label5 = StringVar()
        self.label5.set('paramname')
        
        self.label6 = StringVar()
        self.label6.set('      values      ')
        self.entry4 = IntVar()
        self.entry4.set(0)
        
        
        Label(self.top,textvariable=self.label4).grid(row=0,column=2,columnspan=3,sticky=W+E)
        
        self.b7 = Button(self.top,text='   添加   ',command=self.add_list)
        self.b7.grid(row=1,column=3,sticky=W+E)
        
        Label(self.top,textvariable=self.label5).grid(row=2,column=0,sticky=W)
        self.e3 = Entry(self.top,textvariable=self.entry3)
        self.e3.grid(row=2,column=1,columnspan=2)
        Label(self.top,textvariable=self.label6).grid(row=2,column=3)
        self.e4 = Entry(self.top,textvariable=self.entry4)
        self.e4.grid(row=2,column=4,columnspan=2)
        self.b8 = Button(self.top,text=' 删除 ',command=self.delete)
        self.b8.grid(row=2,column=6)
        
        self.b9 = Button(self.top,text='   确定   ',command=self.makesure)
        self.b9.grid(row=3,column=2)
        self.b10 = Button(self.top,text='   取消   ',command=self.quittop)
        self.b10.grid(row=3,column=4)
        
    def add_list(self):
        ''''''
        
    def delete(self):
        ''''''
        
    def show(self):
        self.top.deiconify()
        return self
    def hide(self):
        self.top.withdraw()              
    #def getnumberofrows(self):
    #    return self.entry3.get()                                                                       # 得到用户的高级设置
                    
    def makesure(self):
        self.top.withdraw()
        self.openAdvancedOptionDialog=self.getAdvancedSettings()
        self.father.openAdvancedOptionDialog=self.getAdvancedSettings()
        
    def quittop(self):                                                                                 # 退出高级选项界面
        self.top.withdraw()
        
    def getAdvancedSettings(self):
        #@todo
        return {}
#----------------------------------------------------------------------------------------------------------------
class OptionsDialog:
    def __init__(self,father):                                                                                # 构建设置用户界面的控件
        self.father=father
        self.settings={'threads':1,'urllistfile':'','usecookie':1}
        
        self.top = Toplevel()
        self.top.title("设置")
        self.top.resizable(False, False)
        
        #self.entry5 = StringVar()
        #self.entry5.set(' ')  
        self.entry_urlListFile = StringVar()
        self.entry_urlListFile.set(' ')          
        self.entry_threads = StringVar()
        self.entry_threads.set('1')
        
        #self.e5 = Entry(self.top,textvariable=self.entry5)
        self.e6 = Entry(self.top,textvariable=self.entry_urlListFile)
        self.e4 = Entry(self.top,textvariable=self.entry_threads)
        
        #self.e5.grid(row=0,column=1,columnspan=3)
        self.e6.grid(row=0,column=1,columnspan=3)
        self.e4.grid(row=1,column=1,columnspan=3)
        
        #Label(self.top,text='   设置URL参数  ').grid(row=0,column=0,sticky=W)
        Label(self.top,text='设置URL列表文件').grid(row=0,column=0,sticky=W)
        Label(self.top,text='       线程数   ').grid(row=1,column=0,sticky=W)
        
        
        self.checkbutton=Checkbutton(self.top,text='使用cookie')
        self.checkbutton.grid(row=2,column=0,columnspan=3,sticky=W)
        
        self.b11 = Button(self.top,text='   确定   ',command=self.suretoset)
        self.b12 = Button(self.top,text='   取消   ',command=self.quitset)
        self.b11.grid(row=4,column=2)
        self.b12.grid(row=4,column=3)
        
    def show(self):
        try:
            self.top.deiconify()
        except TclError:
            self=OptionsDialog(self.father)
            self.settings=self.father.settings
        self.entry_threads.set(self.settings['threads'])
        self.entry_urlListFile.set(self.settings['urllistfile'])
        self.checkbutton.variable=(self.settings['usecookie'])
        return self
    def hide(self):
        self.top.withdraw()
    
    def getsettings(self):                                                                            # 得到用户的设置                                                                     
        dic = {'threads':self.entry_threads.get(),'urllistfile':self.entry_urlListFile.get(),'usecookie':self.checkbutton.variable}
        return dic
        
    def suretoset(self):                     # 将用户的设置储存起来
        path=self.entry_urlListFile.get()
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