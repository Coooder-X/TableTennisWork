import tkinter
from tkinter import *
import tkinter.messagebox
import os
import windnd
from view.utils import process
from view.listBoxAct import dragged_files, clearFile


def doubleProcessTab(fatherFrame, callback):
    # 进入消息循环，可以写控件
    listBoxPanel = tkinter.Frame(fatherFrame)
    buttonPanel = tkinter.Frame(fatherFrame)
    label = tkinter.Label(fatherFrame,
                          text="请选择文件拖入（支持批量拖入）",
                          fg="red",
                          font=("黑体", 12),
                          justify="center",
                          anchor="ne")

    fileBox = Listbox(listBoxPanel, height=7, width=50, selectmode=SINGLE)
    fileBox.pack(side=LEFT, fill=BOTH, expand=True)
    # fileBox.insert(END, 'D:\MyGitKrakenFile\TableTennisWork\\20210726 东京奥运会 混双决赛 许昕刘诗雯vs水谷隼伊藤美诚-collect_project.json')

    windnd.hook_dropfiles(fileBox, func=dragged_files(fileBox))
    isProgress = IntVar()
    isProgress.set(0)

    #   当收到复选框改变时，修改 button 的回调参数，执行不同的业务逻辑
    def click(buttonGenerate):
        def res():
            print(isProgress.get())
            buttonGenerate.configure(text="生成", command=process(fileBox, callback, isProgress.get()))

        return res

    buttonGenerate = tkinter.Button(buttonPanel, text="生成", command=process(fileBox, callback, isProgress.get()))
    buttonDelete = tkinter.Button(buttonPanel, text="删除当前项", command=lambda item=fileBox: {
        item.delete("active"),
        tkinter.messagebox.showinfo('提示', '删除成功')
    })
    buttonClear = tkinter.Button(buttonPanel, text="清空", command=clearFile(fileBox))
    checkBoxPanel = tkinter.Frame(buttonPanel)

    Radiobutton(checkBoxPanel, text='默认', variable=isProgress, value=0, command=click(buttonGenerate)).pack()
    Radiobutton(checkBoxPanel, text='分阶段统计', variable=isProgress, value=1, command=click(buttonGenerate)).pack()
    Radiobutton(checkBoxPanel, text='分态势统计', variable=isProgress, value=2, command=click(buttonGenerate)).pack()

    print('GUI', isProgress)
    label.pack(side=TOP, pady=10)
    fileBox.focus()
    listBoxPanel.pack()
    buttonGenerate.pack(side=LEFT)
    buttonDelete.pack(side=RIGHT, padx=10)
    buttonClear.pack(side=RIGHT, padx=10)
    checkBoxPanel.pack(side=BOTTOM)
    buttonPanel.pack(pady=10)
