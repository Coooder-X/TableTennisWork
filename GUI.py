# -*- coding:utf-8 -*-

from tkinter import *
import tkinter
import tkinter.messagebox
import os
import windnd


# 拖动文件到 listBox 里
def dragged_files(listBox):
    def updateListBox(files):
        for item in files:
            item = item.decode('gbk')
            listBox.insert(END, item)
    return updateListBox


# 根据传入回调，执行不同数据处理的逻辑
def process(listBox, callback):
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
            callback(fileNameList, lambda: tkinter.messagebox.showinfo('提示', '单打功能不支持传入双打数据'))
        except PermissionError:
            tkinter.messagebox.showinfo('提示', '某些文件可能已打开或被占用，请先关闭')
    return show


def clearFile(listBox):
    def clear():
        listBox.delete(0, listBox.size())
    return clear


def createTab(frame, callback):
    # 进入消息循环，可以写控件
    fm1 = tkinter.Frame(frame)
    fm2 = tkinter.Frame(frame)
    label = tkinter.Label(frame,
                          text="请选择文件拖入（支持批量拖入）",
                          fg="red",
                          font=("黑体", 12),
                          justify="center",
                          anchor="ne")
    label.pack(side=TOP, pady=10)

    # sb = Scrollbar(fm1)    #垂直滚动条组件
    # sb.pack(side=BOTTOM, fill=X)  #设置垂直滚动条显示的位置
    fileBox = Listbox(fm1, height=7, width=50, selectmode=SINGLE)
    fileBox.pack(side=LEFT, fill=BOTH, expand=True)
    fileBox.focus()
    # fileBox.insert(END, 'D:\MyGitKrakenFile\TableTennisWork\\20210726 东京奥运会 混双决赛 许昕刘诗雯vs水谷隼伊藤美诚-collect_project.json')
    # sb.config(command=fileBox.xview)
    fm1.pack()

    windnd.hook_dropfiles(fileBox, func=dragged_files(fileBox))

    buttonGenerate = tkinter.Button(fm2, text="生成", command=process(fileBox, callback))
    buttonGenerate.pack(side=LEFT)
    buttonDelete = tkinter.Button(fm2, text="删除当前项", command=lambda item=fileBox: {
        item.delete("active"),
        tkinter.messagebox.showinfo('提示', '删除成功')
    })
    buttonDelete.pack(side=RIGHT, padx=10)
    buttonClear = tkinter.Button(fm2, text="清空", command=clearFile(fileBox))
    buttonClear.pack(side=RIGHT, padx=10)
    fm2.pack(pady=10)


# 20211128 休斯顿世乒赛 女单半决赛 陈梦vs王曼昱-collect_project(new).json
# D:\MyGitKrakenFile\TableTennisWork\20211128 休斯顿世乒赛 女单半决赛 陈梦vs王曼昱-collect_project(new).json
