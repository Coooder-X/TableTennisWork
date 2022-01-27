# -*- coding:utf-8 -*-
import tkinter
import tkinter.messagebox
import os


# 根据传入回调，执行不同数据处理的逻辑
def process(listBox, callback, isProgress=-1):
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
            fileNameList.sort(key=lambda fileName: os.path.basename(fileName)[0:8], reverse=True)
            if isProgress == -1:
                callback(fileNameList, lambda: tkinter.messagebox.showinfo('提示', '单打功能不支持传入双打数据'))
            else:
                callback(fileNameList, lambda: tkinter.messagebox.showinfo('提示', '单打功能不支持传入双打数据'), isProgress)
        except PermissionError:
            tkinter.messagebox.showinfo('提示', '某些文件可能已打开或被占用，请先关闭')

    return show

