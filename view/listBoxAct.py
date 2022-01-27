import os
from tkinter import *


# 拖动文件到 listBox 里
def dragged_files(listBox):
    def updateListBox(files):
        fileList = []
        for item in files:
            item = item.decode('gbk')
            fileList.append(item)
        fileList.sort(key=lambda fileName: os.path.basename(fileName)[0:8], reverse=True)  # file 排序规则
        for item in fileList:
            listBox.insert(END, item)

    return updateListBox


def clearFile(listBox):
    def clear():
        listBox.delete(0, listBox.size())

    return clear

