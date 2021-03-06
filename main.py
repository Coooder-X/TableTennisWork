import tkinter
from tkinter import ttk
from single import process_data
from double import double_process_data
from view.double_process_view import doubleProcessTab
from view.single_process_view import singleProcessTab

# 创建主窗口
win = tkinter.Tk()
# 设置标题
win.title("比赛数据统计")
# 设置大小和位置
sw = win.winfo_screenwidth()
sh = win.winfo_screenheight()
ww = 400
wh = 300
x = (sw - ww) / 2 - 350
y = (sh - wh) / 2
win.geometry("%dx%d+%d+%d" % (ww, wh, x, y))

tab = ttk.Notebook(win)
#---------------------------------
frame1 = tkinter.Frame(tab)
tab1 = tab.add(frame1, text="单打习惯性出手线路")
singleProcessTab(frame1, process_data.process)
#---------------------------------
frame2 = tkinter.Frame(tab)
tab2 = tab.add(frame2, text="双打得分情况统计")
doubleProcessTab(frame2, double_process_data.process)
tab.pack(expand=True, fill=tkinter.BOTH)
# 设置选中tab1
tab.select(frame1)
win.mainloop()

'''
   带控制台：   Pyinstaller -F -i tabletennis.ico main.py -n DataProcess-0.9
   不带控制台： Pyinstaller -F -w -i tabletennis.ico main.py -n DataProcess-0.9
'''