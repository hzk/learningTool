#import tkinter as tk  
from tkinter import *
#from tkinter import ttk  

import tkinter as tk
import csv

class TransparentWindow(tk.Toplevel):
    def __init__(self, master=None, **kwargs):
        tk.Toplevel.__init__(self, master, **kwargs)
        self.overrideredirect(True)  # 隐藏窗口标题栏和边框
        self.attributes('-topmost', True)  # 窗口置顶
        self.attributes('-topmost', True)  # 保持在最上层  
        self.wm_attributes('-topmost', True)
        #self.attributes('-alpha', 0.5)  # 设置窗口完全透明
        self.configure(bg='systemTransparent')
        self.bind('<Enter>', self.on_mouse_enter)  # 鼠标移入事件
        self.bind('<Leave>', self.on_mouse_leave)  # 鼠标移出事件
        self.bind('<Button-1>', self.on_drag_start)  # 绑定鼠标左键拖拽事件
        self.bind('<B1-Motion>', self.on_drag_motion)  # 绑定鼠标左键移动事件
        self.paused = False

    def on_mouse_enter(self, event):
        #print("in")
        self.paused = True

    def on_mouse_leave(self, event):
        #print("out")
        self.paused = False

    def on_drag_start(self, event):
        self.x = event.x
        self.y = event.y

    def on_drag_motion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f'+{x}+{y}')

def load_words_from_csv(filename):
    words = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            words.append(row)
    return words

def display_word(window, words, index):
    label_text = words[index][0]+": "+words[index][1]+" "+words[index][2]+"\r"
    #" , ".join(words[index][:3])
    label_text = label_text+"\r".join(words[index][3:])
    label = tk.Label(window, text=label_text, font=('Helvetica', 20), fg='black',anchor='w',justify='left')
    #word, meaning = words[index]
    #label = tk.Label(window, text=f"{word}: {meaning}", font=('Helvetica', 16), fg='black')
    label.pack(pady=0, padx=0)
    #if not window.paused:  # 如果没有暂停切换，则显示单词
    window.after(10000, lambda: next_word(window, words, (index + 1) % len(words)))
    #else:  # 如果暂停切换，则重新安排定时事件
    #    window.after(1000, lambda: display_word(window, words, index))

def display_word__(window, words, index):
    word, meaning = words[index]
    #transparent_image = PhotoImage(width=1, height=1)
    #label = tk.Label(window, text=f"{word}: {meaning}", font=('Helvetica', 16),image=transparent_image, bg='white')
    label = tk.Label(window, text=f"{word}: {meaning}", font=('Helvetica', 16))
    #label.config(bg="systemTransparent")
    label.pack(pady=5, padx=10)
    window.after(10000, lambda: next_word(window, words, (index + 1) % len(words)))

def next_word(window, words, index):
    for widget in window.winfo_children():
        widget.destroy()
    display_word(window, words, index)

if __name__ == "__main__":
    # 读取单词
    words = load_words_from_csv('englishWordReview.csv')
    # 创建主窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    root.attributes('-topmost', True)  # 窗口置顶
    # 创建透明窗口
    transparent_window = TransparentWindow(root)
    # 显示第一个单词
    display_word(transparent_window, words, 0)
    transparent_window.mainloop()



