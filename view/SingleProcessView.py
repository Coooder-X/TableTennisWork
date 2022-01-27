import tkinter
from tkinter import *
import tkinter.messagebox
import windnd

from view.utils import process
from view.listBoxAct import dragged_files, clearFile


def singleProcessTab(fatherFrame, callback):
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
    windnd.hook_dropfiles(fileBox, func=dragged_files(fileBox))

    buttonGenerate = tkinter.Button(buttonPanel, text="生成", command=process(fileBox, callback))
    buttonDelete = tkinter.Button(buttonPanel, text="删除当前项", command=lambda item=fileBox: {
        item.delete("active"),
        tkinter.messagebox.showinfo('提示', '删除成功')
    })
    buttonClear = tkinter.Button(buttonPanel, text="清空", command=clearFile(fileBox))

    label.pack(side=TOP, pady=10)
    fileBox.focus()
    listBoxPanel.pack()
    buttonGenerate.pack(side=LEFT)
    buttonDelete.pack(side=RIGHT, padx=10)
    buttonClear.pack(side=RIGHT, padx=10)
    buttonPanel.pack(pady=10)
