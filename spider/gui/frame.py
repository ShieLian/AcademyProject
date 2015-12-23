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
class Frame(object):
    '''
    classdocs
    '''
    def __init__(self):                                                                                 # 构建基础用户界面的所有基本控件
        self.root = Tk()
        self.root.title("网页爬取器")
        
        self.entry1 = StringVar()
        self.entry2 = StringVar()

        self.label1=Label(self.root,text='目标网页地址：')
        self.label1.grid(row=0, column=0, sticky=W)
        
        self.e1 = Entry(self.root, textvariable=self.entry1)
        self.e1.grid(row=0, column=1, columnspan=3)
        
        self.label2 = Label(self.root, text='   保存在： ')
        self.label2.grid(row=1, column=0, sticky=W)
        
        self.e2 = Entry(self.root, textvariable=self.entry2)
        self.e2.grid(row=1, column=1, columnspan=3)
        
        self.b1 = Button(self.root, text='   浏览   ', command=self.documentscanning)
        self.b1.grid(row=1, column=4)
        self.b2 = Button(self.root, text='高级选项', command=self.advancedsettings)
        self.b2.grid(row=3, column=0)
        
        self.label3=Label(self.root, text='   ')
        self.label3.grid(row=4, column=0, columnspan=5, sticky=W+E)
        '''s = (此处调用修改标签的函数)''' 
        self.label3["text"] = s
        
        self.b3 = Button(self.root, text='   设置   ', command=self.settings)
        self.b3.grid(row=2, column=0, columnspan=1)
        
        self.b4 = Button(self.root, text='开始爬取',fg='red', command=self.start)
        self.b4.grid(row=2, column=3)
        
        self.b5 = Button(self.root, text='结束爬取', fg='blue',command=self.end)
        self.b5.grid(row=2, column=4)
        
        self.b6 = Button(self.root, text='退出程序', command=self.quit)
        self.b6.grid(row=3, column=4)
        
        self.root.mainloop()
    def documentscanning(self):                                                                         # 打开文件浏览器的函数
       print "文件浏览器暂时不能打开"                           

    def advancedsettings(self):                                                                         # 打开高级选项界面的函数
        dialog = opentop1()
                                                                                                       


    def settings(self):                                                                                 # 打开设置界面的函数                                                        
        dialog = opentop2()
        
                

    def getInfo(self):                                                                                  # 将用户的设置的目标网站与储存位置储存起来
        return self.entry1.get(),self.entry2.get()
    
    def start(self):                                                                                    # 调用程序开始爬取页面的函数
        #Label(self.root,textvariable=self.label3).grid(row=3,column=0,columnspan=5,sticky=W)
        print "程序未完成，该功能暂时无法使用！"

    def end(self):                                                                                      # 调用程序结束页面的爬取的函数
        #Label(self.root,textvariable=self.label3).grid_forget(row=3,column=0,columnspan=5,sticky=W)
        #Label(self.root,textvariable=self.label3).grid_forget()
        #self.label3.grid_forget()
        print "程序未完成，该功能暂时无法使用！"

    def quit(self):                                                                                     # 退出该程序
        self.root.quit()

class opentop1:
    def __init__(self):                                                                                 # 构建高级选项用户界面的控件
        self.top = Toplevel()
        self.top.title("高级选项")
        self.label4 = StringVar()
        self.label4.set('需要爬取的网页行数为: ')
        self.entry3 = StringVar()
        self.entry3.set('100')
        
        Label(self.top,textvariable=self.label4).grid(row=0,column=0,columnspan=3,sticky=W)
        self.e3 = Entry(self.top,textvariable=self.entry3)
        self.e3.grid(row=0,column=3)
        self.b7 = Button(self.top,text='确定',command=self.makesure)
        self.b7.grid(row=2,column=2)
        self.b8 = Button(self.top,text='取消',command=self.quittop)
        self.b8.grid(row=2,column=3)                                                            
                        
    def getnumberofrows(self):
        self.top.mainloop()
        return self.entry3.get()                                                                       # 得到用户的高级设置
                    
    def makesure(self):
        f = open("与爬取网页行数有关文件所处位置","w")                                                   # 将用户的高级设置储存
        self.top.destroy()
        
    def quittop(self):                                                                                 # 退出高级选项界面
        self.top.destroy()
        
                
class opentop2:
    def __init__(self):                                                                                # 构建设置用户界面的控件
        self.top = Toplevel()
        self.top.title("设置")
        self.label6 = StringVar()
        self.label6.set('   设置URL参数  ') 
        self.entry5 = StringVar()
        self.entry5.set(' ')  
        self.label7 = StringVar()
        self.label7.set('设置URL列表文件')
        self.entry6 = StringVar()
        self.entry6.set(' ')          
        self.label5 = StringVar()
        self.label5.set('       线程数   ')
        self.entry4 = StringVar()
        self.entry4.set('1')
        self.checkbutton = IntVar()
        self.checkbutton.set(1)     
        
        Label(self.top,textvariable=self.label6).grid(row=0,column=0,sticky=W)
        self.e5 = Entry(self.top,textvariable=self.entry5)
        self.e5.grid(row=0,column=1,columnspan=3)        
        Label(self.top,textvariable=self.label7).grid(row=1,column=0,sticky=W)
        self.e6 = Entry(self.top,textvariable=self.entry6)                                     
        self.e6.grid(row=1,column=1,columnspan=3)
        Label(self.top,textvariable=self.label5).grid(row=2,column=0,sticky=W)
        self.e4 = Entry(self.top,textvariable=self.entry4)
        self.e4.grid(row=2,column=1,columnspan=3)
        Checkbutton(self.top,text='使用cookie').grid(row=3,column=0,columnspan=3,sticky=W)
        self.b11 = Button(self.top,text='   确定   ',command=self.suretoset)
        self.b11.grid(row=4,column=2)
        self.b12 = Button(self.top,text='   取消   ',command=self.quitset)                                
        self.b12.grid(row=4,column=3)
          
    def getsettings(self):                                                                            # 得到用户的设置                                                                     
        self.top.mainloop()
        dic = {'线程数':self.entry4.get(),'设置URL参数':self.entry5.get(),'设置URL列表文件':self.entry6.get()}
        return dic
        
    def suretoset(self):                                                                              # 将用户的设置储存起来                                                                        
        self.top.destroy()
        
    def quitset(self):                                                                                # 退出设置界面                                                                         
        self.top.destroy()        