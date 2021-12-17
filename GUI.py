# -*- coding:utf-8 -*-

from tkinter import *
import tkinter
from tkinter import ttk
import tkinter.messagebox
import processData
import os
import windnd


def dragged_files(listBox):

    def updateListBox(files):
        for item in files:
            item = item.decode('gbk')
            listBox.insert(END, item)

    return updateListBox


def showinfo(listBox):
    def show():
        fileNameList = []
        if listBox.size() == 0:
            tkinter.messagebox.showinfo('提示', '请拖入文件')
            return
        for i in range(listBox.size()):
            fileName = listBox.get(i)
            if fileName == '':
                tkinter.messagebox.showinfo('提示', '请输入文件绝对路径')
                return
            if os.path.isfile(fileName):
                if fileName[-4:] != 'json':
                    tkinter.messagebox.showinfo('提示', '存在不是json的文件，请输入json文件')
                fileNameList.append(fileName)
            else:
                tkinter.messagebox.showinfo('提示', '文件不存在')
        try:
            processData.process(fileNameList)
        except PermissionError:
            tkinter.messagebox.showinfo('提示', '某些文件可能已打开或被占用，请先关闭')
    return show


def clearFile():
    lb.delete(0, lb.size())


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
#-----------------------------------------------------------

tab = ttk.Notebook(win)

frame1 = tkinter.Frame(tab)
tab1 = tab.add(frame1, text="单打习惯性出手线路")
# 设置选中tab1
tab.select(frame1)

frame2 = tkinter.Frame(tab)
tab2 = tab.add(frame2, text="双打得分情况统计")
tab.pack(expand=True, fill=tkinter.BOTH)
#-----------------------------------------------------------

# 进入消息循环，可以写控件
fm1 = tkinter.Frame(frame1)
fm2 = tkinter.Frame(frame1)
label = tkinter.Label(frame1,
                      text="请选择文件拖入（支持批量拖入）",
                      fg="red",
                      font=("黑体", 12),
                      justify="center",
                      anchor="ne")
label.pack(side=TOP, pady=10)

# sb = Scrollbar(fm1)    #垂直滚动条组件
# sb.pack(side=BOTTOM, fill=X)  #设置垂直滚动条显示的位置
lb = Listbox(fm1, height=7, width=50, selectmode=SINGLE)
lb.pack(side=LEFT, fill=BOTH, expand=True)
lb.focus()
# sb.config(command=lb.xview)
fm1.pack()

windnd.hook_dropfiles(lb, func=dragged_files(lb))


buttonGenerate = tkinter.Button(fm2, text="生成", command=showinfo(lb))
buttonGenerate.pack(side=LEFT)
buttonDelete = tkinter.Button(fm2, text="删除当前项", command=lambda item=lb: {
    item.delete("active"),
    tkinter.messagebox.showinfo('提示', '删除成功')
})
buttonDelete.pack(side=RIGHT, padx=10)
buttonClear = tkinter.Button(fm2, text="清空", command=clearFile)
buttonClear.pack(side=RIGHT, padx=10)
fm2.pack(pady=10)

win.mainloop()

# 20211128 休斯顿世乒赛 女单半决赛 陈梦vs王曼昱-collect_project(new).json
# D:\MyGitKrakenFile\TableTennisWork\20211128 休斯顿世乒赛 女单半决赛 陈梦vs王曼昱-collect_project(new).json
