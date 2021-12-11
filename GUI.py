# -*- coding:utf-8 -*-

from tkinter import *
import tkinter
import tkinter.messagebox
import processData
import os


def showinfo():
    # 获取输入的内容
    fileName = entry.get()
    if fileName == '':
        tkinter.messagebox.showinfo('提示', '请输入文件绝对路径')
        return
    print(entry.get())
    if os.path.isfile(fileName):
        if fileName[-4:] != 'json':
            tkinter.messagebox.showinfo('提示', '该文件不是json文件，请输入json文件')
        processData.process(entry.get())
    else:
        tkinter.messagebox.showinfo('提示', '文件不存在')


# 创建主窗口
win = tkinter.Tk()
# 设置标题
win.title("比赛数据统计")
# 设置大小和位置
sw = win.winfo_screenwidth()
sh = win.winfo_screenheight()
ww = 400
wh = 300
x = (sw - ww) / 2
y = (sh - wh) / 2
win.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
# win.geometry("400x300+200+50")

# 进入消息循环，可以写控件
fm1 = tkinter.Frame(win)
# fm2 = tkinter.Frame(win)
label = tkinter.Label(win,
                      text="请输入文件绝对路径",
                      fg="red",
                      font=("黑体", 12),
                      # width=20,
                      # height=10,
                      # wraplength=100,
                      justify="center",
                      anchor="ne")
# label.grid(row=0, column=0)
label.pack(side=TOP, pady=50)

entry = tkinter.Entry(fm1, width=25, font=("Consolas", 15))
entry.pack(side=LEFT)
# entry.grid(row=1, column=0)

button = tkinter.Button(fm1, text="生成", command=showinfo)
# button.grid(row=1, column=1)
button.pack(side=RIGHT, padx=3)
fm1.pack()

win.mainloop()

# 20211128 休斯顿世乒赛 女单半决赛 陈梦vs王曼昱-collect_project(new).json
# D:\MyGitKrakenFile\TableTennisWork\20211128 休斯顿世乒赛 女单半决赛 陈梦vs王曼昱-collect_project(new).json
