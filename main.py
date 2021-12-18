import tkinter
from tkinter import ttk
import GUI
import processData
import DoubleProcessData

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

tab = ttk.Notebook(win)
#---------------------------------
frame1 = tkinter.Frame(tab)
tab1 = tab.add(frame1, text="单打习惯性出手线路")
GUI.createTab(frame1, processData.process)
#---------------------------------
frame2 = tkinter.Frame(tab)
tab2 = tab.add(frame2, text="双打得分情况统计")
tab.pack(expand=True, fill=tkinter.BOTH)
GUI.createTab(frame2, DoubleProcessData.process)

# 设置选中tab1
tab.select(frame1)
win.mainloop()
